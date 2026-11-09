#!/usr/bin/env python3
"""
stylekit.py - learn how a person writes, from their own posts, and learn from
the edits they make to a draft. Arabic and English.

It measures; it does not guess who you are. Everything it reports is a count or
a ratio from the text you gave it, and everything it proposes to remember is
phrased as a question for you to confirm.

  learn   samples.txt     what your posts have in common
  diff    before.txt after.txt     what you changed in a draft

Samples file: put a line with three dashes (---) between posts. Without that
line, each block separated by a blank line counts as one post.

Usage:
  python3 stylekit.py learn samples.txt
  python3 stylekit.py learn samples.txt --out ~/.instagram-everything/style.md
  python3 stylekit.py diff draft.txt final.txt
  python3 stylekit.py learn samples.txt --json
"""

import argparse
import json
import os
import re
import statistics
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import textkit as tk  # noqa: E402
from hookscore import score_hook  # noqa: E402

STOP = {tk.fold(w) for w in (
    "في من على الى عن ان انه هذا هذه هذي ذلك التي الذي و ما لا هو هي مع كل او ثم قد كان كانت يكون لم لن "
    "the a an and or to of in on is it this that you your for with are was be as at by from not but").split()}
FORMAL = {tk.fold(w) for w in ("علاوه", "بالاضافه", "لذلك", "حيث", "كما", "ايضا", "فضلا", "بناء", "وبالتالي", "ومن")}
COLLOQUIAL = {tk.fold(w): region for w, region in (
    ("وش", "خليجي"), ("شلون", "خليجي/عراقي"), ("وايد", "خليجي"), ("ازاي", "مصري"), ("عايز", "مصري"),
    ("كده", "مصري"), ("اوي", "مصري"), ("شو", "شامي"), ("هلق", "شامي"), ("بدي", "شامي"), ("كتير", "شامي"),
    ("دحين", "يمني/حجازي"), ("ايش", "عامية"), ("الحين", "عامية"), ("ابغى", "عامية"), ("ابي", "عامية"),
    ("عشان", "عامية"), ("علشان", "عامية"), ("ليش", "عامية"), ("مره", "عامية"), ("بس", "عامية"), ("مش", "عامية"))}
AR_LETTER = "[" + chr(0x0600) + "-" + chr(0x06FF) + "]"
SEP_RE = re.compile(r"(?m)^\s*-{3,}\s*$")


def split_posts(text):
    """Return (posts, used_separator)."""
    if SEP_RE.search(text):
        parts, used = SEP_RE.split(text), True
    else:
        parts, used = re.split(r"\n\s*\n", text), False
    return [p.strip() for p in parts if tk.words(p)], used


def _prose(text):
    return tk.HASHTAG_RE.sub(" ", tk.MENTION_RE.sub(" ", tk.URL_RE.sub(" ", text)))


def _emoji(text):
    return [c for c in text if tk.is_emoji(c) and c not in (tk.VS16, tk.ZWJ)
            and not (0x1F3FB <= ord(c) <= 0x1F3FF)]


def _last_text_line(post):
    for ln in reversed(post.split("\n")):
        if tk.HASHTAG_RE.sub("", ln).strip():
            return ln.strip()
    return ""


def _hashtags_at_end(post):
    lines = post.strip().split("\n")
    seen_text_after = False
    for ln in reversed(lines):
        has_tag = bool(tk.HASHTAG_RE.search(ln))
        has_text = bool(tk.HASHTAG_RE.sub("", ln).strip())
        if has_tag and seen_text_after:
            return False
        if has_text:
            seen_text_after = True
    return True


def _ngrams(post):
    """{folded n-gram: the words as the person wrote them}."""
    raw = tk.words(_prose(post))
    toks = [tk.fold(w) for w in raw]
    out = {}
    for n in (2, 3, 4):
        for i in range(len(toks) - n + 1):
            gram = toks[i:i + n]
            if all(t in STOP for t in gram):
                continue
            out.setdefault(" ".join(gram), " ".join(raw[i:i + n]))
    return out


def _count_noun(n, plural, singular, dual=None):
    """Arabic number agreement: 2 takes the dual, 3 to 10 the plural, others the singular."""
    if dual and round(n) == 2:
        return dual
    return plural if 3 <= round(n) <= 10 else singular


def learn(posts):
    n = len(posts)
    prose = [_prose(p) for p in posts]
    sent_lens, q, ex, sents_total = [], 0, 0, 0
    for p in prose:
        for s in tk.sentences(p):
            sent_lens.append(len(tk.words(s)))
            sents_total += 1
            q += s.rstrip().endswith(("?", "؟"))
            ex += s.rstrip().endswith("!")
    all_words = [tk.fold(w) for p in prose for w in tk.words(p)]
    emo = [_emoji(p) for p in posts]
    top_emoji = Counter(c for e in emo for c in e).most_common(3)
    tags = [len(tk.HASHTAG_RE.findall(p)) for p in posts]
    surface = {}
    grams = Counter()
    for p in posts:
        found = _ngrams(p)
        grams.update(found.keys())
        for g, shown in found.items():
            surface.setdefault(g, shown)
    need = max(2, -(-n * 2 // 10))
    common = [(g, c) for g, c in grams.items() if c >= need]
    common.sort(key=lambda gc: (-gc[1], -len(gc[0])))
    kept = []
    for g, c in common:
        if not any(g in k and c == kc for k, kc in kept):
            kept.append((g, c))
    kept = [(surface[g], c) for g, c in kept]
    first_words = [tk.words(_prose(p))[:2] for p in posts]
    openers = Counter(" ".join(w) for w in first_words)
    last_lines = {}
    for p in posts:
        ln = _last_text_line(p)
        if ln:
            last_lines.setdefault(tk.fold(ln), ln)
    closers = Counter(tk.fold(_last_text_line(p)) for p in posts if _last_text_line(p))
    sig = [(last_lines[l], c) for l, c in closers.most_common(2) if c >= max(2, (n + 1) // 2)]
    colloq = Counter(w for w in all_words if w in COLLOQUIAL)
    langs = Counter(tk.lang_of(p) for p in posts)
    digits_ar = sum(1 for p in posts for c in p if c in tk.ARABIC_INDIC_DIGITS)
    digits_w = sum(1 for p in posts for c in p if c in "0123456789")
    ar_comma = sum(p.count(tk.AR_COMMA) for p in posts)
    lat_comma = sum(len(re.findall(AR_LETTER + "\\s*,", p)) for p in posts)
    hook_scores = [score_hook(p.split("\n")[0])["score"] for p in posts]
    mean_len = statistics.mean(sent_lens) if sent_lens else 0.0
    return {
        "posts": n,
        "lang": dict(langs),
        "words_median": statistics.median(len(tk.words(p)) for p in prose),
        "chars_median": statistics.median(len(p) for p in posts),
        "sentence_mean": round(mean_len, 1),
        "sentence_short_share": round(sum(1 for x in sent_lens if x <= 6) / max(len(sent_lens), 1), 2),
        "question_share": round(q / max(sents_total, 1), 2),
        "exclaim_share": round(ex / max(sents_total, 1), 2),
        "emoji_per_post": round(sum(len(e) for e in emo) / n, 1),
        "top_emoji": [c for c, _ in top_emoji],
        "hashtags_median": statistics.median(tags),
        "hashtags_at_end": sum(_hashtags_at_end(p) for p in posts if tk.HASHTAG_RE.search(p)),
        "hashtag_posts": sum(1 for t in tags if t),
        "mentions": sum(len(tk.MENTION_RE.findall(p)) for p in posts),
        "digits": "arabic-indic" if digits_ar > digits_w else "western" if digits_w else "none",
        "comma": "arabic" if ar_comma > lat_comma else "latin" if lat_comma else "none",
        "openers": [(o, c) for o, c in openers.most_common(3) if c >= 2 and o],
        "phrases": kept[:8],
        "signature_candidates": sig,
        "formal_per_100": round(sum(1 for w in all_words if w in FORMAL) / max(len(all_words), 1) * 100, 1),
        "colloquial": dict(colloq.most_common(8)),
        "colloquial_regions": sorted({COLLOQUIAL[w] for w in colloq if COLLOQUIAL[w] != "عامية"}),
        "hook_score_mean": round(statistics.mean(hook_scores), 1),
    }


def render_learn(r, used_sep):
    ar = (r["lang"] and max(r["lang"], key=r["lang"].get)) != "en"
    S = (lambda a, e: a) if ar else (lambda a, e: e)
    out = [S("# أسلوبي (مستخلص من %d %s)" % (r["posts"], _count_noun(r["posts"], "منشورات", "منشور", "منشورين")), "# My style (measured from %d posts)" % r["posts"]), ""]
    if not used_sep:
        out += [S("> لم أجد فاصل `---` بين المنشورات، فعددت كل كتلة بينها سطر فارغ منشوراً. تأكد من ذلك.",
                  "> No `---` separators found, so each blank-line block counted as one post. Check that."), ""]
    if r["posts"] < 5:
        out += [S("> العينة صغيرة (%d). هذه ملاحظات أولية وتتضح بعد خمسة منشورات فأكثر." % r["posts"],
                  "> Small sample (%d). Treat this as a first impression; it firms up from five posts." % r["posts"]), ""]
    out += [S("## ما قِسته", "## What I measured")]
    out.append(S("- الطول: وسيط %d %s، %d حرفاً للمنشور" % (r["words_median"], _count_noun(r["words_median"], "كلمات", "كلمة"), r["chars_median"]),
                 "- Length: median %d words, %d characters per post" % (r["words_median"], r["chars_median"])))
    out.append(S("- الجمل: متوسطها %s %s، و%d%% منها ست كلمات أو أقل" % (r["sentence_mean"], _count_noun(r["sentence_mean"], "كلمات", "كلمة"), r["sentence_short_share"] * 100),
                 "- Sentences: average %s words, %d%% are six words or fewer" % (r["sentence_mean"], r["sentence_short_share"] * 100)))
    out.append(S("- الأسئلة: %d%% من جملك أسئلة، والتعجب %d%%" % (r["question_share"] * 100, r["exclaim_share"] * 100),
                 "- Questions: %d%% of sentences, exclamations %d%%" % (r["question_share"] * 100, r["exclaim_share"] * 100)))
    out.append(S("- الإيموجي: %s لكل منشور %s" % (r["emoji_per_post"], ("(الأكثر: " + " ".join(r["top_emoji"]) + ")") if r["top_emoji"] else ""),
                 "- Emoji: %s per post %s" % (r["emoji_per_post"], ("(top: " + " ".join(r["top_emoji"]) + ")") if r["top_emoji"] else "")))
    out.append(S("- الهاشتاقات: وسيط %d، وفي آخر المنشور في %d من %d" % (r["hashtags_median"], r["hashtags_at_end"], r["hashtag_posts"]),
                 "- Hashtags: median %d, at the end in %d of %d posts" % (r["hashtags_median"], r["hashtags_at_end"], r["hashtag_posts"])))
    out.append(S("- الأرقام: %s، الفاصلة: %s" % ({"arabic-indic": "هندية (٣)", "western": "غربية (3)", "none": "لا أرقام"}[r["digits"]],
                                                   {"arabic": "عربية (،)", "latin": "لاتينية (,)", "none": "لا فواصل"}[r["comma"]]),
                 "- Digits: %s, comma: %s" % (r["digits"], r["comma"])))
    out.append(S("- متوسط درجة افتتاحياتك بـ hookscore: %s من 100" % r["hook_score_mean"],
                 "- Average hookscore of your first lines: %s of 100" % r["hook_score_mean"]))
    if r["openers"]:
        out.append(S("- تبدأ غالباً بـ: " + "، ".join("«%s» (%d×)" % o for o in r["openers"]),
                     "- You often open with: " + ", ".join('"%s" (%dx)' % o for o in r["openers"])))
    if r["phrases"]:
        out.append(S("- عبارات تتكرر: " + "، ".join("«%s» (%d %s)" % (p[0], p[1], _count_noun(p[1], "منشورات", "منشور", "منشورين")) for p in r["phrases"][:6]),
                     "- Recurring phrases: " + ", ".join('"%s" (%d posts)' % p for p in r["phrases"][:6])))
    if r["colloquial"]:
        out.append(S("- كلمات عامية وردت: " + "، ".join("%s (%d)" % kv for kv in r["colloquial"].items()),
                     "- Colloquial words found: " + ", ".join("%s (%d)" % kv for kv in r["colloquial"].items())))
    out += ["", S("## ما أحتاج تأكيده منك", "## What I need you to confirm"), ""]
    if r["signature_candidates"]:
        out.append(S("- [ ] هل هذا توقيعك؟ «%s» (ختمتَ به %d %s)" % (r["signature_candidates"][0][0], r["signature_candidates"][0][1], _count_noun(r["signature_candidates"][0][1], "منشورات", "منشور", "منشورين")),
                     '- [ ] Is this your signature? "%s" (closed %d posts)' % r["signature_candidates"][0]))
    if r["colloquial_regions"]:
        out.append(S("- [ ] الكلمات تشير إلى: %s. أي لهجة تكتب بها؟" % "، ".join(r["colloquial_regions"]),
                     "- [ ] The words point to: %s. Which dialect do you write in?" % ", ".join(r["colloquial_regions"])))
    else:
        out.append(S("- [ ] أي لهجة أو مستوى تكتب به؟ (فصحى مبسطة، لهجة محلية، خليط)",
                     "- [ ] Which register do you write in? (plain standard, local dialect, mix)"))
    out.append(S("- [ ] أي هذه الصفات تريد أن أحافظ عليها، وأيها تريد تغييره؟",
                 "- [ ] Which of these traits should I keep, and which do you want changed?"))
    return "\n".join(out)


def diff(before, after):
    def stats(t):
        p = _prose(t)
        lens = [len(tk.words(s)) for s in tk.sentences(p)]
        return {"sentence_mean": statistics.mean(lens) if lens else 0.0, "emoji": len(_emoji(t)),
                "hashtags": len(tk.HASHTAG_RE.findall(t)), "chars": len(t),
                "questions": sum(1 for s in tk.sentences(p) if s.rstrip().endswith(("?", "؟")))}
    a, b = stats(before), stats(after)
    shown = {}
    for w in tk.words(_prose(before)) + tk.words(_prose(after)):
        shown.setdefault(tk.fold(w), w)
    ca = Counter(tk.fold(w) for w in tk.words(_prose(before)) if tk.fold(w) not in STOP and len(w) > 1)
    cb = Counter(tk.fold(w) for w in tk.words(_prose(after)) if tk.fold(w) not in STOP and len(w) > 1)
    removed = [shown[w] for w, _ in (ca - cb).most_common(8)]
    added = [shown[w] for w, _ in (cb - ca).most_common(8)]
    ideas = []
    if a["sentence_mean"] and b["sentence_mean"] <= a["sentence_mean"] * 0.8:
        ideas.append(("جمل أقصر (من %.1f إلى %.1f كلمات)" % (a["sentence_mean"], b["sentence_mean"]),
                      "shorter sentences (%.1f -> %.1f words)" % (a["sentence_mean"], b["sentence_mean"])))
    elif a["sentence_mean"] and b["sentence_mean"] >= a["sentence_mean"] * 1.25:
        ideas.append(("جمل أطول (من %.1f إلى %.1f كلمة)" % (a["sentence_mean"], b["sentence_mean"]),
                      "longer sentences (%.1f -> %.1f words)" % (a["sentence_mean"], b["sentence_mean"])))
    if a["emoji"] and b["emoji"] == 0:
        ideas.append(("بلا إيموجي", "no emoji"))
    elif b["emoji"] > a["emoji"] + 1:
        ideas.append(("إيموجي أكثر", "more emoji"))
    if b["hashtags"] < a["hashtags"]:
        ideas.append(("هاشتاقات أقل (من %d إلى %d)" % (a["hashtags"], b["hashtags"]),
                      "fewer hashtags (%d -> %d)" % (a["hashtags"], b["hashtags"])))
    if b["questions"] > a["questions"]:
        ideas.append(("أسئلة أكثر", "more questions"))
    if a["chars"] and b["chars"] <= a["chars"] * 0.75:
        ideas.append(("نص أقصر بنحو %d%%" % round((1 - b["chars"] / a["chars"]) * 100),
                      "about %d%% shorter" % round((1 - b["chars"] / a["chars"]) * 100)))
    if removed:
        ideas.append(("حذفتَ كلمات مثل: " + "، ".join(removed[:5]), "you removed words like: " + ", ".join(removed[:5])))
    if added:
        ideas.append(("أضفتَ كلمات مثل: " + "، ".join(added[:5]), "you added words like: " + ", ".join(added[:5])))
    return {"before": a, "after": b, "removed": removed, "added": added, "ideas": ideas}


def render_diff(d, lang):
    S = (lambda a, e: a) if lang == "ar" else (lambda a, e: e)
    out = [S("## ما غيّرتَه في المسودة", "## What you changed in the draft"), ""]
    if not d["ideas"]:
        out.append(S("لا فرق يُذكر في الأسلوب، تعديلاتك كانت في المعنى أو الصياغة الخفيفة.",
                     "No notable style difference; your edits were about meaning or light rewording."))
        return "\n".join(out)
    for ar_, en in d["ideas"]:
        out.append("- " + S(ar_, en))
    out += ["", S("> هذا من تعديل واحد، فهو افتراض. أحفظه كتفضيل فقط إن أكدتَه، ويتأكد بتكراره.",
                  "> This comes from one edit, so it is an assumption. I save it as a preference only if you confirm it.")]
    return "\n".join(out)


def _read(path):
    return tk.read_input(path)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Learn a writing style from samples, or from your edits.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pl = sub.add_parser("learn", help="measure what a set of posts has in common")
    pl.add_argument("samples")
    pl.add_argument("--out", help="write the result (markdown) here")
    pl.add_argument("--json", action="store_true")
    pd = sub.add_parser("diff", help="what changed between a draft and the final text")
    pd.add_argument("before")
    pd.add_argument("after")
    pd.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.cmd == "learn":
        posts, used = split_posts(_read(args.samples))
        if not posts:
            print("error: no posts found in %s" % args.samples, file=sys.stderr)
            return 2
        r = learn(posts)
        if args.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
            return 0
        text = render_learn(r, used)
        if args.out:
            path = os.path.abspath(os.path.expanduser(args.out))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text + "\n")
            print("written: %s" % path)
        print(text)
        return 0

    before, after = _read(args.before), _read(args.after)
    if not tk.words(before) or not tk.words(after):
        print("error: both files need some text", file=sys.stderr)
        return 2
    d = diff(before, after)
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
    else:
        print(render_diff(d, tk.lang_of(after) if tk.lang_of(after) != "mixed" else "ar"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
