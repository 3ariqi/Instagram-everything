---
name: ie-comment
description: >-
  Write comments on other people's Instagram posts that read as a person with
  an opinion, in Arabic or English. Use when the user pastes a post and says
  "comment on this", "what do I say here", "اكتب تعليق", "علق على هذا المنشور",
  or wants a batch for a daily engagement round.
---

# ie-comment

A good comment near the top of a busy post is seen by more people than many
accounts' own posts, and a stranger can tap straight through to the profile.
A generic comment is worse than none: it marks the account as a bot to the one
person whose opinion mattered, the creator.

## Intake (optional questions)

Follow `<base>/../ie-setup/INTAKE.md`: look at the saved config, style and presets first, ask only what is
missing, in one batch, every question optional. For a comment:

1. **Tone / النبرة:** respectful · curious · funny
2. **Length / الطول:** one line · two lines
3. **Mention your account / ذكر حسابك:** no · yes

Skipped answers use the saved defaults. Say what you assumed in one line at the top.

## Input

The user pastes the post text or a screenshot, with the account name. If they
send a link you cannot open, ask them to paste it. Do not browse the feed.

## Comment types: pick by what the post is

| type | when | shape |
| --- | --- | --- |
| Add a fact | you can support the post with a number or source | "وعندنا نفس الشيء: ..." |
| The missing case | right but incomplete | "صحيح، إلا إذا ..." |
| Respectful disagree | you think it's wrong | agree with one part, then the fork |
| Extend one line | one line in it is the good one | quote it, build on it |
| The real question | the post skipped the hard part | one question, specific |
| Your experience | you've done the thing | what happened, two sentences |
| The correction | a factual error, especially in security | right, brief, kind, sourced |
| One-liner | you want presence | under 10 words, true or funny |

## Rules

- One to three sentences. A paragraph gets collapsed.
- Never open with "منشور رائع", "Great post", "Love this", "So true", or an
  emoji alone.
- Never restate the post. Never pitch, never "check my page".
- **Security corrections:** if the post gives advice that would put people at
  risk (for example, "SMS codes are enough"), the correction comment is worth
  writing even on a big account. Cite a source in plain words, stay kind.
- In Arabic, match the post's register: reply to a dialect post in dialect,
  to formal Arabic in simple formal Arabic.

Run each option through `<base>/../ie-tools/clean.py`: in a short comment,
one stock phrase is loud.

## Output

Two options of different types, labelled, and which one to post:

```
[Your experience]
فعّلت تطبيق المصادقة بدل الرسائل بعد ما انسرق رقمي، والفرق إن الرمز ما يطلع من جوالي.

[The real question]
طيب ولو ضاع الجوال نفسه؟ وين تحفظ رموز الاسترداد؟

Post the first: it adds something the post didn't have.
```

## Batch mode

For an engagement round: the user pastes 5-10 posts in one message; return one
comment each. Keep a short note in `~/.instagram-everything/log.md` of accounts
commented on this week, so the round doesn't hit the same three accounts daily.

## Boundaries

This skill writes comments; the user posts them. Never post, never automate
comments, never use a browser to publish on the user's behalf. Automated
engagement breaks Instagram's terms and gets accounts restricted.
