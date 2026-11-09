---
name: ie-caption
description: >-
  Write or fix an Instagram caption in Arabic or English, cut at the right place
  before "more", with one ask, five hashtags at most and the user's signature,
  then lint it. Use when the user says "caption", "write a caption", "كابشن",
  "اكتب وصف للمنشور", "نص المنشور", "hashtags", "هاشتاقات", or pastes a caption
  to improve.
---

# ie-caption

## Tools

`<base>/../ie-tools/` next to this skill's folder:

```bash
python3 <base>/../ie-tools/caption.py caption.txt --signature "<signature from config>"
python3 <base>/../ie-tools/clean.py caption.txt --report
```

Read `~/.claude/instagram/config.md` first for language, voice and signature.

## Platform facts this skill relies on

- A caption holds up to 2,200 characters.
- The feed shows roughly the first 125 characters before "more".
- Five hashtags per post at most (Instagram's limit since December 2025).
- Links in captions are not clickable.

## Two jobs, so ask which one

**Job A: a Reel already hooked them.** The video did the work in its first
seconds. The caption adds what the video could not: the steps written out, the
source, the detail people want to save. Line one should still earn the tap on
"more", but it is not a second hook.

**Job B: a photo or carousel.** The caption's first line *is* the hook, and it
works like a Reel hook: concrete, short, cut on a cliff. Write it with a
formula from `<base>/../ie-tools/data/hooks.json` and score it with
`hookscore.py --hook`.

## Rules

- **The first ~125 characters are the caption** for most people. They must
  make sense alone and stop at a point that makes the reader tap. Never let
  the cut land mid-word.
- **No greeting, no preamble** in line one.
- **One ask.** Save, or comment, or follow, or share: pick the one that fits
  the post. The signature's follow line does not count as a second ask.
- **Hashtags: 3 to 5, specific, at the end.** Mix one broad tag with niche
  ones in the audience's language (#أمن_رقمي, #حماية_البيانات). Never in the
  first line.
- **Arabic lines that start with an @handle or an English word align left**
  in the app and break the right-to-left flow. Start the line with an Arabic
  word: «تابعنا على @3ariqi» not «@3ariqi تابعنا».
- **Use Arabic punctuation in Arabic** (، ؛ ؟). `clean.py` fixes it.
- **No links in the body.** Say where the link is: "the link is in the bio".
- **Sources.** If the caption states a fact, name the source in the caption
  ("المصدر: بيان شركة ميتا، 19 ديسمبر 2025").
- **Signature last**, exactly as in the config, then hashtags after it or
  before it as the user prefers (ask once, save the answer to the config).

## Steps

1. Ask which job, unless it is obvious.
2. Write the caption.
3. Run `clean.py --report`, then rewrite flagged structures by hand.
4. Run `caption.py --signature "..."` and fix every X and ! line.
5. Show the user the visible part on its own first, then the full caption.

## Output

```
VISIBLE BEFORE "MORE"
  <first ~125 characters>

FULL CAPTION
  ...
  <signature>
  #tag1 #tag2 #tag3

CHECKS  1,040 / 2,200 chars · 3 / 5 hashtags · 1 ask · OK
```

## Boundaries

Writes text only. Never posts.
