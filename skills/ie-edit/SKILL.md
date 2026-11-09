---
name: ie-edit
description: >-
  Plan the edit (montage) of a Reel or short video in Arabic or English: a
  shot-by-shot cut list with timecodes, on-screen text, captions, sound and an
  export checklist, matched to the user's editing app and experience. Use when
  the user says "edit my reel", "montage", "cut list", "subtitles", "مونتاج",
  "خطة مونتاج", "كيف أقص الفيديو", "ترجمة على الفيديو", "ركّب لي الريل".
---

# ie-edit

Turns a finished script (from `/ie-reel` or the user's own) into an edit plan
someone can follow in any editor. It plans; it does not touch the video.

## Intake (optional questions)

Follow `<base>/../ie-setup/INTAKE.md`. Ask these in one batch, all optional:

1. **Editor / البرنامج:** CapCut · Premiere Pro · DaVinci Resolve · VN · InShot ·
   another · not sure yet
2. **Experience / خبرتك:** first edits · comfortable · professional
3. **Pace / الإيقاع:** fast (a change every 1-2 s) · medium (3-4 s) · calm
4. **Captions / الترجمة على الشاشة:** none · full line · word by word
5. **Sound / الصوت:** voice only · light music under the voice · music and effects
6. **Footage you have / اللقطات المتاحة:** you on camera · screen recordings ·
   B-roll · photos and screenshots

If a script exists, read it. If not, ask for it or offer `/ie-reel` first.

## Tools

```bash
python3 <base>/../ie-tools/beats.py script.txt --target 30   # timing per beat, long shots, loop check
```

Run it on the script first. A beat the tool flags as a long shot (over 4 seconds
with nothing changing) needs a visual change in the edit: a cut, a zoom, a text
card or a screen recording.

## Build the plan

For each beat of the script, one row: time, what is on screen and its source,
the on-screen text (short, in the user's language), the sound, and one note on
the edit. Then the captions plan and the export checklist.

```
EDIT PLAN  ·  30 s  ·  9:16  ·  <editor>  ·  <pace>

#  time     on screen / source        text on screen            sound       note
1  0-3 s    you, close                "كلمة مرورك تسربت؟"       voice       punch-in at 0:01
2  3-9 s    screen recording          the leak-check site       voice       zoom on the red result
3  9-15 s   B-roll / icon cards       3 steps, one per card     voice+tick  new card every 2 s
...

CAPTIONS   <style>, two lines at most, check the Arabic joins and the order of
           mixed Arabic and English words in the preview
SOUND      voice clearly above the music; music lower under speech
END        last beat repeats a word from the first (loop), then the signature card
EXPORT     [ ] 9:16, 1080 x 1920  [ ] cover frame chosen  [ ] captions on
           [ ] no watermark if cross-posting  [ ] checked once on a phone
```

## Rules

- **Say the operation, not the menu.** Use the common names ("split", "speed
  ramp", "keyframe zoom", "auto captions") and tell the user to search that name
  in their editor, because menus change between versions. Never invent a button
  path.
- Match the explanation to the experience level: for a first edit, give three to
  five operations in total and skip effects.
- One change on screen every 2 to 4 seconds, unless the user chose calm.
- Keep text out of the strip at the top and bottom of the frame where the app's
  own buttons and caption sit. Tell the user to confirm on their phone preview.
- Arabic text in editors: check letter joining and word order in the preview
  before exporting, especially where Arabic and English are mixed.
- Music: only music the user has the right to use. Do not suggest ripping a
  track from another video.
- Sizes and limits change. Quote the numbers in `/ie-crosspost` and the beat
  tool, not from memory.
- Hand the caption and hashtags to `/ie-caption`.
