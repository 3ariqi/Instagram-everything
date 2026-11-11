---
name: ie-harden
description: >-
  Walk the user through securing an Instagram account step by step, in Arabic
  or English: two-factor, sessions, recovery, linked apps, team access, and
  what to do before an account is lost. Use when the user says "secure my
  account", "account hacked", "protect my instagram", "تأمين الحساب", "حماية
  حسابي", "التحقق بخطوتين", "حسابي انسرق", or after a scam attempt.
---

# ie-harden

A checklist the user does on their own phone, one step at a time. Claude
cannot see the account and must not ask for access to it.

**Files and language:** follow `<base>/../ie-setup/WORKSPACE.md`: read settings from the workspace, save the result in this skill's folder there, and use the language the user chose.

## Rules

- **Never ask for the password, a login code, a backup code or a recovery key,
  in any form.** If the user pastes one, tell them to change it now and stop
  using it.
- **Never log in or operate the account.** The user taps; Claude explains.
- **Menu names change between app versions and languages.** Describe each step
  by what it does and give the usual place to look, then tell the user to use
  the app's own search box in Settings if a label differs. Do not state a menu
  path as exact.
- If the user says the account is compromised right now, go to *Emergency*.

## Emergency (account taken over)

1. Use Instagram's own "Forgot password" flow from the login screen, not a link
   from a message.
2. If the email was changed, look for a "secure your account" or "this wasn't me"
   message from Instagram in the **original** email inbox and use it from there.
3. Use the app's account-recovery flow for hacked accounts, and keep screenshots
   and dates for the report.
4. Once back in: password, sessions, 2FA and linked apps, as below.
5. Tell followers through another channel that the account was compromised, and
   not to trust messages sent during that time.

## The checklist, in order of value

**1. The email account behind it (most important)**
Whoever controls the email can reset everything. Make sure that mailbox has its
own strong password and two-factor, and is not used for anything risky.

**2. A password nobody can guess and nowhere else used**
Long (15+ characters), unique, from a password manager. Not a variation of an
old one. Change it if it was ever shared, even once.

**3. Two-factor authentication, with an authenticator app**
Prefer an authenticator app or a hardware security key over SMS text codes,
because SIM-swap attacks can redirect SMS. Where the app offers passkeys, those
are stronger still. Find it in Settings → Accounts Center → Password and
security (or search "two-factor" inside Settings). **Save the backup codes
offline**, on paper or in a password manager, not in the phone's notes.

**4. Sessions: where the account is logged in**
In the same security area, review the logged-in devices and log out of any you
don't recognise. Repeat monthly.

**5. Login alerts**
Turn on alerts for unrecognised logins. Check that the contact email and phone
on the account are yours.

**6. Linked apps and websites**
Remove third-party apps you no longer use, especially "follower analytics",
"who viewed my profile" and giveaway tools. They are a common way in.

**7. Team and agency access**
If more than one person manages the account, use Instagram's own access
controls (Meta Business tools) so people don't share one password. Remove
people who left.

**8. Official email check**
Instagram's security messages should also be visible inside the app (the
account security area). A message that only exists in an email, with a link to
act on within hours, deserves suspicion: check inside the app instead.

**9. Recovery plan, before you need it**
Write down offline: the email used, the backup codes' location, and who you
would contact. Do it now, not after.

## Output

Run it as a conversation, not a wall: one step, wait for "done", next step.
Offer the full checklist as a file the user can save, with checkboxes.

```
الخطوة 3 من 9: التحقق بخطوتين بتطبيق مصادقة
افتح الإعدادات ثم مركز الحسابات ثم كلمة المرور والأمان
(إن اختلف الاسم عندك فابحث عن «التحقق بخطوتين» في مربع بحث الإعدادات)
اختر تطبيق المصادقة، وامسح الرمز، واحفظ رموز الطوارئ على ورقة.
قل لي «تم» حين تنتهي.
```

## Content idea

A short Reel: "٥ دقائق تحمي حسابك" is a natural `/ie-reel` (formula #10),
filmed on a test account, never on the user's real one with real data visible.
