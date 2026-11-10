#!/usr/bin/env python3
"""
hookscore.py - score the first line of a Reel, in Arabic or English.

Five properties, each 0-100:

  FRONTLOAD  the point is in the first words, not a greeting or a preamble
  LENGTH     5-12 words and about 3 seconds or less spoken, timed per language
  CONCRETE   a number, a name, a time, a place, an amount
  TENSION    something is at stake: loss, risk, a mistake, a secret, a warning
  ADDRESS    it talks to "you", or it is an "I" confession

Overall = 60% the average + 40% the weakest. Dealbreakers cap a hook at 15:
a greeting or a channel intro, a hashtag in the hook, an emoji as the first
character, more than 20 words.

What it is good for: catching greetings, preambles, vague hooks and hooks that
take too long to say. What it cannot do: tell you which of two decent hooks will
travel. Shoot both and let the numbers decide.

Usage:
  python3 hookscore.py hooks.txt                 # one hook per line, ranked
  python3 hookscore.py --hook "لا أحد يخبرك أن كلمة مرورك تسربت"
  python3 hookscore.py hooks.txt --json
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

HOOKS = os.path.join(HERE, "data", "hooks.json")

# Written in folded form (see textkit.fold): no diacritics, plain alef, ه for ة, ي for ى.
GREETING_AR = re.compile(r"^(السلام عليكم|مرحبا|اهلا|هلا|هاي|صباح|مساء|يا جماعه|يا شباب|معكم|معاكم|انا معكم)")
PREAMBLE_AR = re.compile(r"^(في هذا الفيديو|في فيديو اليوم|اليوم (راح|رح|سوف|سنتكلم|بنتكلم|حنتكلم|نتكلم|احكيلكم)|قبل ما نبدا|خلونا نبدا|موضوعنا اليوم)")
FILLER_AR = re.compile(r"^(طيب|يعني|اوكي|بص|شوف|اسمع|بالنسبه)\b")
GREETING_EN = re.compile(r"^(hey|hi|hello|what'?s up|welcome back|good (morning|evening))\b")
PREAMBLE_EN = re.compile(r"^(in (this|today'?s) video|today (i'?m|we'?re|i will|we will)|before we (start|begin)|so today)")
FILLER_EN = re.compile(r"^(so|okay|ok|well|alright|basically|look)\b")

STAKES_AR = {"خسرت", "خساره", "خطر", "خطير", "خطا", "غلط", "غلطه", "احذر", "انتبه", "تحذير", "سر", "اسرار",
             "لا احد", "محد", "ابدا", "اختراق", "اخترق", "تسريب", "تسرب", "ثغره", "سرقه", "انسرق", "احتيال",
             "نصب", "يتجسس", "تجسس", "مراقب", "فضيحه", "كارثه", "ممنوع", "توقف", "بطل", "مجانا", "فلوس",
             "حذف", "انحذف", "ضاع", "مات", "دمر", "يكذب", "كذبه", "خرافه", "لا يحميك", "مخفي", "عاجل"}
STAKES_EN = {"lost", "lose", "losing", "cost", "mistake", "wrong", "never", "nobody", "secret", "warning",
             "stop", "don't", "hack", "hacked", "leak", "leaked", "breach", "scam", "stolen", "spy", "tracked",
             "danger", "dangerous", "deleted", "banned", "free", "money", "lie", "myth", "hidden", "broke"}
UNITS_AR = {"ساعه", "دقيقه", "دقيقتين", "ثانيه", "ثواني", "يوم", "ايام", "اسبوع", "شهر", "سنه", "سنوات",
            "ريال", "دولار", "جنيه", "دينار", "درهم", "مليون", "مليار", "الف", "جيجا", "فجرا", "امس"}
SPOKEN_NUM_AR = {"واحد", "اثنين", "ثلاث", "ثلاثه", "اربع", "خمس", "ست", "سبع", "ثمان", "تسع", "عشر",
                 "عشرين", "مئه", "ميه", "نص", "ربع"}
SPOKEN_NUM_EN = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                 "twenty", "hundred", "thousand", "million", "billion", "half", "zero"}
YOU_AR = {"انت", "انتي", "انتم", "لك", "عندك"}
I_AR = {"انا", "جربت", "خسرت", "كنت", "اعترف", "شفت", "لقيت", "وقعت"}
YOU_EN = {"you", "your", "you're", "you've", "yours"}
I_EN = {"i", "i'm", "i've", "my", "me"}


def load_formulas(path=HOOKS):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)["hooks"]


def classify(hook, formulas=None):
    formulas = formulas or load_formulas()
    f = tk.fold(hook.strip())
    for h in formulas:
        for pat in h.get("match_ar", []) + h.get("match_en", []):
            if re.search(pat, f):
                return h
    return None


def _phrases_in(folded, vocab):
    toks = folded.split()
    joined = " " + " ".join(toks) + " "
    return [v for v in vocab if (" " + v + " ") in joined or v in toks]


def score_hook(hook):
    raw = hook.strip()
    lang = tk.lang_of(raw)
    folded = tk.fold(raw)
    ws = tk.words(raw)
    fws = [tk.fold(w) for w in ws]
    n = len(ws)
    secs = tk.spoken_seconds(raw)
    deal, notes = None, []

    # FRONTLOAD
    if GREETING_AR.search(folded) or GREETING_EN.search(folded):
        frontload, deal = 0, tk.say(lang, "تحية في البداية. لا أحد فتح الريلز ليُحَيّا.",
                                    "Greeting. Nobody came to the feed to be greeted.")
    elif PREAMBLE_AR.search(folded) or PREAMBLE_EN.search(folded):
        frontload, deal = 0, tk.say(lang, "تمهيد يضيّع أول ثانيتين. ابدأ بالفكرة نفسها.",
                                    "Preamble. The first two seconds are the hook, not a table of contents.")
    elif FILLER_AR.search(folded) or FILLER_EN.search(folded):
        frontload = 45
        notes.append(tk.say(lang, "كلمة حشو في البداية", "filler word up front"))
    else:
        frontload = 100

    # LENGTH
    if 5 <= n <= 12 and secs <= 3.2:
        length = 100
    elif n < 5:
        length = 50 + n * 8
    else:
        over = max(n - 12, 0) * 8 + max(secs - 3.2, 0) * 25
        length = 100 - over
    ar_words = "كلمات" if 3 <= n <= 10 else "كلمة"
    notes.append(tk.say(lang, "%d " + ar_words + "، نحو %.1f ث نطقاً (المطلوب من 5 إلى 12 كلمة، وحتى 3 ث)",
                        "%d words, ~%.1fs spoken (want 5-12 words, 3s or less)") % (n, secs))
    if n > 20:
        deal = deal or tk.say(lang, "أطول من 20 كلمة. هذا ليس افتتاحية.", "Over 20 words. That is not a hook.")

    # CONCRETE
    digits = sum(1 for w in ws if tk.has_digit(w.translate(tk.DIGIT_TRANS)))
    units = sum(1 for w in fws if w in UNITS_AR)
    spoken = sum(1 for w in fws if w in SPOKEN_NUM_AR or w in SPOKEN_NUM_EN)
    names = len(re.findall(r"(?<!^)(?<![.!?]\s)\b[A-Z][a-zA-Z]+", raw)) if lang == "en" else \
        sum(1 for w in ws if re.match(r"[A-Za-z]", w))
    money = len(re.findall(r"[$€£%٪]", raw))
    concrete_n = digits + units + spoken + names + money
    concrete = {0: 20, 1: 75}.get(concrete_n, 100)
    notes.append(tk.say(lang, "عناصر محددة (رقم، اسم، وقت، مبلغ): %d", "%d concrete markers") % concrete_n)

    # TENSION
    stakes = _phrases_in(folded, STAKES_AR) + [w for w in fws if w in STAKES_EN]
    tension = {0: 30, 1: 80}.get(len(stakes), 100)
    notes.append(tk.say(lang, "كلمات التوتر: %d (%s)", "%d stakes words: %s") % (len(stakes), "، ".join(stakes[:4]) if lang == "ar" else ", ".join(stakes[:4]) or "-") if stakes
                 else tk.say(lang, "كلمات التوتر: لا شيء", "0 stakes words: -"))

    # ADDRESS
    you = sum(1 for w in fws if w in YOU_AR or w in YOU_EN)
    you += sum(1 for w in fws if len(w) > 3 and any(tk.is_arabic(c) for c in w) and re.search("(ك|كم)$", w))
    me = sum(1 for w in fws if w in I_AR or w in I_EN)
    address = 100 if (you or me) else 50

    if tk.HASHTAG_RE.search(raw):
        deal = deal or tk.say(lang, "هاشتاق داخل الافتتاحية. مكانه آخر الكابشن.", "Hashtag in the hook. It belongs at the end of the caption.")
    if raw and tk.is_emoji(raw[0]):
        deal = deal or tk.say(lang, "إيموجي كأول حرف. ابدأ بكلمة.", "Emoji as the first character. Lead with a word.")

    parts = {"FRONTLOAD": frontload, "LENGTH": max(0, min(100, length)), "CONCRETE": concrete,
             "TENSION": tension, "ADDRESS": address}
    overall = 0.6 * statistics.mean(parts.values()) + 0.4 * min(parts.values())
    if deal:
        overall = min(overall, 15)
    verdict = "STRONG" if overall >= 75 else "OK" if overall >= 50 else "WEAK"
    formula = classify(raw)
    return {"hook": raw, "lang": lang, "score": round(overall, 1), "verdict": verdict, "parts": parts,
            "weakest": min(parts, key=parts.get), "dealbreaker": deal, "notes": notes,
            "formula": ({"id": formula["id"], "ar": formula["name_ar"], "en": formula["name_en"]}
                        if formula else None)}


AR_VERDICT = {"STRONG": "قوية", "OK": "مقبولة", "WEAK": "ضعيفة"}


def render(results):
    print("")
    for r in results:
        ar = r["lang"] == "ar"
        v = AR_VERDICT[r["verdict"]] if ar else r["verdict"]
        f = r["formula"]
        fname = ("#%d %s" % (f["id"], f["ar"] if ar else f["en"])) if f else tk.say(r["lang"], "بلا صيغة معروفة", "no known formula")
        hook = r["hook"] if len(r["hook"]) <= 70 else r["hook"][:67] + "..."
        print("  %5.1f  %-7s %s" % (r["score"], v, hook))
        print("         %s | %s: %s" % (fname, tk.say(r["lang"], "الأضعف", "weakest"), r["weakest"]))
        if r["dealbreaker"]:
            print("         ! " + r["dealbreaker"])
        for note in r["notes"]:
            print("         - " + note)
        print("")
    lang = results[0]["lang"] if results else "en"
    print("  " + tk.say(lang, "صوّر الأعلى. إن كانت الأعلى تحت 50 فلا توجد افتتاحية هنا بعد.",
                        "Shoot the top one. If the top one is under 50, none of these is the hook yet."))
    print("")


def main():
    ap = argparse.ArgumentParser(description="Score Reel hooks (Arabic/English).")
    ap.add_argument("input", nargs="?", default="-", help="file with one hook per line, or -")
    ap.add_argument("--hook", help="score a single hook")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    lines = [args.hook] if args.hook else [ln for ln in tk.read_input(args.input).splitlines() if ln.strip()]
    if not lines:
        print("error: no hooks to score (one hook per line, or use --hook)", file=sys.stderr)
        sys.exit(2)
    results = sorted((score_hook(h) for h in lines), key=lambda r: -r["score"])
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        render(results)


if __name__ == "__main__":
    main()
