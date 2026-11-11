#!/usr/bin/env python3
"""
autopilot.py - the bookkeeping behind ie-autopilot: which posts in the weekly
plan are due to be prepared, what is waiting for the user, what is late, and
which published posts still need their numbers.

It reads the plan table (plan.md, written by ie-plan) and keeps one small state
file (queue.json) next to it. It never posts, sends or fetches anything.
Standard library only: no network, no subprocess.

  python3 autopilot.py due    --plan plan.md --state queue.json [--today 2026-11-15] [--lead 1] [--max 3]
  python3 autopilot.py mark   --state queue.json <id> <status> [--file path] [--note "..."]
  python3 autopilot.py status --plan plan.md --state queue.json [--measure-after 2]

  statuses: planned -> drafted -> approved -> posted -> measured   (or skipped)

Add --json for machine-readable output and --lang ar|en for the text report.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textkit as tk  # noqa: E402

STATUSES = ("planned", "drafted", "approved", "posted", "measured", "skipped")
OPEN = ("planned", "drafted", "approved")

# Header names the plan table may use, in Arabic or English.
COLUMNS = {
    "date": ("date", "التاريخ", "تاريخ"),
    "day": ("day", "اليوم", "يوم"),
    "time": ("time", "الوقت", "الساعة"),
    "format": ("format", "الشكل", "النوع", "الصيغة الفنية"),
    "pillar": ("pillar", "المحور", "الركيزة"),
    "idea": ("idea", "الفكرة", "الموضوع", "topic"),
    "formula": ("formula", "الصيغة", "القالب"),
    "hook": ("hook", "hook draft", "الافتتاحية", "مسودة الافتتاحية", "الهوك"),
    "owner": ("owner", "المسؤول", "من ينشر", "من"),
}
# Monday = 0, as datetime.weekday() counts.
DAYS = {
    "mon": 0, "monday": 0, "الاثنين": 0, "الإثنين": 0, "اثنين": 0,
    "tue": 1, "tuesday": 1, "الثلاثاء": 1, "ثلاثاء": 1,
    "wed": 2, "wednesday": 2, "الاربعاء": 2, "الأربعاء": 2, "اربعاء": 2,
    "thu": 3, "thursday": 3, "الخميس": 3, "خميس": 3,
    "fri": 4, "friday": 4, "الجمعة": 4, "جمعة": 4,
    "sat": 5, "saturday": 5, "السبت": 5, "سبت": 5,
    "sun": 6, "sunday": 6, "الاحد": 6, "الأحد": 6, "احد": 6,
}
WEEK_RE = re.compile(r"^\s*(?:\*\*)?\s*(?:week|week of|week starting|الأسبوع|الاسبوع|بداية الأسبوع|بداية الاسبوع)"
                     r"\s*(?:\*\*)?\s*[:：]\s*(?:\*\*)?\s*([0-9٠-٩]{4}-[0-9٠-٩]{1,2}-[0-9٠-٩]{1,2})", re.I | re.M)
DATE_RE = re.compile(r"([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})")
ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")


def parse_date(text):
    m = DATE_RE.search((text or "").translate(ARABIC_DIGITS))
    if not m:
        return None
    try:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


DAYS_FOLDED = {tk.normalize_ar(k): v for k, v in DAYS.items()}


def day_number(text):
    """Weekday (Monday = 0) from an Arabic or English day name, or None."""
    word = re.sub(r"[*_`]", "", text or "").strip().lower()
    word = word.split()[0] if word.split() else ""
    return DAYS.get(word, DAYS_FOLDED.get(tk.normalize_ar(word)))


def _cell_key(header):
    h = re.sub(r"[*_`]", "", header).strip().lower()
    for key, names in COLUMNS.items():
        if h in names:
            return key
    return None


def _split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def parse_plan(text):
    """Return (rows, problems). Each row is a dict with a real date."""
    problems = []
    week = WEEK_RE.search(text)
    week_start = parse_date(week.group(1)) if week else None
    lines = text.splitlines()
    rows, header = [], None
    for line in lines:
        if not line.strip().startswith("|"):
            header = None if not line.strip() else header
            continue
        cells = _split_row(line)
        if header is None:
            keys = [_cell_key(c) for c in cells]
            if "idea" in keys and ("date" in keys or "day" in keys):
                header = keys
            continue
        if all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells):
            continue
        row = {k: (cells[i] if i < len(cells) else "") for i, k in enumerate(header) if k}
        if not row.get("idea"):
            continue
        date = parse_date(row.get("date", ""))
        if date is None and row.get("day"):
            wd = day_number(row["day"])
            if wd is not None and week_start:
                date = week_start + dt.timedelta(days=(wd - week_start.weekday()) % 7)
        if date is None:
            problems.append("no date for: %s" % row["idea"][:60])
            continue
        row["date"] = date.isoformat()
        rows.append(row)
    if not rows and not problems:
        problems.append("no plan table found (need a column for the idea and one for the date or day)")
    elif problems and not week_start and any("no date" in p for p in problems):
        problems.append("add a date column, or a line 'Week: YYYY-MM-DD' above the table")
    return rows, problems


def item_id(row):
    idea = re.sub(r"\s+", " ", row.get("idea", "")).strip().lower()
    return "%s-%s" % (row["date"], hashlib.sha1(idea.encode("utf-8")).hexdigest()[:6])


def load_state(path):
    if not os.path.isfile(path):
        return {"items": {}, "last_run": None}
    with open(path, encoding="utf-8") as fh:
        try:
            state = json.load(fh)
        except ValueError:
            sys.stderr.write("error: %s is not valid JSON; fix or delete it\n" % path)
            sys.exit(2)
    state.setdefault("items", {})
    state.setdefault("last_run", None)
    return state


def save_state(path, state):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2, sort_keys=True)
    os.replace(tmp, path)


def sync(state, rows):
    """Add new plan rows; refresh the details of rows still in the plan; flag removed ones."""
    seen = set()
    for row in rows:
        iid = item_id(row)
        seen.add(iid)
        item = state["items"].get(iid)
        if item is None:
            item = state["items"][iid] = {"status": "planned", "files": [], "notes": []}
        item.update({k: row.get(k, "") for k in ("date", "time", "format", "pillar", "idea", "formula", "hook", "owner")})
        item["in_plan"] = True
    for iid, item in state["items"].items():
        if iid not in seen:
            item["in_plan"] = False
    return state


def read_plan(path):
    if not os.path.isfile(path):
        return [], ["plan not found: %s" % path]
    with open(path, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8-sig", errors="replace")
    return parse_plan(text)


def today_of(args):
    if args.today:
        d = parse_date(args.today)
        if d is None:
            sys.stderr.write("error: --today must look like 2026-11-15\n")
            sys.exit(2)
        return d
    return dt.date.today()


def due(state, today, lead, limit):
    """'planned' items dated from today up to `lead` days ahead, soonest first.
    A date already gone is not prepared any more: status reports it as late."""
    out = []
    for iid, it in state["items"].items():
        if it["status"] != "planned" or not it.get("in_plan", True):
            continue
        d = dt.date.fromisoformat(it["date"])
        days = (d - today).days
        if 0 <= days <= lead:
            out.append((d, iid, days))
    out.sort()
    picked = [{"id": iid, "days_left": days, **state["items"][iid]} for d, iid, days in out[:limit]]
    later = [iid for d, iid, days in out[limit:]]
    return picked, later


def report(state, today, lead, measure_after):
    r = {"ready": [], "approved": [], "late": [], "needs_numbers": [], "upcoming": [],
         "removed": [], "plan_ends": None}
    last = None
    for iid, it in sorted(state["items"].items(), key=lambda kv: kv[1]["date"]):
        d = dt.date.fromisoformat(it["date"])
        if it.get("in_plan", True):
            last = d if last is None or d > last else last
        entry = {"id": iid, **it}
        st = it["status"]
        if not it.get("in_plan", True) and st in OPEN:
            r["removed"].append(entry)
        elif st in OPEN and d < today:
            r["late"].append(entry)
        elif st == "drafted":
            r["ready"].append(entry)
        elif st == "approved":
            r["approved"].append(entry)
        elif st == "posted" and (today - d).days >= measure_after:
            r["needs_numbers"].append(entry)
        elif st == "planned" and (d - today).days > lead:
            r["upcoming"].append(entry)
    r["plan_ends"] = last.isoformat() if last else None
    r["plan_running_out"] = last is None or (last - today).days < 2
    r["last_run"] = state.get("last_run")
    return r


TEXT = {
    "en": {
        "ready": "Ready for your review", "approved": "Approved, waiting for you to post",
        "late": "Date passed: did you post it? (say posted or skipped)",
        "needs_numbers": "Posted: send me the numbers (views, saves, shares)",
        "upcoming": "Coming up", "removed": "No longer in the plan (keep or skip?)",
        "ends": "The plan ends on %s.", "runs_out": "The plan runs out soon: time for next week's plan.",
        "none": "Nothing waiting.", "due": "To prepare now", "later": "Left for the next run: %d",
        "already": "ALREADY_RAN today (%s). Nothing new to prepare; use --force for a manual run.",
    },
    "ar": {
        "ready": "جاهز لمراجعتك", "approved": "معتمد، بانتظار نشرك",
        "late": "فات موعده: هل نشرته؟ (قل نُشر أو تخطَّه)",
        "needs_numbers": "نُشر: أرسل لي أرقامه (مشاهدات، حفظ، مشاركات)",
        "upcoming": "قادم", "removed": "لم يعد في الخطة (أُبقيه أم أتخطاه؟)",
        "ends": "الخطة تنتهي في %s.", "runs_out": "الخطة توشك على الانتهاء: حان وقت خطة الأسبوع القادم.",
        "none": "لا شيء بانتظارك.", "due": "يُجهَّز الآن", "later": "مؤجل للتشغيل القادم: %d",
        "already": "ALREADY_RAN اليوم (%s). لا جديد للتجهيز؛ استخدم --force للتشغيل اليدوي.",
    },
}


def line_of(it):
    bits = [it["date"], it.get("format", ""), it.get("idea", "")]
    st = it.get("status", "")
    return "  - [%s] %s  (%s)" % (it["id"], " · ".join(b for b in bits if b), st)


def main(argv=None):
    tk.utf8_stdio()
    ap = argparse.ArgumentParser(description="Track the weekly plan for ie-autopilot.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("due", "status"):
        p = sub.add_parser(name)
        p.add_argument("--plan", required=True)
        p.add_argument("--state", required=True)
        p.add_argument("--today")
        p.add_argument("--lead", type=int, default=1, help="prepare posts this many days ahead")
        p.add_argument("--json", action="store_true")
        p.add_argument("--lang", choices=("ar", "en"), default="ar")
        if name == "due":
            p.add_argument("--max", type=int, default=3, help="at most this many posts per run")
            p.add_argument("--once-per-day", action="store_true",
                           help="report ALREADY_RAN if a run already happened today")
            p.add_argument("--force", action="store_true")
        else:
            p.add_argument("--measure-after", type=int, default=2,
                           help="ask for numbers this many days after posting")
    pm = sub.add_parser("mark")
    pm.add_argument("--state", required=True)
    pm.add_argument("id")
    pm.add_argument("status", choices=STATUSES)
    pm.add_argument("--file", action="append", default=[])
    pm.add_argument("--note")
    pm.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.cmd == "mark":
        state = load_state(args.state)
        item = state["items"].get(args.id)
        if item is None:
            matches = [k for k in state["items"] if k.startswith(args.id)]
            if len(matches) != 1:
                sys.stderr.write("error: no single item matches %s\n" % args.id)
                return 2
            item = state["items"][matches[0]]
            args.id = matches[0]
        item["status"] = args.status
        for f in args.file:
            if f not in item["files"]:
                item["files"].append(f)
        if args.note:
            item["notes"].append(args.note)
        save_state(args.state, state)
        print(json.dumps({"id": args.id, "status": args.status}, ensure_ascii=False) if args.json
              else "%s -> %s" % (args.id, args.status))
        return 0

    t = TEXT[args.lang]
    today = today_of(args)
    rows, problems = read_plan(args.plan)
    state = load_state(args.state)
    sync(state, rows)

    if args.cmd == "due":
        if args.once_per_day and not args.force and state.get("last_run") == today.isoformat():
            save_state(args.state, state)
            if args.json:
                print(json.dumps({"already_ran": today.isoformat(), "due": [], "problems": problems},
                                 ensure_ascii=False))
            else:
                print(t["already"] % today.isoformat())
            return 0
        picked, later = due(state, today, args.lead, max(args.max, 0))
        state["last_run"] = today.isoformat()
        save_state(args.state, state)
        if args.json:
            print(json.dumps({"today": today.isoformat(), "due": picked, "left_for_next_run": len(later),
                              "problems": problems}, ensure_ascii=False, indent=2))
        else:
            print("%s (%s):" % (t["due"], today.isoformat()))
            for it in picked:
                print(line_of(it))
            if not picked:
                print("  " + t["none"])
            if later:
                print(t["later"] % len(later))
            for p in problems:
                print("  ! " + p)
        return 0

    rep = report(state, today, args.lead, args.measure_after)
    save_state(args.state, state)
    if args.json:
        rep["problems"] = problems
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return 0
    shown = False
    for key in ("late", "ready", "approved", "needs_numbers", "removed", "upcoming"):
        if rep[key]:
            shown = True
            print("%s:" % t[key])
            for it in rep[key]:
                print(line_of(it))
    if not shown:
        print(t["none"])
    if rep["plan_ends"]:
        print(t["ends"] % rep["plan_ends"])
    if rep["plan_running_out"]:
        print(t["runs_out"])
    for p in problems:
        print("! " + p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
