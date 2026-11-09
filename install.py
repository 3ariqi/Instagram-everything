#!/usr/bin/env python3
"""
install.py - install the Instagram-everything skills for any AI agent.

It audits the pack first and refuses to install if the audit fails, then copies
every skills/ie-* folder to the skills folder of the agent you choose. Standard
library only: no network, no subprocess.

  python3 install.py --agent claude      # ~/.claude/skills
  python3 install.py --agent agents      # ~/.agents/skills  (Codex and Gemini CLI read this one)
  python3 install.py --agent codex       # ~/.codex/skills
  python3 install.py --agent gemini      # ~/.gemini/skills
  python3 install.py --agent all         # all four
  python3 install.py --dest /some/folder # any other agent: point it at that agent's skills folder
  python3 install.py --agent agents --dry-run

Every ie-* folder must land in the SAME skills folder, because the skills call
the shared tools in ie-tools/ through a sibling path.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "skills", "ie-tools"))
import selfcheck  # noqa: E402

TARGETS = {
    "claude": "~/.claude/skills",
    "agents": "~/.agents/skills",
    "codex": "~/.codex/skills",
    "gemini": "~/.gemini/skills",
}
SKIP_DIRS = {"__pycache__", ".git"}
SKIP_SUFFIX = (".pyc", ".pyo")


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
                if f.endswith(SKIP_SUFFIX) or os.path.islink(full):
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


def main(argv=None):
    ap = argparse.ArgumentParser(description="Install Instagram-everything for any AI agent.")
    ap.add_argument("--agent", choices=sorted(TARGETS) + ["all"], help="which agent's skills folder to use")
    ap.add_argument("--dest", help="a custom skills folder (for any other agent)")
    ap.add_argument("--dry-run", action="store_true", help="show what would be copied, copy nothing")
    args = ap.parse_args(argv)

    if not args.agent and not args.dest:
        print("error: choose --agent (claude, agents, codex, gemini, all) or --dest FOLDER", file=sys.stderr)
        return 2
    dests = []
    if args.agent == "all":
        dests += [os.path.expanduser(p) for p in TARGETS.values()]
    elif args.agent:
        dests.append(os.path.expanduser(TARGETS[args.agent]))
    if args.dest:
        dests.append(os.path.abspath(os.path.expanduser(args.dest)))

    ok, fails, warns = audit(HERE)
    if not ok:
        print("REFUSED: the security audit did not pass (%d fail, %d warn). Nothing was installed.\n"
              "Run: python3 skills/ie-tools/selfcheck.py ." % (fails, warns), file=sys.stderr)
        return 1
    print("Audit PASS (%d warn). Pack version %s." % (warns, pack_version(HERE)))

    for dest in dests:
        written = install(HERE, dest, dry_run=args.dry_run)
        folders = sorted({w.split(os.sep)[0] for w in written})
        print("%s %d files in %d skills -> %s" % ("Would copy" if args.dry_run else "Installed",
                                                 len(written), len(folders), dest))
    if not args.dry_run:
        print("Restart the agent (or open its /skills list) so it picks the new skills up.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
