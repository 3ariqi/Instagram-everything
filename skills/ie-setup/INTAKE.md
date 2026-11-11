# The intake protocol

Every writing and editing skill in this pack starts with a few optional
questions, because two people who both say "write me a reel" want different
things: a different platform, length, voice, tone and level of detail. This file
is the one protocol they all follow. Read it before asking anything.

## Where things are saved

In the `settings` folder of the user's workspace: see `WORKSPACE.md` next to
this file. `<settings>` in any skill means that folder.

- `config.md`   who the user is, language, dialect, signature
- `style.md`    how the user writes, measured by `stylekit.py` and confirmed by them
- `presets.md`  the answers they chose to keep as defaults, one block per task
- `log.md`, `swipe.md`, `plan.md`   results, research and the weekly plan, used by other skills

If that folder cannot be written or does not survive between conversations (a
chat sandbox, for example), say so once, write the same files into the working
folder, hand them to the user as files, and ask them to attach those files next
time. Never pretend something was saved when it was not.

## The user's field

Every writing skill reads `Field:` in `config.md` and applies its section of
`NICHES.md` (next to this file): which sources count, the tone the audience
expects, and the red lines. Religious, political, social and tech accounts get
different output from the same request. If no field is saved, add the field
question to the batch below.

## The five steps

1. **Look before asking.** Read `config.md`, `style.md` and the task's block in
   `presets.md`. Never ask what they already answer.
2. **A saved preset for this task exists:** say what you will use in one line
   ("Reel, 30 seconds, direct to camera, friendly Gulf Arabic. Change anything?")
   and start unless they change something.
3. **No preset:** ask the task's questions in **one batch**, at most six, each
   with two to four short options. Every question is optional, and the user can
   answer "skip", "ابدأ" or "start" at any point. Use the agent's question
   widget if it has one, otherwise a numbered list they can answer in one line
   ("1b 2a 3 skip"). Ask in the user's language.
4. **Skipped or unanswered:** use the defaults from `config.md` and `style.md`,
   and put one line at the top of the output saying what you assumed, so the
   user can correct it ("Assumed: Reels, 30s, friendly, no emoji").
5. **After delivering:** offer once to keep the answers as the default for this
   task. Save only on a clear yes. Say where it was saved.

## Learning the user's style

- **From samples.** When the user pastes or attaches posts of their own (three
  is a start, ten is better), put them in a file with a line of `---` between
  posts and run `python3 <base>/../ie-tools/stylekit.py learn samples.txt`.
  Show them the result in plain words and ask them to confirm or correct each
  line. Save to `style.md` only what they confirm.
- **From edits.** When the user rewrites your draft, save your draft and their
  final text as two files and run
  `python3 <base>/../ie-tools/stylekit.py diff draft.txt final.txt`. Tell them
  what changed in one or two lines and ask whether to remember it. One edit is an
  assumption; the same change twice is a preference.
- **From a plain instruction** ("I never use emoji", "keep it shorter"): record it
  after they confirm, in their own words.
- Never save a guess about the user. Measurements and confirmed answers only.

## Rules

- At most one batch of questions, plus one follow-up if an answer opens a real
  gap. If the user seems in a hurry, ask nothing and state your assumptions.
- Questions are about the work, never about the person's private life, health,
  money or identity.
- Never ask for a password, a login code, a recovery code or an access token,
  for any account. If something needs the account's data, ask for an export or a
  screenshot (see `ie-audit`).
- Keep the user's own signature and name credit exactly as they wrote them.
