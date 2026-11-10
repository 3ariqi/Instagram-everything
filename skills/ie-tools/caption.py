#!/usr/bin/env python3
"""
caption.py - lint an Instagram caption before it goes out. Arabic and English.

Platform limits it checks (checked November 2026):
  - 2,200 characters per caption
  - about 125 characters show in the feed before "more"
  - hashtags: Instagram announced in December 2025 that it will gradually cap
    a post at 5. The rollout is uneven (some accounts still see 30, some see 3),
    so going over 5 is a WARNING, not an error. Fewer is safer either way.
  - links in captions are not clickable

Writing checks:
  - what the viewer actually sees before "more", and whether it stops at a
    point that makes them tap, or mid-word
  - a greeting or a preamble in the first line
  - more than one call to action (one ask converts; three asks convert none)
  - Arabic lines whose first letter is Latin (an @handle, a brand name): the
    app aligns that line left, so it breaks the right-to-left flow
  - Latin punctuation inside Arabic sentences
  - the signature, if you pass one, is present and is the last thing

Usage:
  python3 caption.py caption.txt
  python3 caption.py caption.txt --signature "تابعنا على منصات التواصل الاجتماعي @3ariqi"
  python3 caption.py caption.txt --json
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import textkit as tk  # noqa: E402
from hookscore import GREETING_AR, GREETING_EN, PREAMBLE_AR, PREAMBLE_EN  # noqa: E402

MAX_CHARS = 2200
VISIBLE = 125
MAX_TAGS = 5
CTA_AR = re.compile(r"(^|\s)(تابع|تابعني|تابعنا|علق|علقوا|اكتب|اكتبوا|احفظ|احفظوا|شارك|شاركوا|منشن|اضغط|الرابط في البايو|ارسل|ارسلها)(\s|$|[،.!])")
CTA_EN = re.compile(r"\b(follow|comment|save this|save it|share this|share it|tag (a|someone|your)|click|link in bio|dm me|send this)\b", re.IGNORECASE)


def visible_part(text):
    """What shows before 'more': the first ~125 characters, and never more than
    the first two lines."""
    lines = text.split("\n")
    two = "\n".join(lines[:2])
    cut = two[:VISIBLE]
    truncated = len(text) > len(cut)
    return cut, truncated


def first_strong(line):
    for ch in line:
        if tk.is_arabic(ch):
            return "ar"
        if "a" <= ch.lower() <= "z":
            return "en"
    return None


def lint(text, signature=None):
    lang = tk.lang_of(text)
    errors, warnings, info = [], [], []
    S = lambda ar, en: tk.say(lang, ar, en)

    n = len(text)
    if n > MAX_CHARS:
        errors.append(S("الكابشن %d حرفاً، والحد %d." % (n, MAX_CHARS), "%d characters, over the %d limit." % (n, MAX_CHARS)))

    cut, truncated = visible_part(text)
    info.append(S("الظاهر قبل «المزيد»:", "visible before 'more':") + "\n      " + cut.replace("\n", " / "))
    first_len = len(text.split("\n")[0])
    if truncated and first_len > len(cut):
        # Only line one matters: if it already ends before the cut, the hook is
        # complete and the second line trailing off into "more" is normal.
        nxt = text[len(cut):len(cut) + 1]
        if nxt and not nxt.isspace() and cut[-1:].isalnum():
            warnings.append(S("القطع يقع في منتصف كلمة. اجعل السطر الأول ينتهي بنقطة تشويق قبل 125 حرفاً.",
                              "The cut lands mid-word. End line one on a cliff before 125 characters."))
    first_line = tk.fold(text.strip().split("\n")[0]) if text.strip() else ""
    if GREETING_AR.search(first_line) or GREETING_EN.search(first_line) or \
            PREAMBLE_AR.search(first_line) or PREAMBLE_EN.search(first_line):
        warnings.append(S("السطر الأول تحية أو تمهيد، وهو السطر الوحيد المضمون أن يُقرأ.",
                          "Line one is a greeting or preamble, and it is the only line everyone reads."))
    if cut.strip() and len(tk.words(cut)) < 3:
        warnings.append(S("الجزء الظاهر يكاد يخلو من الكلمات (إيموجي أو هاشتاقات).",
                          "The visible part is nearly all emoji or hashtags."))

    tags = tk.HASHTAG_RE.findall(text)
    if len(tags) > MAX_TAGS:
        warnings.append(S("%d هاشتاقات. أعلنت إنستقرام في ديسمبر 2025 خفض الحد إلى %d تدريجياً، وقد يرفض حسابك أكثر من ذلك. الأقل أأمن." % (len(tags), MAX_TAGS),
                          "%d hashtags. Instagram announced a gradual cap of %d (Dec 2025); your account may reject more. Fewer is safer." % (len(tags), MAX_TAGS)))
    if tags and tk.HASHTAG_RE.search(cut):
        warnings.append(S("هاشتاق داخل الجزء الظاهر. مكانه آخر الكابشن.",
                          "A hashtag in the visible part. Put hashtags at the end."))

    if tk.URL_RE.search(text):
        warnings.append(S("الروابط في الكابشن غير قابلة للنقر. ضعها في البايو أو في ملصق رابط في الستوري.",
                          "Links in captions are not clickable. Use the bio link or a story link sticker."))

    mentions = tk.MENTION_RE.findall(text)
    if len(mentions) > 5:
        warnings.append(S("%d إشارات (@). كثرتها تبدو كإزعاج." % len(mentions), "%d @mentions reads as spam." % len(mentions)))

    body = text
    if signature and signature.strip() in text:
        body = text.replace(signature.strip(), " ")
    ctas = len(CTA_AR.findall(tk.fold(body))) + len(CTA_EN.findall(body))
    if ctas > 1:
        warnings.append(S("%d طلبات من المتابع (تابع، علّق، احفظ...). طلب واحد فقط." % ctas,
                          "%d calls to action. Keep one." % ctas))

    if lang in ("ar", "mixed"):
        for i, line in enumerate(text.split("\n"), 1):
            if line.strip() and first_strong(line) == "en" and any(tk.is_arabic(c) for c in line):
                warnings.append(S("السطر %d يبدأ بحرف لاتيني، فسيظهر بمحاذاة اليسار. ابدأه بكلمة عربية." % i,
                                  "Line %d starts with a Latin letter and will align left." % i))
        latin = len(re.findall("[\u0600-ۿ]\\s*[,;?](?!\\d)", text))
        if latin:
            warnings.append(S("%d علامة ترقيم لاتينية داخل جمل عربية. شغّل clean.py." % latin,
                              "%d Latin punctuation marks in Arabic sentences. Run clean.py." % latin))

    if signature:
        sig = signature.strip()
        if sig not in text:
            warnings.append(S("التوقيع غير موجود.", "Signature missing."))
        else:
            tail = text[text.rfind(sig) + len(sig):]
            if tk.HASHTAG_RE.sub("", tail).strip():
                warnings.append(S("التوقيع ليس في آخر الكابشن.", "Signature is not at the end."))

    invisible = sum(1 for *_, legit in tk.scan_invisible(text) if not legit)
    if invisible:
        warnings.append(S("%d حرف خفي. شغّل clean.py." % invisible, "%d invisible characters. Run clean.py." % invisible))

    verdict = "FIX" if errors else "REVIEW" if warnings else "OK"
    return {"lang": lang, "chars": n, "hashtags": len(tags), "verdict": verdict,
            "errors": errors, "warnings": warnings, "info": info}


def render(r):
    ar = r["lang"] == "ar"
    names = {"FIX": "يحتاج إصلاح", "REVIEW": "راجعه", "OK": "جاهز"}
    print("")
    for i in r["info"]:
        print("  " + i)
    print("")
    print("  " + ("الأحرف: %d / %d   الهاشتاقات: %d / %d" if ar else "chars: %d / %d   hashtags: %d / %d") % (
        r["chars"], MAX_CHARS, r["hashtags"], MAX_TAGS))
    for e in r["errors"]:
        print("  X " + e)
    for w in r["warnings"]:
        print("  ! " + w)
    print("\n  " + (names[r["verdict"]] if ar else r["verdict"]) + "\n")


def main():
    ap = argparse.ArgumentParser(description="Lint an Instagram caption (Arabic/English).")
    ap.add_argument("input", nargs="?", default="-")
    ap.add_argument("--signature", help="text that must close the caption")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    text = tk.read_input(args.input)
    if not text.strip():
        print("error: the caption is empty (nothing to lint)", file=sys.stderr)
        sys.exit(2)
    r = lint(text, args.signature)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        render(r)


if __name__ == "__main__":
    main()
