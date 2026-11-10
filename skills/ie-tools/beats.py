#!/usr/bin/env python3
"""
beats.py - time a Reel script beat by beat, in Arabic or English.

Give it one beat per line. Timestamps are optional:
    0:00 لا أحد يخبرك أن كلمة مرورك تسربت
    0:03 افتح هذا الموقع واكتب بريدك
    0:07 ...
Without timestamps, each beat is timed from how long it takes to say.

It flags the four things that lose a viewer in the edit:
  - a hook beat longer than 3 seconds
  - any beat longer than 4 seconds with nothing changing on screen
  - a beat with more words than its slot can hold (rushed delivery)
  - a total that misses the target length by more than 15%
and it checks for a loop: the last beat echoing a word from the first, so the
replay feels seamless.

Usage:
  python3 beats.py script.txt
  python3 beats.py script.txt --target 30
  python3 beats.py script.txt --json
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import textkit as tk  # noqa: E402

HOOK_MAX = 3.0
BEAT_MAX = 4.0
TS_RE = re.compile(r"^\s*\[?(\d{1,2}):(\d{2})(?:\.(\d))?\]?\s*[-–—:|]?\s*(.*)$")
STOP_AR = {"في", "من", "على", "الى", "عن", "ان", "هذا", "هذه", "هذي", "و", "ما", "لا", "هو", "هي", "مع", "كل"}
STOP_EN = {"the", "a", "an", "and", "or", "to", "of", "in", "on", "is", "it", "this", "that", "you", "your", "i"}


def parse(raw):
    beats = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        m = TS_RE.match(line[:10].translate(tk.DIGIT_TRANS) + line[10:])
        if m:
            start = int(m.group(1)) * 60 + int(m.group(2)) + (int(m.group(3)) / 10 if m.group(3) else 0)
            beats.append({"start": start, "text": m.group(4).strip()})
        else:
            beats.append({"start": None, "text": line.strip()})
    return beats


def time_beats(beats):
    t = 0.0
    timed = all(b["start"] is not None for b in beats)
    for i, b in enumerate(beats):
        b["say"] = tk.spoken_seconds(b["text"])
        if timed:
            nxt = beats[i + 1]["start"] if i + 1 < len(beats) else None
            b["dur"] = (nxt - b["start"]) if nxt is not None else max(b["say"], 1.0)
        else:
            b["start"] = t
            b["dur"] = max(b["say"], 1.0)
            t += b["dur"]
    return timed


def _content(text):
    """Content words, folded for matching, mapped back to how they were written."""
    stops = STOP_AR | STOP_EN
    return {tk.fold(w): w for w in tk.words(text) if tk.fold(w) not in stops and len(w) > 2}


def analyse(raw, target=None):
    beats = parse(raw)
    if not beats:
        return {"beats": [], "notes": ["empty script"], "total": 0}
    timed = time_beats(beats)
    lang = tk.lang_of(raw)
    for i, b in enumerate(beats):
        b["flags"] = []
        if i == 0 and b["dur"] > HOOK_MAX:
            b["flags"].append(tk.say(lang, "الافتتاحية %.1f ث، أطول من %d ث" % (b["dur"], HOOK_MAX),
                                     "hook runs %.1fs, past %ds" % (b["dur"], HOOK_MAX)))
        elif b["dur"] > BEAT_MAX:
            b["flags"].append(tk.say(lang, "لقطة %.1f ث: غيّر شيئاً على الشاشة أو قسّمها" % b["dur"],
                                     "%.1fs beat: cut, zoom or add text, or split it" % b["dur"]))
        if timed and b["say"] > b["dur"] + 0.3:
            b["flags"].append(tk.say(lang, "كلام %.1f ث في مساحة %.1f ث: ستُسرع أو تُقطع" % (b["say"], b["dur"]),
                                     "%.1fs of speech in a %.1fs slot: rushed" % (b["say"], b["dur"])))
    total = beats[-1]["start"] + beats[-1]["dur"]
    notes = []
    if target:
        off = (total - target) / target
        if abs(off) > 0.15:
            notes.append(tk.say(lang, "المدة %.0f ث والهدف %d ث (%+.0f%%)" % (total, target, off * 100),
                                "runs %.0fs against a %ds target (%+.0f%%)" % (total, target, off * 100)))
    first = _content(beats[0]["text"])
    loop = sorted(first[k] for k in set(first) & set(_content(beats[-1]["text"]))) if len(beats) > 1 else []
    if loop:
        notes.append(tk.say(lang, "حلقة: آخر لقطة تكرر «%s» من الافتتاحية، فالإعادة تبدو طبيعية." % "، ".join(loop[:3]),
                            "Loop: the last beat echoes \"%s\" from the hook. Replays are free reach." % ", ".join(loop[:3])))
    elif len(beats) > 1:
        notes.append(tk.say(lang, "لا حلقة: آخر لقطة لا تشترك بكلمة مع الافتتاحية. فكّر في ربطهما.",
                            "No loop: the last beat shares no word with the hook. Consider tying them."))
    return {"lang": lang, "timed": timed, "beats": beats, "total": round(total, 1), "notes": notes}


def render(r):
    lang = r.get("lang", "en")
    print("")
    for b in r["beats"]:
        m, s = divmod(b["start"], 60)
        text = b["text"] if len(b["text"]) <= 60 else b["text"][:57] + "..."
        print("  %d:%04.1f  %4.1fs  %s" % (m, s, b["dur"], text))
        for f in b["flags"]:
            print("               ! " + f)
    print("\n  " + tk.say(lang, "المدة الكلية: %.1f ث%s", "total: %.1fs%s") % (
        r["total"], "" if r.get("timed") else tk.say(lang, " (مقدّرة من زمن النطق)", " (estimated from speech)")))
    for n in r["notes"]:
        print("  - " + n)
    print("")


def main():
    ap = argparse.ArgumentParser(description="Time a Reel script beat by beat.")
    ap.add_argument("input", nargs="?", default="-")
    ap.add_argument("--target", type=int, help="target length in seconds")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    text = tk.read_input(args.input)
    if not text.strip():
        print("error: the script is empty (one beat per line, with or without timestamps)", file=sys.stderr)
        sys.exit(2)
    r = analyse(text, args.target)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        render(r)


if __name__ == "__main__":
    main()
