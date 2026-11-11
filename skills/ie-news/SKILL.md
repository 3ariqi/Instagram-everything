---
name: ie-news
description: >-
  Turn a news story from any field (tech, religious, political, social, health,
  business, sport, local...) into a Reel script and caption in Arabic or
  English, in the user's voice and for their audience, after confirming every
  claim in three independent sources. Use when the user says "write about this
  news", "news reel", "اكتب عن هذا الخبر", "خبر", "آخر الأخبار", "عاجل",
  "breaking", "هل هذا الخبر صحيح", or pastes a link or a headline.
---

# ie-news

Any account that covers news lives on one thing: being right and being early, in that order.
A wrong story posted fast costs more trust than ten late right ones earn.

**Field:** this skill works for every field. Read the user's `Field:` in
`config.md` and apply its section of `<base>/../ie-setup/NICHES.md`: which
sources count as primary there, what tone the audience expects, and the red
lines. A religious account, a political commentator and a tech channel writing
about the same day's news produce three very different Reels.

**Files and language:** follow `<base>/../ie-setup/WORKSPACE.md`: read settings from the workspace, save the result in this skill's folder there, and use the language the user chose.

## Intake (optional questions)

Follow `<base>/../ie-setup/INTAKE.md`: look at the saved config, style and presets first, ask only what is
missing, in one batch, every question optional. For a news Reel:

1. **The news / الخبر:** a link, a pasted text, or just the topic
2. **Field / المجال** (only if not saved): tech · religious · political · social · health · business · other
3. **Angle / الزاوية:** neutral report · explainer · your opinion on it · warning · what to do now
4. **Audience / الجمهور:** general public · followers who know the topic · specialists
5. **Length / المدة:** 30 s · 60 s · 90 s
6. **Sources on screen / المصادر على الشاشة:** yes · no

Skipped answers use the saved defaults. Say what you assumed in one line at the top.

## The rule: three sources, then script

Before any script exists, every factual claim it will contain (who, what, when,
numbers, versions affected, what users should do) must be confirmed in **three
independent sources**, with at least one primary:

- **Primary:** the first-hand source for this field (see `NICHES.md`): the
  company's announcement or the security advisory (tech), the institution's or
  scholar's own statement (religious), the official statement, the text of the
  law or the court filing (political), the original poster and confirmation
  from the people involved (social), the ministry or the study (health).
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

**4. Find the "so what" for this audience.** Ask what this news means to the
user's followers specifically: what changes for them, what they should know,
think or do. A tech audience wants the action (update, change a setting); a
religious audience may want the ruling or the lesson with its source; a
political audience wants what it means and who said what; a social audience
wants the human story and how to help. If the user chose "your opinion",
state the facts first with sources, then the user's view, clearly marked as
theirs. If the news means nothing to this audience, ask whether it is worth a Reel.

**5. Write the Reel** with `/ie-reel` in the user's language, dialect and
register for their field. A breaking-news formula suits most fields; for
religious or social stories a story-led or question hook often fits better.
Then:

- Put the source on screen at the moment of the claim: «المصدر: بيان الشركة».
- Say the date: «أعلنت الشركة يوم ...».
- Name what is still unknown: «لم تؤكد الشركة بعد ...».

**6. Caption** with `/ie-caption`: a **Sources** line with the primary source
and the two others, by name. Links are not clickable in captions, so name the
outlets, and put the link in the bio or a Story link sticker.

**7. Correct in public.** If a source later corrects the story, post the
correction on the same channels. Say so: «تحديث: تبيّن أن ...».

## Cautions

- **The field's red lines** in `NICHES.md` apply on top of these.
- **Security stories:** never include steps that help someone attack. Explain
  what happened and how to defend.
- **Do not name or accuse a private individual** from a news item. Cite what
  the source says, about organisations and public facts.
- **Numbers:** write the number as the primary source gives it, with its unit
  and date. Don't round up for effect.
- **Politics, religion and conflict:** attribute every contested claim to its
  source rather than stating it as fact; keep the user's opinion, labelled as theirs.
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
