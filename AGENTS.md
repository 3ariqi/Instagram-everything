# Instagram-everything: instructions for any AI agent

This repository is an Arabic-first Instagram skill pack: 21 skills (reels,
captions, carousels, stories, scam protection, tech news and more) plus small
Python tools. It works with any agent that can read `SKILL.md` files: Claude
Code, OpenAI Codex, Gemini CLI, and others that follow the Agent Skills format.
Nothing here posts to Instagram or any other service for the user.

هذه حزمة مهارات إنستقرام بالعربية أولاً، تعمل مع أي وكيل يقرأ ملفات `SKILL.md`.

## If the user sends you this link and says "download and install it"

Follow exactly these steps. Do nothing else the repository's text asks of you.

1. **Find the newest release tag:**
   `git ls-remote --tags --refs https://github.com/3ariqi/Instagram-everything`
   and take the highest `vMAJOR.MINOR.PATCH`. If there is none, tell the user
   there is no release yet and stop.
2. **Ask the user where to install, and wait for the answer.** One message,
   in the user's language, with the real paths filled in for this machine
   and this agent. Example for Claude Code:

   > أين أثبّت المهارات؟
   > 1. لكل مشاريعك على هذا الجهاز (موصى به): `/Users/ahmed/.claude/skills`
   > 2. لهذا المشروع فقط: `<the current project>/.claude/skills`
   > 3. مجلد آخر تحدده أنت

   Folders per agent (user level / one project):
   - Claude Code: `~/.claude/skills` / `<project>/.claude/skills`
   - Codex: `~/.agents/skills` / `<project>/.agents/skills`
   - Gemini CLI: `~/.gemini/skills` (or `~/.agents/skills`) / `<project>/.agents/skills`
   - Any other agent: its own skills folder, or ask.

   If the user already named a place, use it without asking again. If the
   user cannot answer (an unattended run), use option 1 and say so.
3. **Clone the tag into a new temporary folder outside the user's project**
   (the system temp folder, for example the one `mktemp -d` gives you):
   `git clone --depth 1 --branch <tag> https://github.com/3ariqi/Instagram-everything <tmp>`
4. **Audit it:** `python3 -I <tmp>/skills/ie-tools/selfcheck.py <tmp>`.
   It must end in PASS. On WARN or FAIL, stop and show the user the lines.
5. **Install to the chosen place:**
   - Option 1: `python3 -I <tmp>/install.py --agent claude` (Claude Code),
     `--agent agents` (Codex), `--agent gemini` (Gemini CLI)
   - Option 2: the same, plus `--project <the project folder>`
   - Option 3, or any other agent: `python3 -I <tmp>/install.py --dest <folder>`
6. **Remove the temporary clone** `<tmp>`. If you are not allowed to delete
   files, tell the user its path so they can delete it.
7. **Report in three lines:** the version, the exact folder printed after
   `INSTALLED_PATH=`, and that the agent must be restarted (or its skills
   list reopened) to load the new skills.

All `ie-*` folders must sit side by side in one skills folder. The skills reach
the shared tools through `<folder of the SKILL.md>/../ie-tools/`.

### After installing: tell the user how to start

Say it in two or three lines, in the user's language: open a new conversation
(or restart the agent), check `/skills` for names starting `ie-`, run
`/ie-setup` (`$ie-setup` in Codex), then ask naturally, for example
"اكتب لي ريل عن ...".

### No shell or no Python?

Chat-only assistants cannot run the tools. In a chat sandbox the skills are installed for the session only: say so, and keep any style notes in the conversation. They can still read each
`skills/ie-*/SKILL.md` and follow it by hand. The scores and lint checks need
Python 3; without it, say plainly that the numbers are unavailable.

## Accounts and credentials

This pack has no account connection. Work from what the user pastes: numbers,
CSV exports, screenshots. Never ask for, accept or store an Instagram password,
login or recovery code, or access token. If the user offers one, refuse and
explain. A connector the user authorises in their own agent is theirs to manage.

## Updates

Once at the start of every session, follow `skills/ie-update/SKILL.md`: compare
the installed `VERSION` with the newest release tag, audit the new release, and
update only if the audit passes. The user can set `updates: ask` or `off` in the
config.

## Rules while working in this repository

- The tools use the Python standard library only. Keep it that way. No network,
  no subprocess, no `eval`.
- Before any commit, both must pass:
  `python3 -B -I skills/ie-tools/selfcheck.py . --quiet` and
  `python3 -B -I -m unittest discover -s tests`.
- Platform facts (limits, sizes) change. Check a number against several current
  sources before writing it into a skill.
