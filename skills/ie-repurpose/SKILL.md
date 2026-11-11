---
name: ie-repurpose
description: >-
  Turn one long piece (a workshop, a YouTube video, an article, a thread, a
  talk) into several Instagram posts, each with its own angle and hook, in
  Arabic or English. Use when the user says "repurpose", "turn this into
  posts", "حول هذا لمحتوى", "قسم الفيديو لريلز", "من الورشة اعمل منشورات", or
  pastes a transcript or article.
---

# ie-repurpose

One source, several posts, each standing alone. The mistake is cutting the
source into pieces; the goal is finding the separate ideas inside it.

**Files and language:** follow `<base>/../ie-setup/WORKSPACE.md`: read settings from the workspace, save the result in this skill's folder there, and use the language the user chose.

## Input

A transcript, an article, slides, or notes. If it's a video, ask for the
transcript (YouTube's auto-transcript is fine) rather than downloading anything.

## Steps

1. **Find the ideas.** List every self-contained idea in the source: a claim
   with its proof, a story with its lesson, a how-to, a surprising number, a
   common mistake, a strong quote. Usually 5 to 12.
2. **Rank them** by how much a stranger would care, not by how much time the
   source spent on them.
3. **Assign a format to each:**
   - a single point with a visual payoff → Reel (`/ie-reel`)
   - steps or a checklist → carousel (`/ie-carousel`)
   - a question to the audience → Story with a poll or quiz (`/ie-story`)
   - a strong quote → a single image with the quote, credited
4. **Give each a different hook formula.** Five posts from one source with
   the same hook shape reads as a content mill.
5. **Check facts again.** Anything from the source that is a fact still gets
   checked if the source is old: numbers, product names and menus change.

## Rules

- Quotes from other people are attributed, word for word, and short.
- Never repurpose someone else's video as if it were the user's. Repurposing
  is for the user's own material, or for commentary that adds a clear new angle
  and credits the original.
- Space the posts out: one source, at most two or three posts a week.

## Output

```
SOURCE  workshop "حماية الحسابات" · 52 min · 9 ideas found

#  idea                                    format    formula        week
1  SMS codes can be hijacked via SIM swap  Reel      #8 الخرافة     1
2  The 5-minute account check              Carousel  #10 القائمة    1
3  "Which 2FA do you use?"                 Story     poll           1
...
```

Then write each piece with its skill, on the user's go-ahead.
