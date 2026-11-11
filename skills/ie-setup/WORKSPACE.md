# Where files live, and which language to use

Every skill in this pack follows this file for three things: where to read the
user's settings, where to save what it produces, and which language to use.

## 1. Find the workspace

Read `<base>/../ie-tools/workspace.json` (the installer writes it). It holds:

- `workspace`  the folder the user chose for their work
- `lang`       `ar` or `en`, chosen by the user at install time
- `folders`    the full path of each output folder, by key
- `settings`   the settings folder (same as `folders.settings`)

If the file is missing (an older install, or the pack was copied by hand), use
`~/.instagram-everything/` for settings, save outputs in the current working
folder, take the language from `config.md` or from how the user writes, and
suggest reinstalling once so they get the organised workspace.

## 2. Language

Use `lang` for everything the user sees: replies, questions, file names, and the
text of the outputs, unless the user asks for a specific output in another
language ("write this caption in English"). Folder names are already in that
language; never create a folder in the other one.

## 3. Settings

All in the `settings` folder:

- `config.md`   who the user is, dialect, audience, signature, `updates:`
- `style.md`    how the user writes, measured by `stylekit.py` and confirmed by them
- `presets.md`  the answers they chose to keep as defaults, one block per task
- `log.md`, `plan.md`, `swipe.md`   results, the weekly plan, research notes

Written only with the user's clear yes (see `INTAKE.md`).

Moving from an older install: if `~/.instagram-everything/` exists and the
`settings` folder has no `config.md` yet, offer once to copy those files into
`settings`. Copy only on a yes, and leave the old folder for the user to delete.

## 4. Where each skill saves

Save every finished output as a Markdown file in the folder for this skill,
named `YYYY-MM-DD-<short-topic>.md` in the user's language (today's date,
three to five words for the topic, words joined with `-`). If that name
exists, add `-2`, `-3`. Tell the user the file path in one line at the end.

| Folder key | Skills |
|---|---|
| `reels` | ie-reel (script), ie-edit (edit plan) |
| `captions` | ie-caption |
| `carousels` | ie-carousel, ie-story |
| `engage` | ie-comment, ie-reply, ie-dm |
| `news` | ie-news (script and evidence table in one file) |
| `crosspost` | ie-crosspost, ie-repurpose, ie-natural (when the user wants the cleaned text kept) |
| `reports` | ie-audit, ie-plan, ie-viral, ie-profile |
| `security` | ie-scamguard, ie-harden (a checklist of what was done), ie-selfcheck |
| `settings` | ie-setup; ie-update writes nothing else |
| `inbox` | nothing is saved here: it is where the user drops screenshots, exports and old posts for you to read |

Short answers that are not a deliverable (a quick question, a one-line reply)
are not saved. When unsure, ask once: "Save it to <folder>?"

## 5. Never touch the pack

The skills and tools sit in `<workspace>/.claude/skills` or `.agents/skills`
(or the agent's own folder). Never edit, move or delete anything there, and
never save outputs there. If the user wants to change how a skill behaves,
tell them to save the preference in `presets.md` instead. An update replaces
those files, and `selfcheck.py --verify` reports any change to them.
