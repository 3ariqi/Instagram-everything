#!/usr/bin/env python3
"""
install.py - install the Instagram-everything skills for any AI agent.

It audits the pack first and refuses to install if the audit fails. Then it
copies every skills/ie-* folder, checks the copy against the release manifest,
and sets up the user's workspace: one folder per kind of work, named in the
language the user chose, plus a start-here file. Standard library only: no
network, no subprocess.

Recommended: everything in one folder the user picks.
  python3 install.py --workspace "D:/AI-Work/instagram" --agent claude --lang ar
      skills  -> D:/AI-Work/instagram/.claude/skills   (open the agent from this folder)
      outputs -> D:/AI-Work/instagram/01-ريلز, 02-كابشن, ...
  --agent codex or gemini puts the skills in <workspace>/.agents/skills,
  --agent all puts them in both.

Skills for all projects, outputs in a folder of their own:
  python3 install.py --global --agent claude --workspace "~/Instagram-everything" --lang en
      skills  -> ~/.claude/skills  (codex: ~/.agents/skills, gemini: ~/.gemini/skills)

Any other agent:
  python3 install.py --dest <that agent's skills folder> --workspace <folder> --lang ar

  --dry-run shows what would happen and writes nothing.

Every ie-* folder must land in the SAME skills folder, because the skills call
the shared tools in ie-tools/ through a sibling path.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "skills", "ie-tools"))
import selfcheck  # noqa: E402

GLOBAL_TARGETS = {
    "claude": "~/.claude/skills",
    "agents": "~/.agents/skills",
    "codex": "~/.agents/skills",
    "gemini": "~/.gemini/skills",
}
# Inside the workspace (or a project), relative to its root.
LOCAL_TARGETS = {
    "claude": ".claude/skills",
    "agents": ".agents/skills",
    "codex": ".agents/skills",
    "gemini": ".agents/skills",
}
DEFAULT_WORKSPACE = "~/Instagram-everything"
SKIP_DIRS = {"__pycache__", ".git"}
SKIP_SUFFIX = (".pyc", ".pyo")
LAYOUT = os.path.join(HERE, "skills", "ie-tools", "data", "workspace_layout.json")


def audit(root):
    """Return (ok, fails, warns). A pack that cannot be audited is not ok."""
    if not os.path.isdir(os.path.join(root, "skills")):
        return False, 1, 0
    rep, n = selfcheck.scan(root)
    fails, warns = rep.count("FAIL"), rep.count("WARN")
    return (n > 0 and fails == 0), fails, warns


def pack_version(root):
    try:
        with open(os.path.join(root, "skills", "ie-tools", "VERSION"), encoding="utf-8") as fh:
            return fh.read().strip() or "unknown"
    except OSError:
        return "unknown"


def load_layout():
    with open(LAYOUT, encoding="utf-8") as fh:
        return json.load(fh)


def source_files(root):
    """(relative_path, absolute_path) for every file under skills/ie-*."""
    base = os.path.join(root, "skills")
    out = []
    for name in sorted(os.listdir(base)):
        top = os.path.join(base, name)
        if not (name.startswith("ie-") and os.path.isdir(top) and not os.path.islink(top)):
            continue
        for d, dirs, files in os.walk(top, followlinks=False):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not os.path.islink(os.path.join(d, x))]
            for f in sorted(files):
                full = os.path.join(d, f)
                if f.endswith(SKIP_SUFFIX) or os.path.islink(full) or f == "workspace.json":
                    continue
                out.append((os.path.relpath(full, base), full))
    return out


def install(root, dest, dry_run=False):
    """Copy the skills to dest. Returns the list of relative paths written."""
    written = []
    for rel, full in source_files(root):
        target = os.path.join(dest, rel)
        written.append(rel)
        if dry_run:
            continue
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(full, "rb") as src:
            data = src.read()
        with open(target, "wb") as dst:
            dst.write(data)
    return written


def stale_skills(root, dest):
    """ie-* folders in dest that this release no longer ships (renamed or removed)."""
    if not os.path.isdir(dest):
        return []
    shipped = {n for n in os.listdir(os.path.join(root, "skills")) if n.startswith("ie-")}
    return sorted(n for n in os.listdir(dest)
                  if n.startswith("ie-") and n not in shipped and os.path.isdir(os.path.join(dest, n)))


def old_flat_install(workspace):
    """ie-* skill folders sitting directly in the workspace (the v1.0 layout)."""
    if not os.path.isdir(workspace):
        return []
    return sorted(n for n in os.listdir(workspace)
                  if n.startswith("ie-") and os.path.isdir(os.path.join(workspace, n)))


def start_here(layout, lang, workspace, skills_dirs):
    folders = [f for f in layout["folders"]]
    if lang == "ar":
        lines = ["# ابدأ من هنا", "",
                 "هذا مجلد عملك في Instagram-everything. كل نوع شغل له مجلد، والمساعد يحفظ فيه تلقائياً.", "",
                 "## المجلدات", ""]
        for f in folders:
            lines.append("- **%s**: %s" % (f["ar"], f["desc_ar"]))
        lines += ["", "## كيف تبدأ", "",
                  "1. افتح المساعد (Claude Code أو Codex أو Gemini CLI) من هذا المجلد نفسه.",
                  "2. اكتب `/ie-setup` (في Codex: `$ie-setup`) أو قل «ابدأ».",
                  "3. اطلب بكلامك: «اكتب لي ريل عن حماية الحساب». ستجد الناتج في مجلده.", "",
                  "## لا تعدّل هذه", ""]
        for d in skills_dirs:
            lines.append("- `%s`: الحزمة نفسها (المهارات والأدوات). أي تعديل فيها يكشفه الفحص الأمني." % d)
        lines += ["", "اسم كل ملف ناتج: التاريخ ثم الموضوع، مثل `2026-11-11-سرقة-الحسابات.md`.", ""]
    else:
        lines = ["# Start here", "",
                 "This is your Instagram-everything workspace. Each kind of work has a folder, and the assistant saves there for you.", "",
                 "## Folders", ""]
        for f in folders:
            lines.append("- **%s**: %s" % (f["en"], f["desc_en"]))
        lines += ["", "## How to start", "",
                  "1. Open the assistant (Claude Code, Codex or Gemini CLI) from this folder.",
                  "2. Type `/ie-setup` (`$ie-setup` in Codex) or say \"start\".",
                  "3. Ask in plain words: \"write me a reel about account security\". The result lands in its folder.", "",
                  "## Do not edit", ""]
        for d in skills_dirs:
            lines.append("- `%s`: the pack itself (skills and tools). The security check catches any change." % d)
        lines += ["", "Every output file is named date then topic, for example `2026-11-11-account-theft.md`.", ""]
    return "\n".join(lines)


def setup_workspace(workspace, lang, skills_dirs, version, dry_run=False):
    """Create the output folders and the start-here file; return {key: path}."""
    layout = load_layout()
    paths = {f["key"]: os.path.join(workspace, f[lang]) for f in layout["folders"]}
    if dry_run:
        return paths
    for p in paths.values():
        os.makedirs(p, exist_ok=True)
    shown = [os.path.relpath(d, workspace) if d.startswith(workspace) else d for d in skills_dirs]
    with open(os.path.join(workspace, layout["start_here"][lang]), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(start_here(layout, lang, workspace, shown))
    info = {"workspace": workspace, "lang": lang, "version": version, "folders": paths,
            "settings": paths["settings"]}
    for d in skills_dirs:
        with open(os.path.join(d, "ie-tools", "workspace.json"), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(info, fh, ensure_ascii=False, indent=2)
    return paths


def main(argv=None):
    ap = argparse.ArgumentParser(description="Install Instagram-everything for any AI agent.")
    ap.add_argument("--agent", choices=sorted(GLOBAL_TARGETS) + ["all"], help="which agent")
    ap.add_argument("--workspace", help="the folder the user chose for their work (and, by default, the skills)")
    ap.add_argument("--project", help=argparse.SUPPRESS)  # v1.0.1 name for --workspace
    ap.add_argument("--global", dest="global_", action="store_true",
                    help="put the skills in the agent's folder for all projects; the workspace holds outputs only")
    ap.add_argument("--dest", help="a custom skills folder (for any other agent)")
    ap.add_argument("--lang", choices=["ar", "en"], help="language of folders, files and replies (default ar)")
    ap.add_argument("--dry-run", action="store_true", help="show what would happen, write nothing")
    args = ap.parse_args(argv)

    workspace = args.workspace or args.project
    lang = args.lang
    if args.dest and not workspace:
        # An update into an existing install keeps the user's workspace and language.
        prev = os.path.join(os.path.abspath(os.path.expanduser(args.dest)), "ie-tools", "workspace.json")
        if os.path.isfile(prev):
            with open(prev, encoding="utf-8") as fh:
                info = json.load(fh)
            workspace = info.get("workspace")
            lang = args.lang or info.get("lang")
    migrate = False
    if args.dest and not workspace:
        # A v1.0 install put the ie-* folders straight into the folder the user
        # chose. Updating it in place would keep that mess and create the
        # workspace somewhere else, so turn that folder into the workspace.
        dest_abs = os.path.abspath(os.path.expanduser(args.dest))
        if (os.path.isdir(os.path.join(dest_abs, "ie-tools"))
                and os.path.basename(dest_abs.rstrip(os.sep)).lower() != "skills"):
            migrate = True
            workspace = dest_abs
            args.workspace = dest_abs
            args.dest = None
            args.agent = args.agent or "all"
            print("MIGRATE=%s" % dest_abs)
            print("This folder holds an older loose install. It becomes the workspace: the pack goes into "
                  ".claude/skills and .agents/skills inside it, and the loose ie-* folders are listed below.")
    lang = lang if lang in ("ar", "en") else "ar"
    if not args.agent and not args.dest:
        print("error: choose --agent (claude, codex, gemini, agents, all) or --dest FOLDER", file=sys.stderr)
        return 2
    if workspace:
        workspace = os.path.abspath(os.path.expanduser(workspace))
        parent = os.path.dirname(workspace)
        if not os.path.isdir(workspace) and not os.path.isdir(parent):
            print("error: folder not found: %s" % workspace, file=sys.stderr)
            return 2
    else:
        workspace = os.path.abspath(os.path.expanduser(DEFAULT_WORKSPACE))

    workspace_given = bool(args.workspace or args.project)
    agents = [args.agent] if args.agent and args.agent != "all" else (["claude", "agents"] if args.agent else [])
    dests = []
    for a in agents:
        if args.global_ or not workspace_given:
            d = os.path.expanduser(GLOBAL_TARGETS[a])
        else:
            d = os.path.join(workspace, LOCAL_TARGETS[a])
        if args.agent == "all" and args.global_:
            for g in GLOBAL_TARGETS.values():
                g = os.path.expanduser(g)
                if g not in dests:
                    dests.append(g)
            continue
        if d not in dests:
            dests.append(d)
    if args.dest:
        dests.append(os.path.abspath(os.path.expanduser(args.dest)))

    ok, fails, warns = audit(HERE)
    if not ok:
        print("REFUSED: the security audit did not pass (%d fail, %d warn). Nothing was installed.\n"
              "Run: python3 skills/ie-tools/selfcheck.py ." % (fails, warns), file=sys.stderr)
        return 1
    version = pack_version(HERE)
    print("Audit PASS (%d warn). Pack version %s." % (warns, version))

    manifest = os.path.join(HERE, "skills", "ie-tools", selfcheck.MANIFEST)
    for dest in dests:
        written = install(HERE, dest, dry_run=args.dry_run)
        folders = sorted({w.split(os.sep)[0] for w in written})
        print("%s %d files in %d skills -> %s" % ("Would copy" if args.dry_run else "Installed",
                                                 len(written), len(folders), dest))
        if not args.dry_run:
            changed, missing, extra = selfcheck.verify(dest, manifest)
            if changed or missing:
                print("REFUSED: the copy in %s does not match the release manifest (%d changed, %d missing)."
                      % (dest, len(changed), len(missing)), file=sys.stderr)
                return 1
            print("INSTALLED_PATH=%s" % dest)
            stale = stale_skills(HERE, dest)
            if stale:
                print("STALE=%s" % ", ".join(os.path.join(dest, n) for n in stale))
                print("These skills are no longer part of the pack (renamed or removed). Ask the user, then delete them.")
        else:
            print("TARGET_PATH=%s" % dest)

    paths = setup_workspace(workspace, lang, dests, version, dry_run=args.dry_run)
    print("%s (%s) -> %s" % ("Would set up the workspace" if args.dry_run else "Workspace ready", lang, workspace))
    print("WORKSPACE_PATH=%s" % workspace)
    for key in ("reels", "reports", "settings"):
        print("  %-9s %s" % (key, paths[key]))
    old = old_flat_install(workspace)
    if old:
        print("OLD_LAYOUT=%s" % ", ".join(old))
        print("These skill folders sit directly in the workspace from an older install. They are copies and are "
              "no longer used: ask the user, then delete them.")
    if not args.dry_run:
        local = [d for d in dests if d.startswith(workspace + os.sep)]
        if local:
            print("Open the agent from %s (or restart it there) so it picks the skills up." % workspace)
        else:
            print("Restart the agent (or open its /skills list) so it picks the new skills up.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
