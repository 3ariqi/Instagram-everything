---
name: ie-story
description: >-
  Plan an Instagram Story sequence in Arabic or English, frame by frame, with
  the interactive stickers that turn viewers into replies and DMs. Use when the
  user says "stories", "story sequence", "ستوري", "ستوريات", "what do I post on
  my story", "poll", "quiz", "استفتاء", "اسئلة", or wants to warm up followers
  before a post or a launch.
---

# ie-story

Stories reach people who already follow. Their job is not reach, it is
conversation: replies, poll votes and DMs, which is where trust is built.

Read `~/.instagram-everything/config.md` first. Use `clean.py` from
`<base>/../ie-tools/` on all on-screen text.

## Intake (optional questions)

Follow `<base>/../ie-setup/INTAKE.md`: look at the saved config, style and presets first, ask only what is
missing, in one batch, every question optional. For a Story sequence:

1. **Goal / الهدف:** start a conversation · teach one thing · point to a post · behind the scenes
2. **Frames / عدد اللقطات:** 3 · 5 · 7
3. **Sticker / الملصق التفاعلي:** poll · quiz · slider · question box · none
4. **On camera or text / الشكل:** you on camera · text and images only

Skipped answers use the saved defaults. Say what you assumed in one line at the top.

## The sequence

3 to 7 frames, one story arc:

```
1  OPEN      a question or a moment, never "hello"
2  CONTEXT   what happened / what you found
3  TOUCH     an interactive sticker: poll, quiz, slider or question box
4  VALUE     the answer, the tip, the screenshot
5  NEXT      where to go: the new post, the bio link sticker, or "reply to me"
```

## Stickers, and what each one is for

| sticker | use it to |
| --- | --- |
| Poll | split the audience on a real choice ("أي تطبيق مراسلة تستخدم؟") |
| Quiz | test a belief your content corrects; reveal the answer next frame |
| Question box | collect the questions your next Reel answers |
| Slider | gauge feeling ("كم تثق بكلمة مرورك؟") |
| Link | send people to one destination; say in text where it goes |

The answers are content. A question asked by thirty people is a Reel
(`/ie-reel`, formula #16, comment reply).

## Rules

- **Text in the middle band.** The top and bottom of a Story are covered by the
  account name, the progress bar and the reply box.
- **One sticker per frame**, and not on the first frame.
- **Readable in under 3 seconds** per frame, or the viewer taps past it.
- **Security stories:** never show a real person's handle, number or message
  without blurring it, including scam messages you are warning about.
- **Link stickers:** only to destinations you would vouch for. Write the domain
  in the text so viewers know where they are going before they tap.

## Output

```
STORY  ·  5 frames

1  [photo of phone, red notification]
   «وصلتني هذي الرسالة اليوم 👇»
2  [blurred scam DM screenshot]
   «لاحظ الرابط»
3  [Quiz] «هل الرابط رسمي؟»  نعم / لا ✔
4  «الرابط ليس من إنستقرام. الرسائل الرسمية تظهر داخل التطبيق»
5  [Link sticker to the new Reel] «الشرح الكامل هنا»
```

Nothing is posted by this skill.
