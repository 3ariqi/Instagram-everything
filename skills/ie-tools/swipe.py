#!/usr/bin/env python3
"""
swipe.py - rank hand-collected Reels by how far each beat its own account,
name the hook formula each one used, and write a swipe file.

Raw views are not evidence: 400k views on a 2M-follower account is a quiet day,
on a 4k-follower account it is a discovery. So everything ranks on the
OUTLIER MULTIPLE = views / that account's own recent median views.

Input: a tab-separated file with a header row. Required columns:
    account   median   views   hook
Optional: followers, length, cta, platform, url
`hook` is the first spoken or on-screen line, in the creator's own words.

Usage:
  python3 swipe.py captured.tsv
  python3 swipe.py captured.tsv --out <settings>/swipe.md
"""

import argparse
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import textkit as tk  # noqa: E402
from hookscore import load_formulas, classify, score_hook  # noqa: E402


def _num(v):
    v = (v or "").strip().translate(tk.DIGIT_TRANS).replace(",", "").replace("٬", "").lower()
    mult = 1
    if v.endswith("k"):
        mult, v = 1000, v[:-1]
    elif v.endswith("m"):
        mult, v = 1000000, v[:-1]
    try:
        return float(v) * mult
    except ValueError:
        return None


def load(path):
    raw = tk.read_input(path).splitlines()
    rows = [r for r in raw if r.strip()]
    if not rows:
        return [], ["empty file"]
    head = [h.strip().lower() for h in rows[0].split("\t")]
    missing = [c for c in ("account", "median", "views", "hook") if c not in head]
    if missing:
        return [], ["missing columns: " + ", ".join(missing)]
    out, problems = [], []
    for i, line in enumerate(rows[1:], 2):
        cells = line.split("\t")
        rec = {h: (cells[j].strip() if j < len(cells) else "") for j, h in enumerate(head)}
        median, views = _num(rec["median"]), _num(rec["views"])
        if not median or views is None:
            problems.append("line %d: median/views not numbers" % i)
            continue
        rec["median_n"], rec["views_n"] = median, views
        rec["multiple"] = views / median
        out.append(rec)
    return out, problems


def analyse(rows):
    formulas = load_formulas()
    for r in rows:
        f = classify(r["hook"], formulas)
        r["formula"] = f
        r["hook_score"] = score_hook(r["hook"])["score"]
        r["hook_words"] = len(tk.words(r["hook"]))
    rows.sort(key=lambda r: -r["multiple"])
    third = max(1, len(rows) // 3)
    top, bottom = rows[:third], rows[-third:] if len(rows) >= 3 else []

    def counts(group):
        c = {}
        for r in group:
            if r["formula"]:
                c[r["formula"]["id"]] = c.get(r["formula"]["id"], 0) + 1
        return c
    top_c, bot_c = counts(top), counts(bottom)
    over = sorted(((fid, n, bot_c.get(fid, 0)) for fid, n in top_c.items()), key=lambda x: (-(x[1] - x[2]), -x[1]))
    names = {f["id"]: f for f in formulas}
    return {
        "rows": rows, "top": top, "bottom": bottom, "over": over, "names": names,
        "accounts": len({r["account"] for r in rows}),
        "unclassified": [r for r in rows if not r["formula"]],
        "top_len": statistics.median([r["hook_words"] for r in top]) if top else 0,
        "bot_len": statistics.median([r["hook_words"] for r in bottom]) if bottom else 0,
    }


def render(a, lang):
    S = lambda ar, en: tk.say(lang, ar, en)
    L = []
    rows = a["rows"]
    L.append("# " + S("ملف الإلهام (Swipe)", "Swipe file"))
    L.append("")
    L.append(S("%d ريل · %d حساب · الأساس: متوسط كل حساب", "%d reels · %d accounts · baseline: each account's median")
             % (len(rows), a["accounts"]))
    L.append("")
    L.append("## " + S("الأكثر تفوقاً (فوق 3 أضعاف)", "Outliers (above 3x)"))
    L.append("")
    L.append("| x | hook | formula | account | views | median |")
    L.append("| --- | --- | --- | --- | --- | --- |")
    for r in rows:
        if r["multiple"] < 3:
            break
        f = r["formula"]
        fn = ("#%d %s" % (f["id"], f["name_ar"] if lang == "ar" else f["name_en"])) if f else "?"
        L.append("| %.1fx | %s (%d) | %s | %s | %s | %s |" % (
            r["multiple"], r["hook"].replace("|", "/"), r["hook_score"], fn, r["account"],
            "{:,.0f}".format(r["views_n"]), "{:,.0f}".format(r["median_n"])))
    L.append("")
    L.append("## " + S("ما الذي يتكرر في الثلث الأعلى", "What over-indexes in the top third"))
    L.append("")
    for fid, n_top, n_bot in a["over"][:5]:
        f = a["names"][fid]
        L.append("- #%d %s: %d %s، %d %s" % (fid, f["name_ar"] if lang == "ar" else f["name_en"], n_top,
                                            S("في الأعلى", "in the top"), n_bot, S("في الأدنى", "in the bottom")))
    L.append("- " + S("متوسط عدد كلمات الافتتاحية: %s في الأعلى، و%s في الأدنى",
                      "median hook length: %s words up top, %s at the bottom") % (a["top_len"], a["bot_len"]))
    L.append("")
    L.append("## " + S("غير مصنّفة (%d): اقرأها بنفسك", "Unclassified (%d): read these by hand") % len(a["unclassified"]))
    L.append("")
    for r in a["unclassified"][:12]:
        L.append("- %.1fx  %s  (%s)" % (r["multiple"], r["hook"], r["account"]))
    L.append("")
    n = len(rows)
    if n < 25 or a["accounts"] < 5:
        L.append(S("> العينة صغيرة (%d ريل من %d حسابات). هذا مؤشر لا دليل. اجمع 40 ريلاً من 6 حسابات على الأقل قبل أن تبني عليه.",
                   "> Small sample (%d reels, %d accounts). A hint, not evidence. Collect 40+ reels from 6+ accounts before you believe it.")
                 % (n, a["accounts"]))
    else:
        L.append(S("> العينة كافية لملاحظة نمط، وليست كافية لقانون.", "> Enough to see a pattern, not enough for a law."))
    return "\n".join(L) + "\n"


def main():
    tk.utf8_stdio()
    ap = argparse.ArgumentParser(description="Rank collected Reels by outlier multiple.")
    ap.add_argument("input", nargs="?", default="-")
    ap.add_argument("--out", help="write the swipe file (markdown) here")
    args = ap.parse_args()
    rows, problems = load(args.input)
    for p in problems:
        print("! " + p, file=sys.stderr)
    if not rows:
        sys.exit(1)
    lang = tk.lang_of(" ".join(r["hook"] for r in rows))
    md = render(analyse(rows), lang)
    if args.out:
        path = os.path.expanduser(args.out)
        if os.path.dirname(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(md)
        print(tk.say(lang, "كُتب: ", "written: ") + path)
    print(md)


if __name__ == "__main__":
    main()
