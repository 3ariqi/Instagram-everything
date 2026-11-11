---
name: ie-setup
description: >-
  First-run setup for the Instagram-everything pack: asks a few optional
  questions about the user's account, language, dialect and signature, learns
  their writing style from samples of their own posts, and saves it so every
  other skill writes in their voice. Use when the user says "setup", "start",
  "learn my style", "ابدأ", "إعداد", "تعلّم أسلوبي", "هذي منشوراتي", or when no
  config exists yet.
---

# ie-setup

Run once, then whenever the user wants the pack to learn more about them. Follow
`<base>/../ie-setup/INTAKE.md` for how to ask and what to save.

**Files and language:** follow `<base>/../ie-setup/WORKSPACE.md`: read settings from the workspace, save the result in this skill's folder there, and use the language the user chose.

## Step 1: a short, optional interview

Ask in one batch, in the user's language. Every question can be skipped.

1. **Account:** the handle and one line on what it is about.
2. **Field:** tech and security · religious · political and public affairs ·
   social and community · health · money and business · education ·
   entertainment and lifestyle · other (one or two). Every skill adapts its
   sources, tone and red lines to it (see `NICHES.md`).
3. **Platforms:** Instagram, TikTok, YouTube Shorts, X, or all of them.
4. **Language and register:** Arabic, English or both. For Arabic: plain standard
   Arabic, a local dialect (which one), or a mix. Keep technical terms in
   English or translate them?
5. **Audience:** who they are, how technical, what they want from the account.
6. **Voice:** three words for how you sound; words you never use; emoji (none, a
   few, plenty); on camera, voiceover or text only.
7. **Signature:** the closing lines added to every script and caption, and the
   name credit, if any.

## Step 2: learn from the user's own writing

Ask for three to ten of their own posts or scripts (more is better), pasted or
attached. Save them to `samples.txt` with a line of `---` between posts and run:

```bash
python3 <base>/../ie-tools/stylekit.py learn samples.txt
```

Show the result in plain words and go through the "what I need you to confirm"
lines with the user. A recurring last line is offered as their signature; the
colloquial words found are offered as a hint about dialect, never decided for
them. If they have no samples yet, skip this step and say the style will be
learned from the first drafts they edit.

## Step 3: save

Write `<settings>/config.md` (from the answers) and
`<settings>/style.md` (only what the user confirmed). Say where they
are. Tell the user they can say "update my style" at any time, and that the pack
reads these two files before it writes anything.

## What to say at the end

Two lines: what was saved, and the one thing they can try next, for example
"اكتب لي ريل عن ..." (the reel skill will ask its own few questions, or use your
saved defaults).
