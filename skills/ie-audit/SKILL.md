---
name: ie-audit
description: >-
  Post-mortem on what the user already posted: which posts really worked, why,
  and what to stop making, ranked by outlier multiple and shares, not raw
  views. Use when the user pastes Instagram insights or asks "what's working",
  "why did this flop", "حلل أدائي", "ليش ما نجح الفيديو", "audit my content",
  "read my analytics".
---

# ie-audit

The only honest evidence for what works on an account is that account's own
last 20 to 30 posts. Every rule in every guide, this pack included, is a guess
until the account's numbers agree.

## Input

Whatever the user has, screenshots are fine:

- Per post: views, reach, likes, comments, saves, shares, follows, and the
  share of reach from non-followers.
- The retention graph of the best and worst recent Reels: one screenshot here
  says more than the rest combined.
- Or just the posts and their view counts, which is enough for a first pass.

Also read `~/.instagram-everything/log.md` if it exists: it records the hook
formula each post used.

**How the numbers get here.** The user opens Instagram's own Insights
(professional accounts) or each post's "View insights", and pastes the figures,
exports them, or sends screenshots. This skill never logs in, never asks for a
password, a login code or an access token, and never scrapes. If the user's
agent has a data connector they authorised themselves, they can paste its
output here like any other export.

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
