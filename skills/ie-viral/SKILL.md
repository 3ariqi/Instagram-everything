---
name: ie-viral
description: >-
  Research what is working right now in the user's niche: collect Reels from a
  handful of accounts, rank each by how far it beat its own account's normal,
  name the hook formula, and build a swipe file in Arabic or English. Use when
  the user says "what's working", "find viral videos", "ابحث عن الفيديوهات
  الناجحة", "وش ينجح في مجالي", "حلل هذا الحساب", "swipe file", or has no
  evidence for what to make next.
---

# ie-viral

The research skill. Everything else writes; this one looks. Run it monthly:
formulas last a season.

**Files and language:** follow `<base>/../ie-setup/WORKSPACE.md`: read settings from the workspace, save the result in this skill's folder there, and use the language the user chose.

## The one idea

**Raw views are not evidence.** 400,000 views on a 2-million-follower account
is a quiet day; on a 4,000-follower account it is a discovery. Everything here
ranks on the **outlier multiple**: views divided by that account's own recent
median. Above 3x is a signal. Below 1.5x teaches nothing.

Prefer accounts within about 10x of the user's own size, and accounts in the
user's language: an Arabic hook that works is worth more to an Arabic account
than an English one.

## Step 1: pick 6 to 12 accounts (ask, or propose and get approval)

- 4 direct: same topic, slightly ahead.
- 4 adjacent: different topic, same audience.
- 2 to 4 bigger accounts, for format only.

Also ask the user to open their own Saved collection: it is already filtered by
their taste.

## Step 2: look, carefully

Use the browsing tool this session has, with the user present.

**Rules that are not negotiable:**

- **Never log in on the user's behalf and never ask for a password.** If a page
  needs a login, the user is the one who is logged in, driving their own
  browser, or they paste what they see.
- **Reading, not scraping.** Ten accounts, a dozen Reels each, at human pace.
  Do not build a crawler, do not use a scraping service, do not loop this in the
  background. Automated collection breaks Instagram's terms and gets accounts
  blocked.
- **Copy the formula, never the video.** The hook shape, structure, length and
  pacing. Not their script, voice or footage. Attribute every row to its
  account.
- **YouTube Shorts** is a fair second source for the same hook patterns: view
  counts are public. Read the pages in the browser the same way. Do not install
  download tools for this.

**What to capture per Reel**, in the creator's own words:

| column | notes |
| --- | --- |
| account | handle |
| followers | from the profile (optional) |
| median | the middle view count of their last ~12 Reels |
| views | this Reel |
| hook | first line, spoken or on screen, exactly as said |
| length | seconds (optional) |

## Step 3: rank

Save as a tab-separated file with a header row, then:

```bash
python3 <base>/../ie-tools/swipe.py captured.tsv --out <settings>/swipe.md
```

It accepts Arabic digits and "48k" / "1.2m" shorthand, computes the outlier
multiple, names the formula (from `data/hooks.json`) and scores each hook.

## Step 4: say what it means, carefully

Three things only:

1. Which formulas over-index in the top third, with counts.
2. What the top third share structurally that the bottom third don't: hook
   length, a visual payoff, movement in the first frame, where the ask sits.
3. The unclassified hooks, read by hand: some are a formula that isn't in
   `hooks.json` yet. Offer to add it.

State the sample size plainly. Forty Reels across six accounts supports a
pattern. Twelve does not.

## Step 5: make it shootable

For the top three formulas, write the user's own version: their story, their
number, in the shape that works. Hand each to `/ie-reel` with the formula
chosen.

Nothing is posted, followed, liked or messaged by this skill. It reads.
