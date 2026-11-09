#!/usr/bin/env python3
"""
selfcheck.py - audit a skill pack (this one, or any other) before you install it.

Standalone on purpose: it imports nothing from the pack it is checking, so a
tampered helper file cannot change its verdict. Standard library only.

What FAILS the check:
  - Python that imports anything outside a small allowlist (no network,
    no subprocess, no ctypes, no pickle, no base64, no importlib ...)
  - eval / exec / compile / __import__, os.system / popen / exec* / spawn* /
    fork, and getattr() used to reach any of those by name
  - hidden Unicode: zero-width and invisible characters, bidi overrides, tag
    characters, private-use characters (a joiner inside an emoji is allowed)
  - prompt-injection phrasing in instructions: overriding earlier
    instructions, hiding actions from the person, acting without their
    knowledge, sending keys or files out
  - shell pipes from the internet into a shell, base64 decoding, rm -rf on home
  - long encoded blobs, binary files, symbolic links
  - links through shorteners, raw IP addresses or punycode domains

What WARNS: HTML comments in Markdown (text the reader does not see),
"install" commands inside a SKILL.md, file deletion in Python, requests that the agent
disclose its own instructions, mentions of credential stores.

What it REPORTS: every place a Python file can write a file, every external
domain linked from the instructions.

Usage:
  python3 selfcheck.py .                  # run from the pack root
  python3 selfcheck.py ~/.claude/skills
  python3 selfcheck.py . --json
Exit code 1 on any FAIL, 2 if there was nothing to check (a wrong path is
never a PASS), 0 otherwise, so CI can block a change.
"""

import argparse
import ast
import json
import os
import re
import sys
import unicodedata

ALLOWED_IMPORTS = {
    "argparse", "json", "os", "re", "sys", "statistics", "unicodedata", "math", "collections",
    "string", "textwrap", "datetime", "typing", "ast", "unittest", "tempfile", "io", "pathlib",
    "contextlib", "functools", "itertools", "dataclasses",
}
BANNED_CALLS = {"eval", "exec", "compile", "__import__", "breakpoint",
                "getattr", "setattr", "delattr", "globals", "locals", "vars"}
BANNED_OS = {"system", "popen", "fork", "forkpty", "kill", "killpg", "execv", "execve", "execl",
             "execle", "execlp", "execlpe", "execvp", "execvpe", "spawnl", "spawnle", "spawnlp",
             "spawnlpe", "spawnv", "spawnve", "spawnvp", "spawnvpe", "posix_spawn", "posix_spawnp",
             "startfile", "putenv", "chmod", "chown", "setuid", "setgid"}
DELETE_OS = {"remove", "unlink", "rmdir", "removedirs"}
SKIP_DIRS = {".git"}  # nothing else may hide files from the audit
TEXT_EXT = {".py", ".md", ".json", ".txt", ".yml", ".yaml", ".toml", ".cfg", ".ini", ".sh", ".tsv", ".csv", ""}

# Patterns are written with character classes ([o], [e]) so this file does not
# match its own rules when it scans itself.
INJECTION_FAIL = [
    r"ign[o]re\s+(all\s+|any\s+)?(the\s+)?(previous|prior|above|earlier)\s+(instructions|rules|messages|prompts?)",
    r"disr[e]gard\s+(all\s+|any\s+)?(the\s+)?(previous|prior|above|system|earlier)",
    r"(do\s+not|don'?t|never)\s+(tell|inform|alert|warn|notify)\s+the\s+us[e]r",
    r"with[o]ut\s+(telling|asking|informing|notifying|alerting)\s+the\s+us[e]r",
    r"(you\s+are\s+now|from\s+now\s+on,?\s+you\s+are)\s+(in\s+)?(developer\s+mode|dan\b|jailbr[o]ken|unrestricted)",
    r"(send|upload|post|exfiltrat\w*|forward)\s+.{0,40}(\.ssh|id_[r]sa|\.env\b|credentials?|cookies|api[_ ]?keys?|access\s+tokens?)",
    r"(curl|wget)\s+[^\n|]*\|\s*(ba|z|da)?sh\b",
    r"base64\s+(-d|--decode)\b",
    r"\brm\s+-rf\s+[~/$]",
    r"/etc/pass[w]d|\bid_[r]sa\b|~/\.ss[h]/",
    r"تجا[ه]ل\s+(كل\s+|جميع\s+)?(التعليمات|الأوامر|القواعد|ما\s+سبق)",
    r"(لا|ولا)\s+تخب[ر]\s+المستخدم",
    r"(دون|بدون)\s+(علم|إذن|اذن|إخبار|اخبار|موافقة)\s+المستخد[م]",
    r"أرس[ل]\s+.{0,40}(كلمات\s+المرور|كلمة\s+المرور|المفاتيح|ملفات\s+المستخدم)\s+(إلى|الى)",
]
INJECTION_WARN = [
    r"syst[e]m\s+prompt",
    r"(reveal|print|show|output|repeat)\s+(your\s+)?(hidden\s+)?(instructions|system\s+pr[o]mpt)",
    r"~/\.a[w]s\b|gcloud/cred[e]ntials|keych[a]in|\.net[r]c\b",
]
INSTALL_WARN = r"\b(pip3?\s+install|npm\s+(i|install)\b|npx\s+|brew\s+install|apt(-get)?\s+install|curl\s+-[a-zA-Z]*[sSL])"
URL_RE = re.compile(r"https?://([^/\s)\"'>\]]+)", re.IGNORECASE)
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly", "rb.gy", "ow.ly",
              "shorturl.at", "tiny.cc", "s.id", "rebrand.ly", "t.ly"}
BLOB_RE = re.compile(r"[A-Za-z0-9+/]{80,}={0,2}")


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, path, line, what):
        self.items.append({"level": level, "file": path, "line": line, "what": what})

    def count(self, level):
        return sum(1 for i in self.items if i["level"] == level)


def _is_emoji(ch):
    o = ord(ch)
    return unicodedata.category(ch) == "So" or 0x1F000 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF \
        or 0x1F3FB <= o <= 0x1F3FF or o == 0xFE0F


def check_unicode(rel, text, rep):
    for i, ch in enumerate(text):
        o = ord(ch)
        cat = unicodedata.category(ch)
        bad = False
        if ch == "\u200D":
            prev = text[i - 1] if i else ""
            nxt = text[i + 1] if i + 1 < len(text) else ""
            bad = not (prev and nxt and _is_emoji(prev) and _is_emoji(nxt))
        elif 0xE0020 <= o <= 0xE007F:
            j = i
            while j > 0 and 0xE0020 <= ord(text[j - 1]) <= 0xE007F:
                j -= 1
            bad = not (j > 0 and text[j - 1] == "\U0001F3F4")
        elif cat in ("Cf", "Co", "Cs", "Cn") or (cat == "Cc" and ch not in "\n\r\t"):
            bad = True
        if bad:
            line = text.count("\n", 0, i) + 1
            rep.add("FAIL", rel, line, "hidden character U+%04X %s" % (o, unicodedata.name(ch, "").lower()))


def check_python(rel, text, rep, local_modules):
    try:
        tree = ast.parse(text)
    except SyntaxError as e:
        rep.add("FAIL", rel, e.lineno or 0, "Python does not parse: cannot be audited")
        return
    # Names that refer to the os module, however they were imported.
    os_names = {"os"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                root = a.name.split(".")[0]
                if root == "os":
                    os_names.add(a.asname or "os")
                if root not in ALLOWED_IMPORTS and root not in local_modules:
                    rep.add("FAIL", rel, node.lineno, "import outside the allowlist: %s" % a.name)
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if node.level == 0 and root not in ALLOWED_IMPORTS and root not in local_modules:
                rep.add("FAIL", rel, node.lineno, "import outside the allowlist: %s" % node.module)
            if node.level == 0 and root == "os":
                for a in node.names:
                    if a.name in BANNED_OS or a.name == "*":
                        rep.add("FAIL", rel, node.lineno, "imports a banned os function: %s" % a.name)
                    elif a.name in DELETE_OS:
                        rep.add("WARN", rel, node.lineno, "imports a file-deleting function: %s" % a.name)
            if node.level == 0 and root in ("builtins", "__builtin__"):
                rep.add("FAIL", rel, node.lineno, "imports builtins")
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in BANNED_CALLS and isinstance(node.ctx, ast.Load):
            # any reference counts, not only a direct call: "e = eval" is the same thing.
            # getattr/globals/vars are banned too: they reach any name, including a banned one.
            rep.add("FAIL", rel, node.lineno, "dynamic code execution or name lookup: %s" % node.id)
        elif isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name) and fn.value.id in os_names:
                if fn.attr in BANNED_OS:
                    rep.add("FAIL", rel, node.lineno, "process/system call: os.%s()" % fn.attr)
                elif fn.attr in DELETE_OS:
                    rep.add("WARN", rel, node.lineno, "deletes files: os.%s()" % fn.attr)
            if isinstance(fn, ast.Name) and fn.id == "open":
                mode = None
                if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
                    mode = node.args[1].value
                for kw in node.keywords:
                    if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                        mode = kw.value.value
                if isinstance(mode, str) and any(c in mode for c in "wax+"):
                    rep.add("INFO", rel, node.lineno, "writes a file (mode %r)" % mode)
            if isinstance(fn, ast.Attribute) and fn.attr in ("write_text", "write_bytes"):
                rep.add("INFO", rel, node.lineno, "writes a file (%s)" % fn.attr)
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id == "sys" and node.attr == "modules":
                rep.add("WARN", rel, node.lineno, "touches sys.modules")
            if node.value.id in ("__builtins__", "builtins"):
                rep.add("FAIL", rel, node.lineno, "reaches into builtins")
        elif isinstance(node, ast.Name) and node.id == "__builtins__":
            rep.add("FAIL", rel, node.lineno, "reaches into builtins")


def check_text(rel, text, rep, is_skill):
    for pat in INJECTION_FAIL:
        for m in re.finditer(pat, text, re.IGNORECASE):
            rep.add("FAIL", rel, text.count("\n", 0, m.start()) + 1, "instruction pattern: \"%s\"" % m.group(0)[:60])
    for pat in INJECTION_WARN:
        for m in re.finditer(pat, text, re.IGNORECASE):
            rep.add("WARN", rel, text.count("\n", 0, m.start()) + 1, "sensitive mention: \"%s\"" % m.group(0)[:60])
    for m in BLOB_RE.finditer(text):
        if not re.fullmatch(r"[=\-#]+", m.group(0)):
            rep.add("FAIL", rel, text.count("\n", 0, m.start()) + 1, "long encoded-looking blob (%d chars)" % len(m.group(0)))
    if rel.endswith(".md"):
        for m in re.finditer(r"<!--", text):
            rep.add("FAIL" if is_skill else "WARN", rel, text.count("\n", 0, m.start()) + 1,
                    "HTML comment: text the reader cannot see")
    if is_skill:
        for m in re.finditer(INSTALL_WARN, text):
            rep.add("WARN", rel, text.count("\n", 0, m.start()) + 1, "install command in instructions: %s" % m.group(0).strip())
    for m in URL_RE.finditer(text):
        host = m.group(1).lower().split(":")[0]
        line = text.count("\n", 0, m.start()) + 1
        if host in SHORTENERS:
            rep.add("FAIL", rel, line, "link shortener hides the destination: %s" % host)
        elif re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host):
            rep.add("FAIL", rel, line, "link to a raw IP address: %s" % host)
        elif "xn--" in host:
            rep.add("FAIL", rel, line, "punycode domain: %s" % host)
        else:
            rep.add("INFO", rel, line, "links to %s" % host)


def scan(root):
    rep = Report()
    root = os.path.abspath(os.path.expanduser(root))
    files = []
    for d, dirs, names in os.walk(root, followlinks=False):
        for sub in list(dirs):
            full = os.path.join(d, sub)
            if os.path.islink(full):
                rep.add("FAIL", os.path.relpath(full, root), 0, "symbolic link to %s" % os.readlink(full))
                dirs.remove(sub)
            elif sub in SKIP_DIRS:
                dirs.remove(sub)
        for n in names:
            files.append(os.path.join(d, n))
    local_modules = {os.path.splitext(os.path.basename(f))[0] for f in files if f.endswith(".py")}
    for f in sorted(files):
        rel = os.path.relpath(f, root)
        if os.path.islink(f):
            rep.add("FAIL", rel, 0, "symbolic link to %s" % os.readlink(f))
            continue
        ext = os.path.splitext(f)[1].lower()
        if "__pycache__" in rel.split(os.sep) or ext == ".pyc":
            rep.add("WARN", rel, 0, "compiled bytecode cache: not source, cannot be audited; delete it (find . -name __pycache__ -prune -exec rm -r {} +)")
            continue
        with open(f, "rb") as fh:
            data = fh.read()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            rep.add("FAIL", rel, 0, "binary or non-UTF-8 file: cannot be read as text")
            continue
        if ext not in TEXT_EXT and os.path.basename(f) not in ("LICENSE",):
            rep.add("WARN", rel, 0, "unexpected file type %s" % ext)
        if b"\x00" in data:
            rep.add("FAIL", rel, 0, "contains NUL bytes")
        check_unicode(rel, text, rep)
        if ext == ".py":
            check_python(rel, text, rep, local_modules)
        check_text(rel, text, rep, is_skill=os.path.basename(f) == "SKILL.md")
    return rep, len(files)


def main():
    ap = argparse.ArgumentParser(description="Audit a skill pack before installing it.")
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="hide INFO lines")
    args = ap.parse_args()
    target = os.path.abspath(os.path.expanduser(args.path))
    if not os.path.isdir(target):
        print("  ERROR  not a folder: %s\n  Nothing was checked. This is not a PASS." % args.path, file=sys.stderr)
        sys.exit(2)
    rep, n = scan(args.path)
    if n == 0:
        print("  ERROR  no files found in %s\n  Nothing was checked. This is not a PASS." % args.path, file=sys.stderr)
        sys.exit(2)
    fails, warns = rep.count("FAIL"), rep.count("WARN")
    verdict = "FAIL" if fails else "WARN" if warns else "PASS"
    if args.json:
        print(json.dumps({"verdict": verdict, "files": n, "items": rep.items}, ensure_ascii=False, indent=2))
    else:
        order = {"FAIL": 0, "WARN": 1, "INFO": 2}
        for it in sorted(rep.items, key=lambda i: (order[i["level"]], i["file"], i["line"])):
            if args.quiet and it["level"] == "INFO":
                continue
            print("  %-4s  %s:%d  %s" % (it["level"], it["file"], it["line"], it["what"]))
        print("\n  %s   %d files   %d fail   %d warn" % (verdict, n, fails, warns))
        if verdict == "PASS":
            print("  No banned code, hidden characters or injection patterns found.")
            print("  Still read every SKILL.md yourself before installing: a check is not a review.\n")
        else:
            print("  Do not install until every FAIL is understood.\n" if fails else
                  "  Read each WARN before installing.\n")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
