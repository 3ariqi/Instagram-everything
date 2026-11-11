#!/usr/bin/env python3
"""
scamcheck.py - read a suspicious DM, comment or email and score the risk.
Arabic and English. Nothing is opened, fetched or clicked: links are judged
by how they are written, never by visiting them.

Signals (data/scam_patterns.json): asks for a password or login code,
threatens deletion or a copyright strike, offers verification, claims to be
Instagram/Meta support, asks for money, a prize too good to be true, moves you
to WhatsApp/Telegram, pressure and deadlines, asks you to download a file.

Link checks: a brand name (instagram, meta...) on a domain that is not the
brand's own, look-alike spellings, punycode (xn--) domains, raw IP addresses,
link shorteners, unusual top-level domains, plain http.

Verdicts: SCAM LIKELY (60+), SUSPICIOUS (25-59), NO STRONG SIGNS (under 25).
"No strong signs" is not "safe". These are heuristics.

Usage:
  python3 scamcheck.py message.txt
  echo "..." | python3 scamcheck.py -
  python3 scamcheck.py message.txt --json
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import textkit as tk  # noqa: E402

PATTERNS = os.path.join(HERE, "data", "scam_patterns.json")
HOST_RE = re.compile(r"(?:https?://)?(?:www\.)?([^/\s:?#]+)", re.IGNORECASE)
BARE_DOMAIN_RE = re.compile(r"(?<![@\w.])((?:[a-z0-9-]+\.)+(?:com|net|org|info|xyz|top|click|live|online|site|ru|tk|ml|ga|cf|gq|me|io|co|app|link|zip|mov|icu|buzz|cam|rest|ly|gl|gd|at|cc|id)\b)(/\S*)?", re.IGNORECASE)


def load_patterns(path=PATTERNS):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def registered_domain(host):
    parts = host.lower().strip(".").split(".")
    if len(parts) >= 3 and parts[-2] in ("co", "com", "org", "net", "gov", "edu") and len(parts[-1]) == 2:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def find_hosts(text):
    hosts = []
    for m in tk.URL_RE.finditer(text):
        h = HOST_RE.match(m.group(0))
        if h:
            hosts.append(h.group(1).lower())
    for m in BARE_DOMAIN_RE.finditer(text):
        host = m.group(1).lower()
        if host not in hosts and not any(host in h for h in hosts):
            hosts.append(host)
    return hosts


def check_link(host, pat):
    risk, reasons = 0, []
    official = set(pat["official_domains"])
    reg = registered_domain(host)
    is_official = reg in official or host in official
    label = host.replace("-", "").replace(".", "")
    if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host):
        risk += 35
        reasons.append(("رابط يشير إلى عنوان IP مباشرة بدل اسم موقع", "link points at a raw IP address"))
    if "xn--" in host:
        risk += 35
        reasons.append(("نطاق بترميز punycode قد يخفي أحرفاً مشابهة للأصل", "punycode domain, can disguise look-alike letters"))
    if not is_official:
        brand = [b for b in pat["brand_words"] if b in label]
        if brand:
            risk += 45
            reasons.append(("يستخدم اسم «%s» في نطاق ليس تابعاً له (%s)" % (brand[0], reg),
                            "uses \"%s\" on a domain it does not own (%s)" % (brand[0], reg)))
        lure = [w for w in pat["lure_words"] if w in label]
        if lure and not brand:
            risk += 20
            reasons.append(("كلمة طُعم في النطاق: %s" % lure[0], "lure word in the domain: %s" % lure[0]))
    if reg in pat["shorteners"] or host in pat["shorteners"]:
        risk += 15
        reasons.append(("رابط مختصر يخفي الوجهة الحقيقية", "shortened link hides the real destination"))
    tld = host.rsplit(".", 1)[-1]
    if tld in pat["risky_tlds"]:
        risk += 10
        reasons.append(("امتداد نطاق شائع في الاحتيال (.%s)" % tld, "top-level domain common in scams (.%s)" % tld))
    return {"host": host, "official": is_official, "risk": risk, "reasons": reasons}


def analyse(text, pat=None):
    pat = pat or load_patterns()
    lang = tk.lang_of(text)
    folded = tk.fold(text)
    hits = []
    for s in pat["signals"]:
        matched = [p for p in s["match_ar"] + s["match_en"] if re.search(p, folded)]
        if not matched:
            continue
        weight = s["weight"]
        req = [s.get("request_ar"), s.get("request_en")]
        if any(req) and not any(r and re.search(r, folded) for r in req):
            weight = weight // 2  # mentioned, not requested
        hits.append(dict(s, weight=weight))
    score = sum(s["weight"] for s in hits)
    links = [check_link(h, pat) for h in find_hosts(text)]
    risky = sorted((l["risk"] for l in links if l["risk"] >= 25), reverse=True)
    score += max((l["risk"] for l in links), default=0) + 10 * max(len(risky) - 1, 0)
    if any(re.search(r"http://", u, re.IGNORECASE) for u in tk.URL_RE.findall(text)):
        score += 5
    # A login link plus a request for a code is the textbook takeover
    ids = {s["id"] for s in hits}
    if any(not l["official"] for l in links) and ids & {"credentials", "account_threat", "badge_offer", "impersonation"}:
        score += 15
    score = min(100, score)
    verdict = "SCAM_LIKELY" if score >= 60 else "SUSPICIOUS" if score >= 25 else "NO_STRONG_SIGNS"
    return {"lang": lang, "score": score, "verdict": verdict, "signals": hits, "links": links}


VERDICT = {
    "SCAM_LIKELY": ("احتيال مرجّح", "SCAM LIKELY"),
    "SUSPICIOUS": ("مشبوه", "SUSPICIOUS"),
    "NO_STRONG_SIGNS": ("لا مؤشرات قوية (وهذا لا يعني أنه آمن)", "NO STRONG SIGNS (not the same as safe)"),
}
ADVICE_AR = [
    "لا تضغط أي رابط في الرسالة، ولا ترسل أي رمز وصلك.",
    "تحقق من الرسائل الرسمية من داخل تطبيق إنستقرام نفسه، لا من الرسالة.",
    "أبلغ عن الحساب واحظره من داخل المحادثة.",
    "إن كنت ضغطت الرابط أو أعطيت رمزاً: غيّر كلمة المرور فوراً وشغّل /ie-harden.",
]
ADVICE_EN = [
    "Don't tap any link in it, and don't send any code you received.",
    "Check official notices inside the Instagram app itself, not through the message.",
    "Report and block the account from the chat.",
    "If you already tapped or shared a code: change your password now and run /ie-harden.",
]


def render(r):
    ar = r["lang"] != "en"
    i = 0 if ar else 1
    print("")
    print("  %s   %s %d/100" % (VERDICT[r["verdict"]][i], tk.bar(r["score"]), r["score"]))
    if r["signals"]:
        print("\n  " + ("المؤشرات:" if ar else "signals:"))
        for s in r["signals"]:
            print("   - %s (+%d)" % (s["label_ar"] if ar else s["label_en"], s["weight"]))
            print("     %s" % (s["why_ar"] if ar else s["why_en"]))
    if r["links"]:
        print("\n  " + ("الروابط:" if ar else "links:"))
        for l in r["links"]:
            tag = ("رسمي" if ar else "official") if l["official"] else ("غير رسمي" if ar else "not official")
            print("   - %s  [%s]  +%d" % (l["host"], tag, l["risk"]))
            for ra, re_ in l["reasons"]:
                print("     %s" % (ra if ar else re_))
    if r["verdict"] != "NO_STRONG_SIGNS":
        print("\n  " + ("ماذا تفعل:" if ar else "what to do:"))
        for a in (ADVICE_AR if ar else ADVICE_EN):
            print("   - " + a)
    print("\n  " + ("فحص تقديري بالأنماط؛ لم يُفتح أي رابط." if ar else "Pattern-based estimate; no link was opened.") + "\n")


def main():
    tk.utf8_stdio()
    ap = argparse.ArgumentParser(description="Score a suspicious message (Arabic/English).")
    ap.add_argument("input", nargs="?", default="-")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    text = tk.read_input(args.input)
    if not text.strip():
        print("error: no message to analyse (paste the message text, or a file name, or - for stdin)", file=sys.stderr)
        sys.exit(2)
    r = analyse(text)
    if args.json:
        out = dict(r)
        out["signals"] = [{"id": s["id"], "weight": s["weight"], "label_ar": s["label_ar"], "label_en": s["label_en"]}
                          for s in r["signals"]]
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        render(r)


if __name__ == "__main__":
    main()
