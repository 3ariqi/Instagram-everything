#!/usr/bin/env python3
"""
clean.py - make a draft read like a person wrote it, in Arabic or English.

What it changes automatically:
  1. Invisible characters that have no business in a caption (zero-width
     spaces, word joiners, stray BOMs, bidi overrides). It KEEPS the joiners
     inside emoji sequences, the non-joiner between letters, direction marks
     and the tag characters of subdivision flags.
  2. Punctuation, by language:
       Arabic sentence: em dash -> Arabic comma, Latin , ; ? -> ، ؛ ؟
       English sentence: em dash -> comma, curly quotes -> straight
       Everywhere: horizontal ellipsis -> "...", bullet character -> "-"
  3. Stock phrases from data/stock_phrases.json marked mode=replace.

What it only REPORTS (needs judgement): stock phrases marked mode=flag, and
structural tells such as "not just X, but Y" or a one-word rhetorical question.

It never touches URLs, @mentions or #hashtags.

Usage:
  python3 clean.py draft.txt --report
  python3 clean.py draft.txt -o clean.txt
  cat draft.txt | python3 clean.py - --json
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import textkit as tk  # noqa: E402

LEXICON = os.path.join(HERE, "data", "stock_phrases.json")
PROTECT_RE = re.compile(tk.URL_RE.pattern + r"|(?<![\w@])@[A-Za-z0-9._]+|#[^\s#]+", re.IGNORECASE)


def load_lexicon(path=LEXICON):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _protect(text):
    """Swap URLs, mentions and hashtags for placeholders so nothing edits them."""
    saved = []

    def keep(m):
        saved.append(m.group(0))
        return "\u27EAIE%d\u27EB" % (len(saved) - 1)
    return PROTECT_RE.sub(keep, text), saved


def _restore(text, saved):
    return re.sub("\u27EAIE(\\d+)\u27EB", lambda m: saved[int(m.group(1))], text)


def _line_lang(line):
    return tk.lang_of(line)


def fix_punctuation(text):
    changes = []
    out_lines = []
    for line in text.split("\n"):
        lang = _line_lang(line)
        before = line
        line = line.replace("\u2026", "...").replace("\u2022", "-")
        if lang == "ar":
            line = re.sub(r"\s*[\u2014\u2015]\s*", "\u060C ", line)
            line = re.sub(r"\s+\u2013\s+", "\u060C ", line)
            # Latin punctuation directly after an Arabic letter
            ar = "[\u0600-\u06FF]"
            line = re.sub("(%s)\\s*,(?!\\d)" % ar, "\\1\u060C", line)
            line = re.sub("(%s)\\s*;" % ar, "\\1\u061B", line)
            line = re.sub("(%s)\\s*\\?" % ar, "\\1\u061F", line)
        else:
            line = re.sub(r"\s*[\u2014\u2015]\s*", ", ", line)
            line = re.sub(r"(?<=\d)\u2013(?=\d)", "-", line)
            line = re.sub(r"\s+\u2013\s+", ", ", line)
            line = line.replace("\u2018", "'").replace("\u2019", "'")
            line = line.replace("\u201C", '"').replace("\u201D", '"')
        # clean up what the dash swap can leave behind
        line = re.sub(r"([,\u060C])\s*([,\u060C.!?\u061F])", r"\2", line)
        line = re.sub(r"([,\u060C])(\S)", r"\1 \2", line)
        line = re.sub(r"[ \t]{2,}", " ", line).rstrip()
        if line != before:
            changes.append((before.strip(), line.strip()))
        out_lines.append(line)
    return "\n".join(out_lines), changes


def apply_lexicon(text, lex):
    replaced, flagged = [], []
    for lang in ("ar", "en"):
        for entry in lex.get(lang, []):
            pat = tk.ar_pattern(entry["find"])
            hits = len(pat.findall(text))
            if not hits:
                continue
            if entry.get("mode") == "replace":
                rep = entry.get("replace", "")

                def sub(m, rep=rep):
                    word = m.group(0)
                    before = m.string[m.start() - 1:m.start()]
                    if before in ("\u0648", "\u0641") and rep.startswith("\u0648"):
                        rep = rep[1:]  # "wa" is already attached in the text
                    if rep and word[:1].isupper():
                        return rep[:1].upper() + rep[1:]
                    return rep
                text = pat.sub(sub, text)
                replaced.append((hits, entry["find"], rep or "(deleted)", entry.get("group", "")))
            else:
                flagged.append((hits, entry["find"], entry.get("group", "")))
    # tidy after deletions: doubled spaces, a comma or Arabic comma left at a
    # line start, space before punctuation, sentence-initial capital
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(^|\n)[ \t]*[,\u060C]?[ \t]*", r"\1", text)
    text = re.sub(r"[ \t]+([,.!?\u060C\u061F\u061B])", r"\1", text)
    text = re.sub(r"(^|\n|[.!?]\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), text)
    return text, replaced, flagged


def structural_flags(text, lex):
    flags = []
    for lang in ("ar", "en"):
        for s in lex.get("structures", {}).get(lang, []):
            for m in re.finditer(s["pattern"], text, re.IGNORECASE):
                snippet = m.group(0).strip().replace("\n", " ")
                flags.append((snippet[:60], s["note"]))
    tags = tk.HASHTAG_RE.findall(text)
    if len(tags) > 5:
        flags.append((" ".join(tags[:6]) + " ...",
                      "More than 5 hashtags. Instagram is rolling out a cap of 5 / إنستقرام تطبّق تدريجياً حداً قدره خمسة هاشتاقات."))
    emoji_lines = [ln for ln in text.split("\n") if ln.strip() and tk.is_emoji(ln.strip()[0])]
    if len(emoji_lines) >= 3:
        flags.append((emoji_lines[0][:40], "Emoji-bullet list / قائمة بإيموجي في أول كل سطر: تبدو قالباً جاهزاً."))
    for m in re.finditer(r"\b(?:[A-Z]{3,}\s+){2,}[A-Z]{3,}\b", text):
        flags.append((m.group(0)[:40], "Three or more shouted words in a row."))
    return flags


def clean(text, lex=None):
    lex = lex or load_lexicon()
    protected, saved = _protect(text)
    no_inv, removed = tk.strip_invisible(protected)
    punct, punct_changes = fix_punctuation(no_inv)
    lexed, replaced, flagged = apply_lexicon(punct, lex)
    result = _restore(lexed, saved)
    return {
        "text": result,
        "invisible_removed": removed,
        "punctuation": punct_changes,
        "replaced": replaced,
        "flagged": flagged,
        "structures": structural_flags(result, lex),
    }


def render_report(r, lang, out=sys.stderr):
    p = lambda *a: print(*a, file=out)
    p("")
    p(tk.say(lang, "تقرير التنظيف", "CLEAN REPORT"))
    p("-" * 60)
    p(tk.say(lang, "  أحرف خفية حُذفت: %d", "  invisible characters removed: %d") % r["invisible_removed"])
    p(tk.say(lang, "  أسطر تغيّر ترقيمها: %d", "  lines with punctuation fixed: %d") % len(r["punctuation"]))
    if r["replaced"]:
        p(tk.say(lang, "\n  عبارات استُبدلت:", "\n  replaced:"))
        for hits, find, rep, group in r["replaced"]:
            p("    %dx  %s  ->  %s   [%s]" % (hits, find, rep, group))
    if r["flagged"]:
        p(tk.say(lang, "\n  عبارات تحتاج قرارك (لم تُغيَّر):", "\n  flagged, not changed (your call):"))
        for hits, find, group in r["flagged"]:
            p("    %dx  %s   [%s]" % (hits, find, group))
    if r["structures"]:
        p(tk.say(lang, "\n  أنماط تركيبية أعد صياغتها بيدك:", "\n  structures to rewrite by hand:"))
        for snippet, note in r["structures"]:
            p("    - \"%s\"\n      %s" % (snippet, note))
    p("")


def main():
    ap = argparse.ArgumentParser(description="Clean a draft (Arabic or English).")
    ap.add_argument("input", nargs="?", default="-", help="file, or - for stdin")
    ap.add_argument("-o", "--out", help="write the cleaned text here")
    ap.add_argument("--report", action="store_true", help="print what changed")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    raw = tk.read_input(args.input)
    if not raw.strip():
        print("error: nothing to clean (the input is empty)", file=sys.stderr)
        sys.exit(2)
    r = clean(raw)
    lang = tk.lang_of(raw)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(r["text"])
    else:
        sys.stdout.write(r["text"])
        if not r["text"].endswith("\n"):
            sys.stdout.write("\n")
    if args.report:
        render_report(r, lang)


if __name__ == "__main__":
    main()
