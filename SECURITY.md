# Security / الأمان

## العربية

### ما الذي تضمنه هذه الحزمة

- كود Python بالمكتبة القياسية فقط: لا اتصال بالشبكة، ولا تشغيل أوامر نظام، ولا `eval`/`exec`، ولا مكتبات خارجية.
- الأدوات تقرأ النص الذي تعطيها إياه وتكتب فقط الملف الذي تحدده أنت (`-o` أو `--out`).
- ملفات التعليمات (`SKILL.md`) لا تطلب كلمات مرور، ولا تسجّل دخولاً نيابةً عنك، ولا تنشر أو ترسل شيئاً بنفسها.
- كل تعديل يمر بفحص تلقائي (`.github/workflows/check.yml`) يشغّل الاختبارات والفاحص الذاتي، ويرفض أي تعديل يضيف ما ذُكر أعلاه.

### ما الذي لا تضمنه

- الفاحص الذاتي يجد أنماطاً معروفة. لا يثبت أن الحزمة بريئة، ولا يغني عن قراءتك لملفات `SKILL.md`.
- لا أضمن أن قوائم الإعدادات في إنستقرام ستبقى كما هي. التطبيق يتغير.
- المقاييس (طبيعية النص، قوة الـ Hook، خطر الاحتيال) تقديرية، وليست كاشف ذكاء اصطناعي ولا حكماً نهائياً.

### كيف تثبّت بأمان

1. ثبّت إصداراً محدداً (`git checkout v1.0.0`) لا أحدث نسخة.
2. شغّل `python3 skills/ie-tools/selfcheck.py .` قبل النسخ.
3. اقرأ ملفات `SKILL.md` التي ستستخدمها.
4. بعد أي تحديث، اقرأ التغييرات (`git diff`) وأعد الفحص.

### الإبلاغ عن ثغرة

استخدم **Report a vulnerability** من تبويب Security في المستودع (إبلاغ خاص). لا تفتح Issue عاماً لثغرة قبل إصلاحها. اذكر: الملف والسطر، وما الذي يمكن فعله بها، وخطوات إعادة الإنتاج.

سأردّ بحسب وقتي كفرد، وأعدّل الإصدار وأذكر الإصلاح في ملاحظات الإصدار.

## English

### What this pack guarantees

- Standard-library Python only: no network, no process execution, no `eval`/`exec`, no third-party packages.
- Tools read the text you give them and write only the file you name (`-o` / `--out`).
- The `SKILL.md` files never ask for passwords, never log in for you, and never post or send anything.
- Every change goes through an automatic check (`.github/workflows/check.yml`) that runs the tests and the self-check and rejects changes that add any of the above.

### What it does not guarantee

- The self-check finds known patterns. It does not prove the pack is harmless, and it does not replace you reading the `SKILL.md` files.
- Instagram's menus change; step-by-step paths may drift.
- The scores (naturalness, hook strength, scam risk) are estimates, not an AI detector and not a verdict.

### Installing safely

1. Pin a release (`git checkout v1.0.0`), not the latest commit.
2. Run `python3 skills/ie-tools/selfcheck.py .` before copying.
3. Read the `SKILL.md` files you will use.
4. After any update, read the diff and re-run the check.

### Reporting a vulnerability

Use **Report a vulnerability** under the repository's Security tab (private). Please don't open a public issue for an unfixed problem. Include the file and line, what it enables, and how to reproduce it. This is a one-person project; I'll reply as time allows and credit the fix in the release notes.
