---
name: ie-plan
description: >-
  Build a weekly Instagram content plan in Arabic or English from the user's own
  results and research, not from generic templates: what to post each day, in
  which format, on which hook formula. Use when the user says "content plan",
  "what should I post this week", "خطة محتوى", "جدول نشر", "ماذا أنشر", or
  starts a new week.
---

# ie-plan

## Intake (optional questions)

**Files and language:** follow `<base>/../ie-setup/WORKSPACE.md`: read settings from the workspace, save the result in this skill's folder there, and use the language the user chose.

Follow `<base>/../ie-setup/INTAKE.md`: look at the saved config, style and presets first, ask only what is
missing, in one batch, every question optional. For a weekly plan:

1. **Posts you can really make this week / عدد المنشورات الواقعي:** 3 · 5 · 7 (plan for that, not more)
2. **Formats / الأشكال:** Reels only · Reels and a carousel · plus Stories
3. **Goal this month / الهدف:** reach · followers · trust · sales
4. **Fixed dates / مواعيد ثابتة:** an event, a launch, a workshop, news to cover
5. **Who posts / من ينشر:** only you · a team (then plan an owner per post)

Skipped answers use the saved defaults. Say what you assumed in one line at the top.

## Inputs, in order of trust

1. `<settings>/config.md`: topic, audience, voice, platforms.
2. `/ie-audit` results the user has shared, or `<settings>/log.md`:
   what actually worked for this account.
3. `<settings>/swipe.md` from `/ie-viral`: what works in the niche.
4. Defaults below, only for what 1-3 do not cover.

If 2 and 3 are both missing, say so in one line: the plan is a starting
guess until there is evidence.

## Shape of a week

- **Content pillars:** 3, from the config. For a security-awareness account,
  for example: protect yourself (how-tos), know the scam (warnings),
  news in your field, explained (`/ie-news`).
- **Formats:** mostly Reels for reach, one carousel for saves, Stories every
  posting day for conversation.
- **One idea per post.** If two posts in the week share a hook formula, change
  one of them.
- **Recycling is allowed:** a post that hit 3x the account median deserves a
  new angle within a month (`/ie-repurpose`).

## Output

A table the user can follow, and the same table written to
`<settings>/plan.md` so the other skills can read it:

| day | format | pillar | idea | formula | hook draft | owner |
| --- | --- | --- | --- | --- | --- | --- |
| Sun | Reel | know the scam | fake copyright DM | #1 الثغرة | ... | me |
| ... | | | | | | |

Under the table, one line: what this week tests ("Does formula #3 beat #10 for
this audience?"), so next week's `/ie-audit` has a question to answer.

Nothing is scheduled or posted by this skill.
