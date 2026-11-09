---
name: ie-carousel
description: >-
  Plan an Instagram carousel slide by slide in Arabic or English: cover, one
  idea per slide, recap and a single ask, with on-slide text sized to be read
  on a phone. Use when the user says "carousel", "slides post", "كاروسيل",
  "منشور شرائح", "بوست سحب", "swipe post", or wants a step-by-step or checklist
  post.
---

# ie-carousel

A carousel is the format people save. Saves come from reference value: a
checklist, steps, a comparison they will need again. Write it for the second
time they open it, not only the first.

## Intake (optional questions)

Follow `<base>/../ie-setup/INTAKE.md`: look at the saved config, style and presets first, ask only what is
missing, in one batch, every question optional. For a carousel:

1. **Shape / الشكل:** list · myth versus fact · step by step · story
2. **Slides / عدد الشرائح:** 5 · 8 · 10
3. **Goal / الهدف:** saves · shares
4. **Text per slide / كثافة النص:** light · medium · dense
5. **Cover / الغلاف:** a question · a number · a bold claim
6. **Language / اللغة:** from the config, or different for this one

Skipped answers use the saved defaults. Say what you assumed in one line at the top.

## Tools

`<base>/../ie-tools/` next to this skill's folder: `hookscore.py` for the
cover line, `clean.py` for all slide text, `caption.py` for the caption.
Read `~/.instagram-everything/config.md` first.

## Platform facts

- A carousel holds up to 20 photos or videos (since August 2024).
- Portrait 4:5 (1080 × 1350 px) is the safe default size for feed posts.
- The profile grid crops previews, so keep the cover's text centred.

## Structure

```
1        COVER     the hook. Six words or fewer, readable as a thumbnail.
2        STAKES    why this matters to the reader, with a number if possible
3..n-2   ONE IDEA PER SLIDE   a heading of 3-6 words + 1-2 short lines
n-1      RECAP     the whole carousel on one slide: the one people screenshot
n        ASK       one action, plus the signature
```

Aim for 6 to 10 slides. More only when each slide earns its place: twenty
thin slides lose people at slide five.

## Writing rules

- **Cover:** score it with `hookscore.py --hook "..."`. Under 50 means rewrite.
- **Each slide must make sense alone**, because people land on slide 4 from a
  share.
- **Swipe cue direction:** before publishing, open a draft on a phone set to
  the audience's app language and check which way the carousel advances, then
  point the arrow that way. Number slides «١/٨» or «1/8», consistently.
- **Text size:** if a line does not fit at a size readable on a phone without
  zooming, cut words, not font size.
- **Screenshots of settings:** blur personal data. Mark the exact button with a
  circle or arrow. Mention that menus can differ slightly between app versions.
- **Every factual slide has a source** on the recap slide or in the caption.
- Run `clean.py` over all slide text together before handing it over.

## Output

```
CAROUSEL  ·  8 slides  ·  4:5

1  COVER    "٣ إعدادات تحمي حسابك الليلة"            hook 81
            visual: phone mockup, red lock
2  STAKES   "حساب يُسرق كل ..."  (needs the user's number or a sourced one)
3  ...
7  RECAP    the three settings in one list
8  ASK      احفظ المنشور للرجوع له
            <signature>

CAPTION  -> /ie-caption, Job B
```

Nothing is designed or uploaded by this skill: it hands over the text and the
layout notes. The user builds the slides in their design tool and posts them.
