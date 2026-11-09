---
name: ie-crosspost
description: >-
  Adapt one Instagram post for TikTok, YouTube Shorts and X, respecting each
  platform's limits and habits, in Arabic or English. Use when the user says
  "post this everywhere", "adapt for TikTok", "انشره في كل المنصات", "نسخة
  لتيك توك", "نسخة لتويتر", "Shorts", or works across platforms.
---

# ie-crosspost

Same idea, different room. The video can often stay the same; the text around
it should not.

Read `~/.claude/instagram/config.md` for the handles on each platform and the
signature. Run all text through `<base>/../ie-tools/clean.py`.

## Before you adapt

Platform limits change. Before relying on a number below for a post that
matters, check the platform's own help page and note the date you checked.
The figures here were checked in November 2026.

## Per platform

**Instagram Reels** (the source)
Caption up to 2,200 characters, about 125 visible before "more", 5 hashtags at
most, links not clickable in captions.

**TikTok**
- Re-export the video **without** the Instagram watermark or on-screen handle.
- First line of the description works like a hook: TikTok search reads it, so
  put the keyword people would search for in it.
- On-screen text can be added in TikTok itself so it uses native styling.
- A few hashtags that describe the topic; trend tags only if truly relevant.

**YouTube Shorts**
- Shorts can be up to 3 minutes; keep the Reel's length unless the extra time
  carries real content.
- **Title** matters: under ~60 characters, searchable words first, in the
  language people search in. ("كيف تعرف إذا انسرق حسابك في إنستقرام")
- Description: the source links (clickable here), and the signature.

**X (Twitter)**
- A post is short (280 characters for standard accounts, longer for paid
  ones). Arabic text counts per character the same way.
- Lead with the claim, not "new video". The video attached plays inline.
- For how-tos, a thread works better than a clip alone: hook post with the
  video, then one step per reply, sources in the last reply.

## Rules

- Never copy Instagram hashtags blindly to other platforms.
- Never post a watermarked export from one platform on another.
- Same facts, same sources everywhere. If you correct a mistake on one
  platform, correct it on all.
- The signature fits each platform: handle names can differ per platform.

## Output

```
INSTAGRAM   caption (unchanged, already linted)
TIKTOK      description: ...         (keyword: "سرقة حساب انستقرام")
SHORTS      title: ...  (54 chars)   description: ... + sources
X           post: ... (231/280)     thread: 4 replies
CHECKLIST   [ ] export without watermark  [ ] captions burned in  [ ] cover frame chosen
```

The user publishes on each platform. Nothing is posted by this skill.
