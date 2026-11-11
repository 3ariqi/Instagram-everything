---
name: ie-audit
description: >-
  Post-mortem on what the user already posted: which posts really worked, why,
  and what to stop making, ranked by outlier multiple and shares, not raw
  views, from screenshots the user attaches or, if they allow it, by reading
  their own Insights in their browser. Use when the user pastes Instagram
  insights or asks "what's working",
  "why did this flop", "حلل أدائي", "ليش ما نجح الفيديو", "audit my content",
  "read my analytics".
---

# ie-audit

The only honest evidence for what works on an account is that account's own
last 20 to 30 posts. Every rule in every guide, this pack included, is a guess
until the account's numbers agree.

**Files and language:** follow `<base>/../ie-setup/WORKSPACE.md`: read settings from the workspace, save the result in this skill's folder there, and use the language the user chose.

**Autopilot first:** if `<settings>/autopilot.md` exists and the user is
reporting that planned posts went out (or should be skipped), update the queue
first as `ie-autopilot` follow-up mode says (mark posted, measured or skipped,
add the numbers to `log.md`). Then audit, if there is enough to compare.

## Two ways to get the numbers: the user chooses

Ask once, in the user's language, and do whichever they pick:

> كيف تحب أعطيك أرقامك؟
> 1. أرفق لقطات شاشة أو ملف تصدير من «رؤى» (Insights)
> 2. أتصفح أنا صفحة «رؤى» حسابك من متصفحك وأنت مسجّل الدخول، للقراءة فقط

**Option 1: screenshots or an export.** Whatever the user has is fine:

- Per post: views, reach, likes, comments, saves, shares, follows, and the
  share of reach from non-followers.
- The retention graph of the best and worst recent Reels: one screenshot here
  says more than the rest combined.
- Or just the posts and their view counts, which is enough for a first pass.

Point them to their workspace's `inbox` folder: they can drop the files there
and you read them from it.

**Option 2: you browse, with their permission.** Only if this agent has a
browser it can drive (a browser extension, a built-in browser, computer use).
If it has none, say so in one line and fall back to option 1.

1. **The user signs in, not you.** Ask them to open Instagram (web) in that
   browser and sign in themselves. Never type, ask for, read aloud or store a
   password, a login or 2FA code, or a recovery code, even if they offer it.
   At any login, 2FA or "confirm it's you" screen, stop and let them do it.
2. **Read only.** Open their own profile, the professional dashboard or
   Insights, and each recent post's "View insights". Never click follow, like,
   comment, post, delete, archive, message, or change any setting. If a page
   asks you to accept or confirm anything, stop and ask the user.
3. **Their account only, at a human pace.** About 20 to 30 recent posts, one at
   a time. No other accounts in this step, no loops, no scraping tools,
   nothing left running after the task. Say plainly that automated collection
   is against Instagram's terms and heavy browsing can get an account
   rate-limited, which is why you keep it short.
4. **Write down what you read** in a table (date, format, views, reach,
   saves, shares, follows, non-follower share) and show it to the user before
   analysing, so they can correct a misread number.
5. **Close what you opened** and tell them they can sign out if they want.

A data connector the user authorised themselves in their agent (an analytics
connector, for example) counts as option 2 without the browser: use its read
functions only, never its write functions, and show the table the same way.

Either way, also read `<settings>/log.md` if it exists: it records the hook
formula each post used.

## What to compute, showing the working

| metric | how | tells you |
| --- | --- | --- |
| Outlier multiple | views / the account's median views | a real hit or a normal day |
| Non-follower reach | % of reach from non-followers | whether it travelled |
| Hold at 3s | viewers still watching at 3s, from the retention graph | whether the hook worked |
| Shares per reach | shares / reach | the strongest signal: someone put their name on it |
| Saves per reach | saves / reach | reference value (carousels, how-tos) |
| Follows per reach | follows / reach | whether the profile converted |

Rank by outlier multiple and shares per reach, never by raw views.

## Find the pattern

Put the top five and bottom five side by side and look for what separates them:

- **Hold at 3 seconds.** If top and bottom differ here, it is the hook.
- **Hook formula** (ids from `ie-tools/data/hooks.json`). Run
  `python3 <base>/../ie-tools/hookscore.py` over the hooks of both groups.
- **Format and length.** Under 15s, 15-30s, 30-60s, over 60s.
- **Pillar / topic.** For security accounts: warnings, how-tos, news.
- **Whether the user replied to comments in the first hour.**
- **Day and time, last,** and only if nothing else explains it.

State each finding as a claim with its evidence and the confidence. With 30
posts a pattern can show. With 6 it cannot, and saying so beats inventing one.

## The distinction that saves months

**Views and no follows is a profile problem** (`/ie-profile`). **No views is a
hook problem.** Separate the two before recommending anything.

## Output

```
AUDIT  ·  28 posts  ·  median 3,900 views

TOP 5 BY OUTLIER MULTIPLE
  14.1x  #1 الثغرة       55,000 views  61% non-follower  hold@3s 68%  210 shares
  ...
BOTTOM 5
  0.3x   #13 لماذا        1,100 views   7% non-follower  hold@3s 29%    1 share

WHAT THE DATA SAYS
1. Hold at 3s is the whole story: top five average 66%, bottom five 31%.
2. Scam warnings with a real (blurred) message on screen: 9.2x vs 1.1x. n=6.
3. ...

STOP:     general "tips" with no concrete case
DO MORE:  real scam examples, explained in under 30 seconds
```

Then hand the conclusions to `/ie-plan` for next week, and to `/ie-viral` to
filter the swipe file to what works for this account.
