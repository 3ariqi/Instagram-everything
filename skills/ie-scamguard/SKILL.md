---
name: ie-scamguard
description: >-
  Analyse a suspicious Instagram DM, comment, email or link and tell the user
  what it is, how risky it is, and exactly what to do, in Arabic or English.
  Use when the user pastes a message and asks "is this a scam", "هل هذه رسالة
  احتيال", "وصلتني رسالة مشبوهة", "انتهاك حقوق", "توثيق الحساب", "رابط غريب",
  "someone asked for my code", or after clicking something they now doubt.
---

# ie-scamguard

The scams that hit creators are repetitive: a fake copyright notice with a
deadline, a fake verification offer, a "brand" asking for a fee, a "support"
account asking for a login code. They work because the victim is rushed. This
skill slows the moment down and names the trick.

**Files and language:** follow `<base>/../ie-setup/WORKSPACE.md`: read settings from the workspace, save the result in this skill's folder there, and use the language the user chose.

## Tool

```bash
echo "<the message>" | python3 <base>/../ie-tools/scamcheck.py -
python3 <base>/../ie-tools/scamcheck.py message.txt --json
```

It scores 0-100 from pattern signals (asks for a password or code, threatens
deletion or a copyright strike, offers verification, claims to be Instagram or
Meta, asks for money, a prize, moves you to WhatsApp or Telegram, urgency, asks
for a download) and from how each link is written (brand name on a domain the
brand does not own, look-alike spellings, punycode, raw IP, shorteners, odd
domain endings, plain http).

**It never opens, fetches or clicks anything.** Links are judged by their
spelling only. Do not open a suspicious link yourself to "see what it is", and
do not advise the user to either.

## First question, always

Ask: **"هل ضغطت على الرابط أو أرسلت أي رمز أو كلمة مرور؟"** / "Did you tap the
link, or send any code or password?"

- **No:** go to the analysis.
- **Yes:** skip the analysis and go to *If they already acted* below.

## The analysis

1. Run `scamcheck.py` on the exact text.
2. Tell the user the verdict in one line, then the two or three reasons that
   mattered, in plain words. Use the checker's `why` text.
3. Name the scam type if it matches a known one:

| pattern | what it really is |
| --- | --- |
| "copyright violation, appeal within 24h" | login-theft page dressed as an appeal form |
| "you are eligible for the blue badge" | verification is requested inside the app only |
| "send us the code we texted you" | they are logging into the account right now and need your code |
| "brand collab, pay a small fee / install this app" | advance-fee fraud, or spyware in an APK |
| "support team: your account will be deleted" | Instagram does not open DMs with you |
| "you won, claim here" | a prize for a contest nobody entered |

4. Say what to do (the checker prints it): do not tap, do not reply, report the
   account inside the chat, block. Official notices appear inside the app, so
   open the app yourself and look there, not through the message.
5. **"No strong signs" is not "safe".** Say it. A careful scammer writes
   clean messages. If anything still feels off, treat it as suspicious.

## If they already acted

Calmly, in order, and do not shame them: this happens to security
professionals too.

1. **Changed nothing yet?** Open the app yourself (not through the link) and
   change the password now. Choose a long, unique one.
2. In Accounts Center, review where the account is logged in and **log out of
   every session you don't recognise**.
3. Check the email linked to the account: if it was changed, use the "this
   wasn't me" link in the old email and Instagram's recovery flow.
4. Turn on two-factor with an authenticator app (`/ie-harden`).
5. If they sent a code: assume the account is being accessed right now and do
   steps 1 to 3 immediately.
6. If they paid money: contact the bank or payment provider at once and keep
   the screenshots. Report to the national cybercrime authority.
7. Warn followers if the account sent messages while compromised.

Never ask the user to paste a password, a code or a recovery key into this
chat. If they offer, stop them.

## Screenshots and privacy

Ask the user to blur other people's names and numbers before sharing a scam
screenshot publicly. For content, the scam message itself is useful material
(`/ie-reel`, formula #1), with the sender's handle hidden.

## Output

```
SCAM LIKELY  ████████████████░░░░ 78/100

Why: fake copyright notice (+30), "appeal" link on instagram-appeal.xyz,
a domain Instagram does not own (+45), 24-hour deadline (+10).
Type: login-theft "appeal" page.
Do now: don't tap · report and block in the chat · check notices inside the app.
```
