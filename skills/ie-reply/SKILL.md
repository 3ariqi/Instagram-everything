---
name: ie-reply
description: >-
  Sort the comments under the user's own posts and draft replies to the ones
  worth answering, in Arabic or English, including critics, leads and
  questions that deserve a whole Reel. Use when the user pastes comments, says
  "reply to these", "handle my comments", "رد على التعليقات", "واحد كتب لي",
  or is dealing with a hater, a critic or a lead.
---

# ie-reply

Replies in the first hour after posting keep a post's conversation alive, and
a question with real demand behind it is a ready-made next Reel.

## Intake (optional questions)

Follow `<base>/../ie-setup/INTAKE.md`: look at the saved config, style and presets first, ask only what is
missing, in one batch, every question optional. For replies:

1. **Tone / النبرة:** as in the config, or different today
2. **Length / الطول:** one line · two or three lines
3. **Spam and risky accounts / الحسابات المشبوهة:** just flag them · draft a report note
4. **Good questions / الأسئلة الجيدة:** also suggest turning them into Reels · replies only

Skipped answers use the saved defaults. Say what you assumed in one line at the top.

## Input

The user pastes the comments (with handles if possible) or screenshots. Do not
scrape the thread with a browser.

## Triage first, and say the counts

| bucket | what it is | what it gets |
| --- | --- | --- |
| KEYWORD | the word the post asked for | what was promised, sent by hand or by the user's approved tool |
| LEAD | someone describing the problem the user solves | a real answer in public, then one line offering help |
| SUBSTANCE | adds data, disagrees, extends | the most thoughtful reply on the thread |
| QUESTION | a question many people have | flagged for a Reel reply (`/ie-reel`, formula #16) |
| SUPPORT | "🔥", "شكراً", a tag | a like, and a few words at most |
| RISK | a scam link, an impersonator, someone asking for codes, doxxing | do not reply: hide or delete, report, and warn followers if needed |
| NOISE | bait, spam, bad faith | nothing |

Write replies in that order and stop when the value stops.

## The RISK bucket (security accounts get this a lot)

- Comments with links promising "account recovery", "verification" or
  "followers": never reply with engagement. Run the text through
  `python3 <base>/../ie-tools/scamcheck.py -` and tell the user what it is.
- Accounts impersonating the user (same photo, similar handle) replying to
  followers: report the impersonator, and draft a pinned comment or Story
  warning followers that the real account never asks for money or codes.

## How to reply

- Answer the actual question in the reply. Don't send people to DMs for an
  answer they could have had in public.
- Use their name once, at the start.
- Match their length. A four-word comment does not get a paragraph.
- **A critic:** concede the true part first, in their words, then hold your
  point with a source. Never twice on the same thread.
- **A hater:** no reply. Hide it if it's abusive. Instagram's comment
  controls exist for this.
- **A lead:** answer fully in public. The offer of help is one sentence at
  the end, not a pitch.
- Same dialect and register as the comment.

Run every reply through `<base>/../ie-tools/clean.py`.

## Output

```
REPLIES  ·  64 comments  ·  20 KEYWORD, 2 LEAD, 3 SUBSTANCE, 2 QUESTION, 33 SUPPORT, 2 RISK, 2 NOISE

LEAD
@handle - "حسابي انسرق وغيروا الإيميل"
> ادخل من صفحة "نسيت كلمة المرور" واختر ...، ولو احتجت مساعدة راسلني.

QUESTION -> REEL
@handle - "طيب والآيفون؟"  (31 likes on the comment: that's a Reel)

RISK  (2)  do not reply
@insta_support_44 - link to "recover-account" site: scam pattern, 85/100. Delete + report.
```

The user posts every reply. Nothing is posted by this skill.
