---
name: ie-natural
description: >-
  Clean any draft so it reads like a person wrote it, in Arabic or English:
  remove stock phrases, fix Arabic punctuation, strip stray invisible
  characters while keeping emoji intact, then score how natural it reads. Use
  before any caption, script, comment, reply or DM goes out, or when the user
  says "this sounds robotic", "اجعله طبيعي", "النص يبدو آلي", "نظف النص",
  "humanize", "de-slop".
---

# ie-natural

Captions are short and scripts are said out loud, so one template phrase is a
bigger share of the text than it would be in an essay. The tell is not a
detector; it is a viewer scrolling past something that sounds like a brochure.

## Tools

In `<base>/../ie-tools/`:

```bash
python3 <base>/../ie-tools/clean.py draft.txt -o clean.txt --report
python3 <base>/../ie-tools/score.py draft.txt clean.txt
```

Both use `data/stock_phrases.json`: Arabic and English stock phrases, each set
to `replace` (fixed automatically) or `flag` (reported only). It is meant to be
edited: if the user genuinely says a phrase, remove its entry.

## What `clean.py` fixes automatically

1. **Invisible characters** with no place in a caption: zero-width spaces, word
   joiners, stray byte-order marks, soft hyphens, bidi override characters.
   It **keeps** the joiner inside emoji like 👨‍💻, flag sequences, and direction
   marks that mixed Arabic/English text needs.
2. **Punctuation by language.** In Arabic lines: «،» «؛» «؟» instead of
   Latin marks, the em dash turned into «،». In English lines: em dash to
   comma, curly quotes to straight. URLs, @handles and #hashtags are never
   touched.
3. **Stock phrases** marked `replace`: «في عالمنا المتسارع»، «تجدر الإشارة إلى
   أن»، «علاوة على ذلك»، "delve into", "leverage", "in today's fast-paced
   world" and more. Diacritics and letter variants don't hide a phrase from it.

## What it only flags (your job)

- «ليس مجرد... بل»، "it's not X, it's Y", "not only... but also"
- One-word rhetorical questions: «والنتيجة؟», "The result?"
- Video preambles and greetings: «في هذا الفيديو سأشرح»، «مرحباً بكم»
- Engagement bait: «لا تنسى المتابعة»، «منشن صديقك»، "follow for more"
- More than 5 hashtags, emoji-bullet lists, runs of shouted words

Rewrite each flagged line by hand, keeping the meaning, in the user's dialect.

## The five checks in `score.py`

| check | measures |
| --- | --- |
| VARIETY / تنوّع الجمل | sentence lengths vary like speech |
| SPECIFICS / التفاصيل | numbers, names, times, places |
| STOCK / العبارات الجاهزة | stock-phrase density |
| TYPOGRAPHY / الترقيم والأحرف | stray invisible characters, em dashes, Latin punctuation in Arabic |
| VOICE / الصوت البشري | I/we and you, colloquial forms, no staged structures |

PASS: overall 70+ with no check under 55.

## Be honest about what this is

These are local writing checks. They run on the user's machine, upload
nothing, and are **not** an AI detector. Passing them does not promise any
detector's verdict, and the goal is not to hide anything: it is writing people
want to read. Do not describe a text as "undetectable": no one can promise that.

## Order

1. `clean.py draft.txt -o clean.txt --report`
2. Rewrite the flagged lines by hand.
3. `score.py draft.txt clean.txt` to show before and after.
4. If not PASS, fix the weakest check and run again. Two rounds is normal; if
   five rounds don't get there, write a new draft instead.
5. Show the cleaned text and the score together, never the score alone.
