#!/usr/bin/env python3
"""
score.py - how natural does this draft read? Arabic and English.

Five checks, each 0-100, higher reads more like a person:

  VARIETY      sentence lengths vary the way speech does
  SPECIFICS    numbers, names, handles, times, places per 100 words
  STOCK        stock-phrase density from data/stock_phrases.json (lower is better)
  TYPOGRAPHY   stray invisible characters, em dashes, Latin punctuation inside
               Arabic, curly quotes inside English
  VOICE        a person talking to a person: I/we and you, contractions or
               colloquial forms, no staged structures

Overall = 60% the average + 40% the weakest check, because one bad signal is
enough to make a draft read wrong. PASS: overall 70+ and no check under 55.

Say this honestly: these are local writing heuristics. They are not an AI
detector, they call no service, and passing them guarantees nothing about any
detector's verdict. The goal is writing people want to read, not evasion.

Usage:
  python3 score.py draft.txt
  python3 score.py before.txt after.txt      # compare
  python3 score.py draft.txt --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import textkit as tk  # noqa: E402
from clean import load_lexicon, structural_flags  # noqa: E402

AR_FIRST = {"انا", "نحن", "احنا", "إحنا", "عندي", "لي", "اعرف", "نعرف", "جربت", "كنت", "خسرت", "شفت",
            "قلت", "لقيت", "فتحت", "غيرت", "فعلت", "سويت", "كتبت", "قريت", "حطيت", "رحت", "عرفت",
            "نسيت", "دخلت", "اكتشفت", "طلعت", "ضغطت", "نزلت", "حملت", "تعلمت", "خلصت", "بديت"}
# time, money and size units that make a sentence concrete in Arabic
AR_UNITS = {"الساعه", "ساعه", "ساعتين", "ساعات", "دقيقه", "دقيقتين", "دقائق", "ثانيه", "ثواني", "يوم",
            "يومين", "ايام", "اسبوع", "اسبوعين", "شهر", "شهرين", "اشهر", "سنه", "سنتين", "سنوات",
            "امس", "فجرا", "الفجر", "الظهر", "العصر", "المغرب", "الليل", "ريال", "دولار", "جنيه",
            "دينار", "درهم", "جيجا", "ميجا", "تيرا", "مليون", "مليار", "الف"}
AR_SECOND = {"انت", "انتي", "انتم", "حسابك", "جوالك", "هاتفك", "بياناتك", "كلمتك", "لك", "عندك", "تعرف", "تقدر", "تستخدم"}
AR_COLLOQUIAL = {"ليش", "وش", "ايش", "شو", "كيفك", "يعني", "بس", "مره", "مرة", "حق", "اللي", "هذي", "هاذا", "الحين", "هسه", "دحين", "ازاي", "عشان", "علشان", "مو", "مش", "ما", "راح", "رح", "ابغى", "ابي", "بدي", "عايز"}
EN_FIRST = {"i", "i'm", "i've", "i'd", "we", "we're", "my", "our", "me", "us"}
EN_SECOND = {"you", "you're", "your", "you've", "yours"}
CONTRACTION_RE = re.compile(r"\b\w+'(?:t|s|re|ve|ll|d|m)\b", re.IGNORECASE)


def _clamp(v):
    return max(0.0, min(100.0, v))


def _prose(text):
    """Text without URLs, handles and hashtags: those are not writing."""
    return tk.HASHTAG_RE.sub(" ", tk.MENTION_RE.sub(" ", tk.URL_RE.sub(" ", text)))


def check_variety(text):
    text = _prose(text)
    lens = [len(tk.words(s)) for s in tk.sentences(text)]
    if len(lens) < 3:
        return 60.0, "too few sentences to judge"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    # people land around 0.45-0.8; machines and templates sit near 0.2
    return _clamp(cv / 0.5 * 100), "length variation %.2f across %d sentences" % (cv, len(lens))


def check_specifics(text):
    ws = tk.words(text)
    if not ws:
        return 0.0, "no words"
    n = len(ws)
    digits = sum(1 for w in ws if tk.has_digit(w.translate(tk.DIGIT_TRANS)))
    handles = len(tk.MENTION_RE.findall(text))
    quoted = len(re.findall(r"[\"«][^\"»]{2,40}[\"»]", text))
    # English proper nouns: capitalised words not at a sentence start
    caps = 0
    for s in tk.sentences(text):
        sw = tk.words(s)
        caps += sum(1 for w in sw[1:] if w[:1].isupper() and not w.isupper())
    latin_in_ar = 0
    if tk.lang_of(text) != "en":
        # product and brand names written in Latin inside Arabic text
        latin_in_ar = sum(1 for w in ws if re.match(r"[A-Za-z]", w))
    units = sum(1 for w in ws if tk.fold(w) in AR_UNITS)
    markers = digits + handles + quoted + caps + latin_in_ar + units
    per100 = markers / n * 100
    return _clamp(per100 / 5 * 100), "%d concrete markers per 100 words" % round(per100)


def check_stock(text, lex):
    ws = tk.words(text)
    if not ws:
        return 100.0, "no words"
    hits = 0
    for lang in ("ar", "en"):
        for e in lex.get(lang, []):
            hits += len(tk.ar_pattern(e["find"]).findall(text))
    per100 = hits / len(ws) * 100
    return _clamp(100 - per100 * 25), "%d stock phrases (%.1f per 100 words)" % (hits, per100)


def check_typography(text):
    text = tk.URL_RE.sub(" ", text)
    bad_inv = sum(1 for _, _, _, legit in tk.scan_invisible(text) if not legit)
    em = text.count("—") + text.count("―")
    latin_in_ar, curly = 0, 0
    for line in text.split("\n"):
        lang = tk.lang_of(line)
        if lang == "ar":
            latin_in_ar += len(re.findall("[\u0600-ۿ]\\s*[,;?](?!\\d)", line))
        elif lang == "en":
            curly += sum(line.count(c) for c in "‘’“”")
    per1k = (bad_inv * 4 + em * 2 + latin_in_ar * 2 + curly) / max(len(text), 1) * 1000
    detail = "%d invisible, %d em dash, %d Latin punctuation in Arabic, %d curly quotes" % (
        bad_inv, em, latin_in_ar, curly)
    return _clamp(100 - per1k * 12), detail


def check_voice(text, lex):
    text = _prose(text)
    ws = [tk.fold(w) for w in tk.words(text)]
    if not ws:
        return 0.0, "no words"
    first = sum(1 for w in ws if w in EN_FIRST or w in {tk.fold(x) for x in AR_FIRST})
    second = sum(1 for w in ws if w in EN_SECOND or w in {tk.fold(x) for x in AR_SECOND})
    # Arabic first person often lives in an object suffix: wassalni, khallani
    first += sum(1 for w in ws if len(w) > 3 and w.endswith("\u0646\u064a")
                 and any(tk.is_arabic(c) for c in w))
    # Arabic second person is mostly a suffix: a word ending in -ak / -kum
    second += sum(1 for w in ws if len(w) > 3 and re.search("(ك|كم)$", w)
                  and any(tk.is_arabic(c) for c in w))
    colloquial = sum(1 for w in ws if w in {tk.fold(x) for x in AR_COLLOQUIAL})
    contractions = len(CONTRACTION_RE.findall(text))
    staged = len(structural_flags(text, lex))
    n = len(ws)
    score = 40
    score += min(25, (first / n * 100) * 5)
    score += min(25, (second / n * 100) * 5)
    score += min(15, ((contractions + colloquial) / n * 100) * 3)
    score -= staged * 12
    detail = "I/we %d, you %d, contractions/colloquial %d, staged structures %d" % (
        first, second, contractions + colloquial, staged)
    return _clamp(score), detail


def run(text, lex=None):
    lex = lex or load_lexicon()
    if not tk.words(text):
        print("error: no words to score", file=sys.stderr)
        sys.exit(2)
    checks = [
        ("VARIETY",) + check_variety(text),
        ("SPECIFICS",) + check_specifics(text),
        ("STOCK",) + check_stock(text, lex),
        ("TYPOGRAPHY",) + check_typography(text),
        ("VOICE",) + check_voice(text, lex),
    ]
    scores = [c[1] for c in checks]
    overall = 0.6 * statistics.mean(scores) + 0.4 * min(scores)
    if overall >= 70 and min(scores) >= 55:
        verdict = "PASS"
    elif overall >= 50:
        verdict = "REVIEW"
    else:
        verdict = "REWRITE"
    weakest = min(checks, key=lambda c: c[1])[0]
    return {"lang": tk.lang_of(text), "checks": checks, "overall": round(overall, 1),
            "verdict": verdict, "weakest": weakest}


AR_NAMES = {"VARIETY": "تنوّع الجمل", "SPECIFICS": "التفاصيل", "STOCK": "العبارات الجاهزة",
            "TYPOGRAPHY": "الترقيم والأحرف", "VOICE": "الصوت البشري"}
AR_VERDICT = {"PASS": "طبيعي", "REVIEW": "يحتاج مراجعة", "REWRITE": "أعد الكتابة"}


def render(r, label=None):
    ar = r["lang"] == "ar"
    if label:
        print("\n== %s" % label)
    print("")
    for name, score, detail in r["checks"]:
        shown = AR_NAMES[name] if ar else name
        print("  %-16s %s %5.1f   %s" % (shown, tk.bar(score), score, detail))
    verdict = AR_VERDICT[r["verdict"]] if ar else r["verdict"]
    print("\n  %-16s %s %5.1f   %s" % ("النتيجة" if ar else "OVERALL", tk.bar(r["overall"]), r["overall"], verdict))
    weak = AR_NAMES[r["weakest"]] if ar else r["weakest"]
    print("  " + tk.say(r["lang"], "أضعف نقطة: %s. ابدأ بها." % weak, "Weakest: %s. Fix that first." % weak))
    print("  " + tk.say(r["lang"], "مقاييس كتابة محلية، وليست كاشف ذكاء اصطناعي.",
                        "Local writing heuristics, not an AI detector."))


def main():
    ap = argparse.ArgumentParser(description="Score how natural a draft reads (Arabic/English).")
    ap.add_argument("inputs", nargs="+", help="one file, or two to compare (before after)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    lex = load_lexicon()
    results = [(p, run(tk.read_input(p), lex)) for p in args.inputs]
    if args.json:
        print(json.dumps([{"file": p, **r} for p, r in results], ensure_ascii=False, indent=2))
        return
    for p, r in results:
        render(r, label=os.path.basename(p) if len(results) > 1 else None)
    if len(results) == 2:
        a, b = results[0][1]["overall"], results[1][1]["overall"]
        print("\n  %.1f -> %.1f  (%+.1f)\n" % (a, b, b - a))


if __name__ == "__main__":
    main()
