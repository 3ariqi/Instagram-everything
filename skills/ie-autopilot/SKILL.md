---
name: ie-autopilot
description: >-
  Learns the user's whole content routine once (what to prepare, from which
  plan, in which order, when, and what they review), then runs it by itself on
  a schedule: prepares every post due from the weekly plan, keeps a queue, flags
  what is late, asks for the numbers after posting and drafts next week's plan.
  Never posts. Use when the user says "autopilot", "automate this", "run it by
  itself", "schedule", "الطيار الآلي", "شغّلها تلقائياً", "جدولة", "خلها تشتغل
  لحالها", "ماذا جهزت", "what's ready", when they report a planned post as
  published or skipped ("I posted", "skip it", "نشرت", "نشرته", "تخطّه",
  "اعتمد"), with or without its numbers, or when a scheduled task runs
  "/ie-autopilot run".
---

# ie-autopilot

Three modes. Pick one from what the user said, or from the prompt of a scheduled
run.

| Mode | When | What it does |
| --- | --- | --- |
| **learn** | first time, or "change my routine" | learns the routine and saves it, then sets up the schedule |
| **run** | a scheduled task fires, or "prepare what's due" | prepares, tracks and reports, with nobody there to answer |
| **follow-up** | "what's ready?", "I posted it", "pause" | shows the queue and updates it |

**Files and language:** follow `<base>/../ie-setup/WORKSPACE.md`. The routine is
`<settings>/autopilot.md`, the queue is `<settings>/queue.json`, the plan is
`<settings>/plan.md`. Packages go to the `ready` folder. `<tool>` below means
`python3 <base>/../ie-tools/autopilot.py`.

## The hard limits (all modes)

- **Nothing is published.** No post, story, comment, reply or DM is sent, and
  nothing is scheduled inside Instagram or any other platform. The user posts.
- No login, no password, code or token, no browsing the user's accounts. A run
  reads only files: settings, the plan, and what the user put in the `inbox` folder.
- Web access only for `ie-news` source checks (read only).
- Write only inside the workspace: outputs in their folders, packages in `ready`,
  and `queue.json`, `autopilot.md`, `log.md`, `autopilot-log.md` in settings.
  Never delete or overwrite a file the user wrote. Never touch the pack folder.
- At most `max_per_run` posts per run (default 3), so a run can never snowball.

## Mode 1: learn

### Step 1: check what already exists

Read `config.md`, `style.md`, `presets.md` and `plan.md`. If `config.md` is
missing, run `ie-setup` first: the autopilot needs the user's voice and field.

### Step 2: learn the routine

Two ways. Offer both in one line and let the user pick.

**A. Learn from what we just did.** If in this conversation the user went
through a full cycle by hand (for example plan, then a Reel script, caption and
edit plan), turn exactly that into the routine: the skills in the order they were
used, and the choices they made at each intake. Show it back and confirm.

**B. A short interview.** This is a one-time setup, so two batches are allowed
(see `INTAKE.md` for how to ask). Every question can be skipped.

Batch 1, the work:
1. **Where ideas come from / من أين الأفكار:** my weekly plan · news in my field · both
2. **What to prepare for each Reel / ماذا يُجهَّز لكل ريل:** script only · script and caption · script, caption and edit plan · all of these plus TikTok/Shorts/X versions
3. **Carousels and Stories / الكاروسيل والستوري:** prepare them too · Reels only
4. **How early / قبل الموعد بكم:** the day before · two days before · the morning of the day
5. **What you review / ماذا تراجع:** every post before I post it · only the plan · nothing, just tell me what is ready

Batch 2, the timing:
1. **When it runs / وقت التشغيل:** every morning (pick the hour) · weekdays · on posting days only
2. **Next week's plan / خطة الأسبوع القادم:** draft it on (pick a day) and wait for my OK · draft and use it · I make it myself
3. **Follow-up / المتابعة:** ask me for the numbers N days after posting (default 2) · do not ask
4. **News scan / متابعة الأخبار** (if news is a source): which topics, how many items a week at most

### Step 3: save the routine

Write `<settings>/autopilot.md` in the user's language with this shape, then show
it and save only on a clear yes:

```
# Autopilot routine
status: on
run: daily 08:40
lead_days: 1
max_per_run: 3
sources: plan            (plan | news | plan+news)
plan_day: thursday       (none if the user plans by hand)
plan_approval: ask       (ask | auto)
measure_after: 2         (0 = do not ask for numbers)
review: every-post       (every-post | plan-only | none)

## Chains (skills run in this order for each format)
- Reel: ie-reel > ie-caption > ie-edit > ie-crosspost
- Carousel: ie-carousel > ie-caption
- Story: ie-story
- News: ie-news > ie-edit

## News scan
topics: ...
max_per_week: 2

## Scheduler
where: (filled in step 4)
```

The answers each skill used during learning go to `presets.md` as usual, so the
unattended run can reuse them.

### Step 4: set up the schedule

Follow `SCHEDULE.md` next to this file. In short: use the agent's own scheduler
when it has one that runs on this computer in the workspace folder; otherwise
offer the operating system's scheduler. Show the user exactly what will be
created, create it only on a clear yes, record where it lives under
`## Scheduler`, and run once straight away (`run` mode) so they see the result
and approve any permission prompts. If nothing can be scheduled, say so and
explain the fallback: the check at the start of every session (below).

## Mode 2: run (unattended)

Nobody is watching. Do not ask questions and do not wait for answers: anything
that needs the user goes into the report. Follow `INTAKE.md`, "Unattended runs".

1. **Read** `workspace.json`, `autopilot.md`, `config.md`, `style.md`,
   `presets.md`. If `autopilot.md` is missing or `status: paused`, write one line
   to the report and stop.
2. **Plan check.** If `plan.md` is missing or ends within two days, and today is
   `plan_day`: run `ie-plan` with the saved presets. With `plan_approval: ask`
   save it as `plan-next.md` and list it in the report; with `auto`, append it
   to `plan.md` under a new week line.
3. **What is due:**
   `<tool> due --plan <settings>/plan.md --state <settings>/queue.json --lead <lead_days> --max <max_per_run> --once-per-day --json --lang <lang>`
   If it reports `already_ran`, a run happened today (a catch-up run, or two
   schedules): skip to step 6.
4. **Prepare each due post** with its format's chain. Each skill runs as usual
   and saves its output in its own folder. Then write one package to the `ready`
   folder, `YYYY-MM-DD-<topic>.md` with the post's date, holding: the plan row,
   the hook options, the script, the caption, the edit plan and other-platform
   versions (or links to their files), an "Assumed" line, and a checklist
   (review, film, edit, post, tell me "posted"). Then
   `<tool> mark --state <settings>/queue.json <id> drafted --file <package>`.
   A chain step that fails or lacks something: keep what worked, note the gap
   in the package and in the report, continue with the next post.
5. **News** (if a source): run `ie-news` for the saved topics, up to the weekly
   cap. A story that does not reach three independent sources is listed in the
   report as "unconfirmed", not written.
6. **Follow-up:** `<tool> status --plan ... --state ... --measure-after <n> --lang <lang>`.
   If the `inbox` folder holds new Insights screenshots or exports (newer than
   the last run in `autopilot-log.md`), run `ie-audit` on those files, add the
   results to `log.md`, and mark matching posts `measured`.
7. **Report.** Overwrite `<ready>/00-ماذا-ينتظرك.md` (English: `00-whats-waiting.md`)
   with: what was prepared (paths), what waits for review, what is late,
   which posts need numbers, plan or news items waiting for an OK, and any
   problem. Append one line per run to `<settings>/autopilot-log.md`:
   date, time, prepared, problems. If the agent can send a notification, send
   the first three lines of the report.

## Mode 3: follow-up (the user is here)

- **"What's ready / ماذا جهزت":** run `status`, show it, offer to open a package.
- **"I posted X / نشرت":** find the item in `status` by its idea or date and
  `mark <id> posted`. If they give numbers, add one line per post to
  `log.md` (date, format, idea, the hook actually used, taken from the
  package and not from the plan, views, saves, shares, follows) and mark
  `measured`. Do this first, before any analysis: a full `ie-audit` comes
  only when they ask why something worked or there are enough posts to compare.
- **"Skip it / تخطّه":** `mark <id> skipped`.
- **"Approved / اعتمد":** `mark <id> approved`; for `plan-next.md`, move it
  into `plan.md` under a new week line, and say what changed.
- **Changes to a draft:** edit the package, then learn from the edit as
  `INTAKE.md` describes (one edit is a guess, two the same way is a preference).
- **"Pause / أوقف":** set `status: paused` in `autopilot.md`, and pause or
  delete the scheduled task where `## Scheduler` says it lives (ask which).
- **"Change the routine / عدّل الروتين":** back to learn, starting from the
  saved routine.

## At the start of every session

If `autopilot.md` exists with `status: on`, run `status` once, quietly. Say
nothing when nothing is waiting. Otherwise one line: what is ready, late or
needs numbers, and an offer to prepare what is due now. This is also the
fallback when no scheduler is available.
