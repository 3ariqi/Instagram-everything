"""
textkit.py - shared, Unicode-aware text helpers for every tool in this pack.

Arabic and English are both first-class here. Everything is standard library,
nothing touches the network, nothing runs a process.

What it gives the other tools:
  - language detection (ar / en / mixed)
  - Arabic normalisation for matching (diacritics, tatweel, alef/ya/ta-marbuta)
  - word and sentence splitting that understands Arabic letters and digits
  - spoken-duration estimates per language
  - invisible-character handling that KEEPS what is legitimate:
      ZWJ inside emoji sequences (the joiner in a person-with-laptop emoji),
      ZWNJ between letters (needed in Persian/Urdu and some Arabic typesetting),
      RLM/LRM direction marks (needed when Arabic and Latin text mix),
      tag characters that build subdivision flags.
    and drops what is not: zero-width spaces, word joiners, BOMs mid-text,
    soft hyphens, bidi embedding/override controls (the "Trojan Source" class).
"""

import re
import unicodedata

# --------------------------------------------------------------------------
# character classes
# --------------------------------------------------------------------------

ARABIC_RANGES = (
    (0x0600, 0x06FF), (0x0750, 0x077F), (0x08A0, 0x08FF),
    (0xFB50, 0xFDFF), (0xFE70, 0xFEFF),
)
TASHKEEL_RE = re.compile("[ؐ-ًؚ-ٰٟۖ-ۭ]")
TATWEEL = "ـ"

ARABIC_INDIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
DIGIT_TRANS = str.maketrans(ARABIC_INDIC_DIGITS + PERSIAN_DIGITS, "0123456789" * 2)

AR_COMMA, AR_SEMICOLON, AR_QUESTION = "،", "؛", "؟"

ZWJ, ZWNJ, LRM, RLM = "\u200D", "\u200C", "\u200E", "\u200F"
VS16 = "️"

# Removed everywhere: they have no legitimate use in a caption or a script.
ALWAYS_DROP = {
    "\u200B": "zero-width space",
    "\u2060": "word joiner",
    "\u2061": "function application",
    "\u2062": "invisible times",
    "\u2063": "invisible separator",
    "\u2064": "invisible plus",
    "\u00AD": "soft hyphen",
    "\u180E": "mongolian vowel separator",
    "\u202A": "LRE embedding", "\u202B": "RLE embedding", "\u202C": "PDF pop",
    "\u202D": "LRO override", "\u202E": "RLO override",
    "\u2066": "LRI isolate", "\u2067": "RLI isolate", "\u2068": "FSI isolate",
    "\u2069": "PDI pop isolate",
}
SPACE_LIKE = {" ": " ", " ": " ", " ": " ", " ": " ",
              " ": " ", "　": " "}


def is_arabic(ch):
    o = ord(ch)
    return any(a <= o <= b for a, b in ARABIC_RANGES) and unicodedata.category(ch).startswith("L")


def is_emoji(ch):
    """Good-enough emoji test: pictographs, symbols, regional indicators, modifiers."""
    o = ord(ch)
    return (unicodedata.category(ch) == "So" or 0x1F1E6 <= o <= 0x1F1FF
            or 0x1F3FB <= o <= 0x1F3FF or o == 0xFE0F or 0x1F000 <= o <= 0x1FAFF
            or 0x2600 <= o <= 0x27BF)


def lang_of(text):
    """'ar', 'en' or 'mixed' from the share of Arabic vs Latin letters."""
    ar = sum(1 for c in text if is_arabic(c))
    la = sum(1 for c in text if ("a" <= c.lower() <= "z"))
    total = ar + la
    if total == 0:
        return "en"
    share = ar / total
    if share >= 0.7:
        return "ar"
    if share <= 0.3:
        return "en"
    return "mixed"


def normalize_ar(text):
    """For MATCHING only, never for output: strip diacritics and tatweel,
    unify alef forms, final ya and ta marbuta, convert Eastern digits."""
    t = TASHKEEL_RE.sub("", text).replace(TATWEEL, "")
    t = re.sub("[آأإٱ]", "ا", t)
    t = t.replace("ى", "ي").replace("ة", "ه")
    return t.translate(DIGIT_TRANS)


def fold(text):
    """Lowercase + Arabic normalisation, for case/variant-insensitive matching."""
    return normalize_ar(text).lower()


def ar_pattern(phrase):
    """Turn an Arabic (or English) phrase into a regex that tolerates
    diacritics, tatweel and the common letter variants, for in-place replacement."""
    out = []
    opt = "[ؐ-ًؚ-ٰٟـ]*"
    variants = {
        "ا": "[اأإآٱ]",
        "أ": "[اأإآٱ]",
        "إ": "[اأإآٱ]",
        "آ": "[اأإآٱ]",
        "ي": "[يى]", "ى": "[يى]",
        "ة": "[ةه]", "ه": "[ةه]",
    }
    for ch in phrase:
        if ch == " ":
            out.append(r"\s+")
        elif ch in variants:
            out.append(variants[ch] + opt)
        elif is_arabic(ch):
            out.append(re.escape(ch) + opt)
        else:
            out.append(re.escape(ch))
    body = "".join(out)
    # Word boundaries that work for Arabic too. A phrase may also follow a
    # single attached conjunction (wa-, fa-), which is kept, not replaced.
    start = r"(?:(?<![^\W_])|(?<=(?<![^\W_])[وف]))"
    return re.compile(start + body + r"(?![^\W_])", re.IGNORECASE)


# --------------------------------------------------------------------------
# tokenising
# --------------------------------------------------------------------------

WORD_RE = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*", re.UNICODE)
SENT_SPLIT_RE = re.compile(r"(?<=[.!?؟…])\s+|\n+")


def words(text):
    """Words, Arabic-aware: diacritics and tatweel are removed first so they
    never split a word in two."""
    clean = TASHKEEL_RE.sub("", text).replace(TATWEEL, "")
    return WORD_RE.findall(clean)


def sentences(text):
    parts = [p.strip() for p in SENT_SPLIT_RE.split(text)]
    return [p for p in parts if words(p)]


# Average conversational speaking rates, words per second. Arabic words carry
# attached prefixes and suffixes, so fewer of them fit in a second.
RATE = {"ar": 2.2, "en": 2.6}


def spoken_seconds(text):
    ws = words(text)
    if not ws:
        return 0.0
    ar = sum(1 for w in ws if any(is_arabic(c) for c in w))
    en = len(ws) - ar
    return ar / RATE["ar"] + en / RATE["en"]


def has_digit(token):
    return any(c.isdigit() for c in token)


# --------------------------------------------------------------------------
# invisible characters
# --------------------------------------------------------------------------

def _keep_zwj(text, i):
    prev = text[i - 1] if i > 0 else ""
    nxt = text[i + 1] if i + 1 < len(text) else ""
    return bool(prev and nxt and (is_emoji(prev) or prev == VS16) and is_emoji(nxt))


def _keep_zwnj(text, i):
    prev = text[i - 1] if i > 0 else ""
    nxt = text[i + 1] if i + 1 < len(text) else ""
    return bool(prev and nxt and unicodedata.category(prev).startswith("L")
                and unicodedata.category(nxt).startswith("L"))


def _in_tag_sequence(text, i):
    """Tag characters are legitimate only inside a black-flag subdivision flag."""
    j = i
    while j > 0 and 0xE0020 <= ord(text[j - 1]) <= 0xE007F:
        j -= 1
    return j > 0 and text[j - 1] == "\U0001F3F4"


def scan_invisible(text):
    """Return a list of (index, codepoint, name, legit) for every invisible or
    format character, saying which ones are legitimate in context."""
    found = []
    for i, ch in enumerate(text):
        o = ord(ch)
        cat = unicodedata.category(ch)
        if ch == ZWJ:
            found.append((i, o, "zero-width joiner", _keep_zwj(text, i)))
        elif ch == ZWNJ:
            found.append((i, o, "zero-width non-joiner", _keep_zwnj(text, i)))
        elif ch in (LRM, RLM):
            found.append((i, o, "direction mark", True))
        elif 0xE0020 <= o <= 0xE007F:
            found.append((i, o, "tag character", _in_tag_sequence(text, i)))
        elif ch == "\uFEFF":
            found.append((i, o, "byte-order mark", False))
        elif ch in ALWAYS_DROP:
            found.append((i, o, ALWAYS_DROP[ch], False))
        elif ch in SPACE_LIKE:
            found.append((i, o, "non-breaking/narrow space", False))
        elif cat in ("Cf", "Co", "Cn") and ch not in "\n\r\t":
            found.append((i, o, unicodedata.name(ch, "unnamed format character").lower(), False))
    return found


def strip_invisible(text):
    """Remove invisible characters that are not legitimate in context; turn
    odd spaces into normal spaces. Returns (clean_text, removed_count)."""
    bad = {i for i, o, name, legit in scan_invisible(text) if not legit}
    out, removed = [], 0
    for i, ch in enumerate(text):
        if i in bad:
            removed += 1
            if ch in SPACE_LIKE:
                out.append(" ")
            continue
        out.append(ch)
    return "".join(out), removed


# --------------------------------------------------------------------------
# misc
# --------------------------------------------------------------------------

URL_RE = re.compile(r"https?://[^\s<>\"]+|www\.[^\s<>\"]+", re.IGNORECASE)
HASHTAG_RE = re.compile(r"(?<![^\s])#[^\s#]+")
MENTION_RE = re.compile(r"(?<![\w@])@[A-Za-z0-9._]{1,30}")


def utf8_stdio():
    """Make stdout and stderr UTF-8, whatever the console's code page is.

    On Windows, output that is piped (which is how every agent runs a tool) is
    encoded with the legacy code page, cp1252 or cp437, and the first Arabic
    character raises UnicodeEncodeError. PYTHONUTF8 cannot fix that for us,
    because the tools are run with -I, which ignores environment variables."""
    import sys
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
        except (AttributeError, ValueError, OSError):
            pass  # not a text stream we can change (already wrapped or closed)


MAX_INPUT_CHARS = 400000


def read_input(path):
    """Read text from a file or stdin. On a problem, print one clear line and
    exit with code 2 instead of a traceback. Accepts UTF-8 (with or without a
    BOM) and UTF-16, the two encodings Arabic text files usually arrive in."""
    import sys
    try:
        if path in (None, "-"):
            raw = sys.stdin.buffer.read()
        else:
            with open(path, "rb") as fh:
                raw = fh.read(MAX_INPUT_CHARS * 4 + 1)
    except OSError as e:
        sys.stderr.write("error: cannot read %s (%s)\n" % (path, e.strerror or e))
        sys.exit(2)
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        codecs = ("utf-16",)
    else:
        codecs = ("utf-8-sig",)
    for codec in codecs:
        try:
            text = raw.decode(codec)
            break
        except UnicodeDecodeError:
            text = None
    if text is None:
        sys.stderr.write("error: %s is not a UTF-8 text file. Save it as UTF-8 (in Notepad: "
                         "Save As > Encoding > UTF-8) and try again.\n" % path)
        sys.exit(2)
    if len(text) > MAX_INPUT_CHARS:
        sys.stderr.write("error: input is %d characters; the limit is %d. Split it into parts.\n"
                         % (len(text), MAX_INPUT_CHARS))
        sys.exit(2)
    return text


def bar(value, width=24):
    filled = int(round(max(0, min(100, value)) / 100 * width))
    return "#" * filled + "." * (width - filled)


def say(lang, ar, en):
    """Pick the message language to match the text being analysed."""
    return ar if lang == "ar" else en
