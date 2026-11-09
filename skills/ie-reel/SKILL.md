---
name: ie-reel
description: >-
  Write an Instagram Reel script from an idea, in Arabic or English: scored hook
  options, a timed beat sheet with on-screen text, a clean caption and the
  user's signature. Use when the user says "make a reel", "write a reel about",
  "script for a short video", "ريل عن", "اكتب لي سكربت ريل", "فيديو قصير",
  "hook", "افتتاحية", or hands over a topic for short-form video.
---

# ie-reel

The writing skill the rest of the pack feeds. It produces a script the user can
shoot today, with every claim in it true and every number in it checked.

## Intake (optional questions)

Follow `<base>/../ie-setup/INTAKE.md`: look at the saved config, style and presets first, ask only what is
missing, in one batch, every question optional. For a Reel script:

1. **Goal / الهدف:** warning · how-to steps · news · story · myth-busting
2. **Platform and length / المنصة والمدة:** Reels 15 s · 30 s · 60 s · same script for TikTok and Shorts too
3. **Delivery / طريقة التقديم:** you to camera · voiceover over the screen · text only · two voices
4. **Tone / النبرة:** serious · friendly · sharp · urgent
5. **Language / اللغة:** standard Arabic · my dialect · English
6. **Audience level / مستوى الجمهور:** beginner · average · technical

Skipped answers use the saved defaults. Say what you assumed in one line at the top.

## Tools

The tools live in `ie-tools`, the folder next to this skill's folder. Build
absolute paths from this skill's base directory: `<base>/../ie-tools/`.

```bash
python3 <base>/../ie-tools/hookscore.py hooks.txt         # rank hook options
python3 <base>/../ie-tools/beats.py script.txt --target 30 # time the script
python3 <base>/../ie-tools/clean.py script.txt --report    # strip stock phrasing
```

Formulas are in `<base>/../ie-tools/data/hooks.json` (22 formulas, Arabic and
English, each with a shape and an example).

## Before writing

1. Read `~/.instagram-everything/config.md` if it exists: language, dialect,
   voice, audience, signature. Write in **their** language and register. If
   the file is missing, ask in one question: language/dialect, audience,
   target length. Then go.
2. Read `~/.instagram-everything/swipe.md` if it exists. Formulas that work in the
   user's niche beat the defaults.
3. **Facts.** If the script states a fact about a product, a company, a law, a
   vulnerability, a statistic or a date, it must be checked before it is
   scripted. For anything newsworthy, hand off to `/ie-technews`. Never
   invent a number to make a hook concrete: ask the user for theirs.

## Steps

**1. Pin the one idea.** One Reel, one point. If the user's idea holds three
points, it is three Reels or a carousel. Say so.

**2. Write 5 hook options** from 5 different formulas that fit the idea. Then
score them:

```bash
python3 <base>/../ie-tools/hookscore.py hooks.txt
```

Show the user the ranking. If the top hook is under 50, there is no hook yet:
write five more rather than polishing a weak one.

**3. Write the script** on the winning hook, beat by beat, one line per beat,
with timestamps. Spoken language, the way the user talks, in their dialect if
the config says so. For each beat give:

- what is **said**
- what is **on screen** (text card, screen recording, B-roll, face)

The shape that holds attention:

```
0-3s    HOOK       the line, on screen from frame 1 as text too
3-8s    STAKES     why this matters to the viewer, concretely
8-25s   PAYOFF     the steps or the answer, one per beat, each visual
last 3s THE ASK    one action only
last    THE LOOP   echo a word from the hook so the replay feels seamless
```

**4. Time it:**

```bash
python3 <base>/../ie-tools/beats.py script.txt --target 30
```

Fix every flag: a hook past 3 seconds, a beat past 4 seconds with nothing
changing on screen, a beat with more words than its slot.

**5. Clean it:**

```bash
python3 <base>/../ie-tools/clean.py script.txt --report
```

Rewrite any flagged structure by hand. Read the script out loud in your head in
the user's dialect: if a line cannot be said naturally, rewrite it.

**6. Caption** with `/ie-caption` (Job A: the Reel already hooked them).

**7. Signature.** End the script's last on-screen card and the caption with the
signature from the config, exactly as written there.

## Production notes to include

- Most people watch muted at first: every spoken line also appears as on-screen
  text, large, in the upper two-thirds (the bottom is covered by the caption
  and buttons).
- Arabic on-screen text: right-aligned, one idea per card, no more than about
  7 words per card.
- Screen recordings of settings: blur emails, phone numbers, account names and
  anything that identifies a real person.
- For security how-tos: show the real menu path the viewer will see, and say
  it may differ slightly by app version.

## Output

```
HOOKS (ranked)
  86  #3 لا أحد يخبرك   لا أحد يخبرك أن كلمة مرورك تسربت
  ...

SCRIPT  ·  28s  ·  formula #3
0:00  [قول]  لا أحد يخبرك أن كلمة مرورك تسربت
      [شاشة] نص كبير: كلمة مرورك تسربت؟
0:03  ...

CAPTION
...
<signature>

CHECKS  hook 86 · beats OK · natural 82 PASS
```

When the user approves, append one line to `~/.instagram-everything/log.md`: date,
topic, formula id, hook line. `/ie-audit` uses this later.

## Boundaries

This skill writes. It never posts, uploads or schedules anything. The user
shoots and publishes.
