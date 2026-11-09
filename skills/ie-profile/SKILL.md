---
name: ie-profile
description: >-
  Score an Instagram profile and rewrite what converts visitors into followers:
  name field, bio, link, highlights and pinned posts, in Arabic or English. Use
  when the user says "fix my bio", "audit my profile", "البايو", "حسن حسابي",
  "الوصف", "highlights", "الهايلايت", or gets views but no follows.
---

# ie-profile

A Reel brings a stranger to the profile. The profile has about three seconds
to answer three questions: who is this, what will I get, why follow now. Views
with no follows is a profile problem, not a content problem.

Read `~/.instagram-everything/config.md` first. Run all rewritten text through
`<base>/../ie-tools/clean.py`.

## Input

A screenshot of the profile, or the pasted name field, bio, link and the titles
of highlights and pinned posts. Do not browse to the profile with a tool unless
the user asks and is present.

## Facts

- The bio holds 150 characters.
- The **name field** is searchable, so it can carry a keyword next to the name
  ("أحمد طاهر | أمن رقمي").

## Score (0-10 each, show the working)

| element | 10 looks like |
| --- | --- |
| Name field | name + the topic people would search for |
| Bio line 1 | what the follower gets, in their words, not a job title |
| Bio line 2 | proof: a number, a credential, a result |
| Bio line 3 | the one action, pointing at the link |
| Link | one clear destination, named in the bio |
| Profile photo | a face or a mark readable at thumbnail size |
| Highlights | 3-5, named by what's inside ("ابدأ هنا", "احمِ حسابك") |
| Pinned posts | the best proof of value, not the newest post |
| Grid, last 9 | a visitor can tell the topic without reading |

## Rewrites

Give **three bio versions** with different angles (benefit-first,
proof-first, identity-first). Count characters for each; all must fit in 150.

For Arabic bios:

- One idea per line, short lines.
- A line that starts with an @handle or English word aligns left: start
  lines with Arabic.
- Emoji as line markers only if the config allows emoji.

## Security check on the profile (always)

- Public email or phone in the bio? Recommend a contact button or a dedicated
  address instead of a personal one.
- Does the link go through a shortener? Recommend a direct, recognisable domain
  so followers can tell it is really yours.
- Suggest running `/ie-harden` if the account has never been reviewed.

## Output

```
PROFILE SCORE  58 / 90

Name field   4   just the name: add the topic people search for
Bio          ...
...

BIO OPTIONS
A (benefit)  ... (142 chars)
B (proof)    ... (138 chars)
C (identity) ... (121 chars)

PIN  the reel with the highest sends per reach, not the latest
```

The user makes the changes in the app. Nothing is edited by this skill.
