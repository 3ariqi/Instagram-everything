---
name: ie-technews
description: >-
  Turn a tech or security news story into a Reel script and caption in Arabic or
  English, after confirming every claim in three independent sources. Use when
  the user says "tech news", "news reel", "خبر تقني", "اكتب عن هذا الخبر",
  "آخر الأخبار", "breaking", "هل هذا الخبر صحيح", or pastes a link or headline.
---

# ie-technews

A news account lives on one thing: being right and being early, in that order.
A wrong story posted fast costs more trust than ten late right ones earn.

## Intake (optional questions)

Follow `<base>/../ie-setup/INTAKE.md`: look at the saved config, style and presets first, ask only what is
missing, in one batch, every question optional. For a news Reel:

1. **The news / الخبر:** a link, a pasted text, or just the topic
2. **Audience / الجمهور:** general public · beginners · technical readers
3. **Length / المدة:** 30 s · 60 s
4. **Angle / الزاوية:** neutral explainer · warning · what to do now
5. **Sources on screen / المصادر على الشاشة:** yes · no

Skipped answers use the saved defaults. Say what you assumed in one line at the top.

## The rule: three sources, then script

Before any script exists, every factual claim it will contain (who, what, when,
numbers, versions affected, what users should do) must be confirmed in **three
independent sources**, with at least one primary:

- **Primary:** the company's own announcement or blog, the security advisory,
  the official statement, the court filing, the published paper.
- **Independent:** two further outlets that did their own reporting or
  confirmation. Outlets repeating one another's wording, or all citing the
  same single post, count as **one** source.

If a claim has fewer than three, either cut it from the script or label it
plainly: «غير مؤكد بعد» / "unconfirmed so far". Never present an unconfirmed
claim as fact to make the hook stronger.

## Steps

**1. Pin the claim.** Write the story as one sentence with its date. Ask the
user for the link or headline if they have one.

**2. Search properly.** Use web search for the story and open the pages, not
the snippets. Check the date of every page: a story from last year resurfaces
as "breaking" often. State today's date in your searches.

**3. Build the evidence table:**

| claim | source 1 (primary) | source 2 | source 3 | status |
| --- | --- | --- | --- | --- |
| "5M accounts affected" | company statement | outlet A | outlet B | confirmed |
| "passwords were stored in plain text" | outlet A only | — | — | unconfirmed: cut |

Show this table to the user before the script. It is what lets them defend the
post when someone challenges it.

**4. Find the "so what".** The viewer cares about one thing: *does this affect
me, and what do I do?* Lead with the effect on them, and end with the action
(update, change a setting, check a site). If there is no action, ask whether
it is worth a Reel.

**5. Write the Reel** with `/ie-reel` in the user's language and dialect. Use
formula #2 (Breaking) or #1 (The Breach). Then:

- Put the source on screen at the moment of the claim: «المصدر: بيان الشركة».
- Say the date: «أعلنت الشركة يوم ...».
- Name what is still unknown: «لم تؤكد الشركة بعد ...».

**6. Caption** with `/ie-caption`: a **Sources** line with the primary source
and the two others, by name. Links are not clickable in captions, so name the
outlets, and put the link in the bio or a Story link sticker.

**7. Correct in public.** If a source later corrects the story, post the
correction on the same channels. Say so: «تحديث: تبيّن أن ...».

## Cautions

- **Security stories:** never include steps that help someone attack. Explain
  what happened and how to defend.
- **Do not name or accuse a private individual** from a news item. Cite what
  the source says, about organisations and public facts.
- **Numbers:** write the number as the primary source gives it, with its unit
  and date. Don't round up for effect.
- **Politics and conflict:** attribute every contested claim to its source
  rather than stating it as fact.
- **Rumours and screenshots:** a tweet or a screenshot is not a source. It is a
  lead to chase.

## Output

```
STORY   One sentence, dated.
TABLE   claim | 3 sources | status
SCRIPT  hook · beats · on-screen source cards   (-> /ie-reel)
CAPTION sources line + signature                (-> /ie-caption)
CUT     claims left out and why
```

Hand the user the table with the script. They decide whether to post.
