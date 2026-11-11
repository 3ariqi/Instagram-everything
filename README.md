# Instagram Everything

[![Release](https://img.shields.io/github/v/release/3ariqi/Instagram-everything?label=%D8%A7%D9%84%D8%A5%D8%B5%D8%AF%D8%A7%D8%B1)](https://github.com/3ariqi/Instagram-everything/releases/latest)
[![Checks](https://github.com/3ariqi/Instagram-everything/actions/workflows/check.yml/badge.svg)](https://github.com/3ariqi/Instagram-everything/actions/workflows/check.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**حزمة مهارات لوكلاء الذكاء الاصطناعي (Claude Code وCodex وGemini CLI) تدير محتوى إنستقرام بالعربي أولاً، وتفحص نفسها أمنياً.**

21 مهارة تكتب سكربتات الريلز والكابشن والكاروسيل والستوري، وتبحث عمّا ينجح في مجالك، وترد على التعليقات والرسائل، وتكشف رسائل الاحتيال، وتؤمّن حسابك، وتحوّل أخبار مجالك (تقني، ديني، سياسي، اجتماعي...) إلى محتوى موثّق المصادر.

> مشروع من إعداد **م.أحمد طاهر** · [@3ariqi](https://github.com/3ariqi) · [3ariqi.com](https://3ariqi.com)
> تابعنا على منصات التواصل الاجتماعي: يوتيوب، إنستقرام، تيك توك، X — **@3ariqi**

---

## ثبّت في دقيقة

انسخ هذا الرابط وأرسله لوكيلك (Claude Code أو Codex أو Gemini CLI) وقل له: **«نزّل وثبّت»**

```
https://github.com/3ariqi/Instagram-everything
```

سيسألك عن اللغة (عربي أو إنجليزي) وعن المجلد الذي تريد العمل فيه، ثم يفحص الحزمة ويثبّتها ويخبرك بالمسار. بعدها افتح الوكيل من ذلك المجلد وقل: «ابدأ».

## الدليل المصوّر

- [دليل المستخدم (PDF)](docs/user-guide.pdf): لكل شخص، بلا أوامر برمجية: ماذا تفعل الحزمة، كيف تبدأ، أمثلة محادثة كاملة.
- [دليل المبرمجين (PDF)](docs/developer-guide.pdf): البنية، التثبيت لكل وكيل، الأدوات بمخرجاتها الحقيقية، والفحص الأمني.

## الإصدار الحالي: v1.1.0

- **مجلد عمل مرتّب:** مجلد لكل نوع من العمل (ريلز، كابشن، أخبار، تقارير...)، وملف «ابدأ-هنا»، والحزمة نفسها في مجلد منفصل لا يُعدَّل.
- **لغتك من أول خطوة:** تختار العربية أو الإنجليزية عند التثبيت، فتصبح بها أسماء المجلدات والملفات وكل تعامل المساعد معك.
- **أنت تختار مكان التثبيت:** مجلد عمل، أو لكل مشاريعك، أو مجلد وكيل آخر.
- **أخبار لأي مجال:** `/ie-news` يتحقق من ثلاثة مصادر ويكتب بأسلوب مجالك وخطوطه الحمراء، وكل مهارات الكتابة تتكيف مع مجالك.
- **تحليل الأداء بطريقتين:** ترفق لقطات الشاشة، أو تسمح للمساعد بقراءة صفحة «رؤى» حسابك بنفسه (قراءة فقط).
- **بصمة لكل ملف:** تكشف أي تعديل على الحزمة بعد التثبيت، والمثبّت يرفض النسخة المعدّلة.

كل الإصدارات وملاحظاتها في [صفحة الإصدارات](https://github.com/3ariqi/Instagram-everything/releases).

## لماذا هذه الحزمة؟

| | الحزم المعتادة | Instagram Everything |
| --- | --- | --- |
| اللغة | إنجليزي فقط، وأدواتها تُفسد النص العربي | عربي وإنجليزي، تفهم الترقيم العربي واللهجات |
| الإيموجي المركّبة (👨‍💻 🇾🇪) | تُكسر | تبقى سليمة |
| الأمان | ثق بنا | فحص ذاتي تلقائي مع كل تعديل، وأمر `/ie-selfcheck` تشغّله بنفسك |
| النشر على إنستقرام | — | لا تنشر ولا ترسل أي شيء نيابةً عنك. أنت من ينشر |
| الحماية من الاحتيال | — | `/ie-scamguard` و`/ie-harden` |
| الأخبار في أي مجال | — | `/ie-news` يتحقق من ثلاثة مصادر، ويكتب حسب مجالك (تقني، ديني، سياسي، اجتماعي...) |
| المنصات | إنستقرام | إنستقرام + تيك توك + يوتيوب شورتس + X |

## المهارات

### الكتابة
| الأمر | الوظيفة |
| --- | --- |
| `/ie-reel` | سكربت ريل كامل: خيارات افتتاحية (Hook) مقيّمة، ونص بتوقيت كل لقطة |
| `/ie-caption` | كابشن يتوقف في المكان الصحيح قبل «المزيد»، مع 5 هاشتاقات أو أقل (الحد الذي أعلنته إنستقرام تدريجياً) |
| `/ie-carousel` | كاروسيل شريحة بشريحة، من الغلاف إلى دعوة الفعل |
| `/ie-story` | تسلسل ستوري بملصقات تفاعلية |
| `/ie-profile` | تقييم البايو والصورة والهايلايت وتحسينها |
| `/ie-plan` | خطة أسبوعية مبنية على أدائك الفعلي |

### التفاعل
| الأمر | الوظيفة |
| --- | --- |
| `/ie-comment` | تعليق له رأي على منشورات الآخرين، لا «منشور رائع» |
| `/ie-reply` | فرز تعليقات منشورك والرد على ما يستحق |
| `/ie-dm` | رسائل خاصة تحصل على رد، بلا رسائل جماعية |

### البحث والتحليل
| الأمر | الوظيفة |
| --- | --- |
| `/ie-viral` | يبحث عمّا ينجح في مجالك ويرتّبه بمقارنته بمتوسط كل حساب |
| `/ie-audit` | تحليل ما نشرته: ما الذي نجح ولماذا، وما الذي تتوقف عنه |
| `/ie-repurpose` | يحوّل مقالاً أو فيديو طويلاً إلى عدة منشورات |
| `/ie-crosspost` | يكيّف المحتوى نفسه لتيك توك ويوتيوب شورتس وX |

### الجودة
| الأمر | الوظيفة |
| --- | --- |
| `/ie-natural` | ينظّف النص من العبارات الآلية المكررة بالعربي والإنجليزي، ويقيس طبيعية الأسلوب |

### الأمان والأخبار والتحديث
| الأمر | الوظيفة |
| --- | --- |
| `/ie-scamguard` | يحلل رسالة أو تعليقاً مشبوهاً: انتهاك حقوق مزيف، توثيق مزيف، تعاون احتيالي، تصيّد |
| `/ie-harden` | قائمة تأمين الحساب خطوة بخطوة |
| `/ie-news` | خبر من مجالك ← تحقق من 3 مصادر ← سكربت ريل + كابشن بالمصادر، بأسلوب مجالك وخطوطه الحمراء |
| `/ie-selfcheck` | يفحص الحزمة نفسها قبل التثبيت وبعد أي تحديث |
| `/ie-update` | يفحص عند بدء كل جلسة هل صدر إصدار جديد، ويحدّث بعد اجتياز الفحص الأمني |

### الإعداد والمونتاج

| الأمر | ماذا يفعل |
| --- | --- |
| `/ie-setup` | أسئلة اختيارية عن حسابك ولهجتك، ثم يتعلّم أسلوبك من منشوراتك ويحفظه |
| `/ie-edit` | خطة مونتاج ريل: اللقطات والقطعات والنصوص على الشاشة بتوقيت محسوب |

قبل أي كتابة أو مونتاج تسألك المهارة أسئلة **اختيارية** (المنصة، الأسلوب، الطول، الجمهور...). تجاوز ما شئت وتستخدم المحفوظ. وعند موافقتك الصريحة فقط تحفظ إجاباتك كقالب في `الإعدادات/presets.md` داخل مجلد عملك، وتتعلم أسلوبك من تعديلاتك على المسودات.

## لأي وكيل ذكاء اصطناعي (Claude وCodex وGemini وغيرها)

أرسل للوكيل رابط المستودع وقل له: «نزّل وثبّت هذه المهارات». ملف [`AGENTS.md`](AGENTS.md) يشرح له الخطوات بالترتيب: يجلب أحدث وسم إصدار، **ويسألك عن اللغة (عربي أو إنجليزي) وعن مكان مجلد العمل**، ثم ينزّل نسخة مؤقتة ويفحصها، ولا يثبّت إلا إذا نجح الفحص، ثم يحذف النسخة المؤقتة ويخبرك بالمسارات.

### شكل مجلد العمل بعد التثبيت

```
D:\AI-Work\instagram\          ← المجلد الذي اخترته
├── ابدأ-هنا.md               ← افتحه أولاً: شرح كل مجلد وكيف تبدأ
├── 00-ملفاتي\                ← ضع هنا لقطات التحليلات والتصدير ومنشوراتك القديمة
├── 01-ريلز\                  ← سكربتات الريلز وخطط المونتاج
├── 02-كابشن\
├── 03-كاروسيل-وستوري\
├── 04-تعليقات-وردود\
├── 05-أخبار\
├── 06-نشر-وإعادة-استخدام\
├── 07-تقارير\                ← تحليل الأداء، خطة الأسبوع، البايو
├── 08-حماية\
├── الإعدادات\                ← حسابك وأسلوبك واختياراتك المحفوظة
└── .claude\skills\           ← الحزمة نفسها (لا تعدّل فيها)
```

كل ناتج يُحفظ في مجلده باسم التاريخ والموضوع، مثل `2026-11-11-سرقة-الحسابات.md`. وإن اخترت الإنجليزية تصبح الأسماء `01-reels` و`START-HERE.md` وهكذا، ويتعامل معك المساعد بالإنجليزية.

افتح المساعد من هذا المجلد نفسه حتى يرى المهارات (Claude Code يقرأ `.claude/skills`، وCodex وGemini CLI يقرآن `.agents/skills`).

أو ثبّت بنفسك بعد `git clone --depth 1 --branch <وسم>`:

```bash
python3 -I install.py --workspace "D:/AI-Work/instagram" --agent claude --lang ar   # كل شيء في مجلد واحد
python3 -I install.py --workspace "D:/AI-Work/instagram" --agent all --lang ar      # لـClaude Code وCodex معاً
python3 -I install.py --global --agent claude --lang en                            # المهارات لكل مشاريعك
python3 -I install.py --dest <مجلد مهارات وكيل آخر> --workspace <مجلد> --lang ar
```

**هل عدّل أحد الحزمة؟** كل إصدار فيه بصمة لكل ملف. شغّل
`python3 -I <مجلد المهارات>/ie-tools/selfcheck.py --verify <مجلد المهارات>`
فيخبرك أي ملف تغيّر بالضبط، أو `INTACT` إن لم يتغير شيء.

المثبّت يفحص الحزمة أولاً ويرفض التثبيت إن فشل الفحص. الأدوات بايثون فقط، فالوكلاء التي لا تشغّل أوامر (مثل المحادثات العادية) تقرأ ملفات `SKILL.md` وتطبّقها يدوياً بلا الأرقام.

**التحديث:** مهارة `ie-update` تفحص عند بدء كل جلسة هل صدر إصدار جديد. إن وُجد جلبته وفحصته وثبّتته تلقائياً بعد نجاح الفحص، وتسأل أولاً عند تغيّر الرقم الرئيسي. يمكنك ضبط `updates: ask` أو `off` في ملف الإعدادات.

## كيف أفعّل المهارات وأستخدمها؟ (خطوة بخطوة)

1. **ثبّت**: أرسل للوكيل رابط المستودع وقل «نزّل وثبّت». سيسألك عن اللغة وعن مكان مجلد العمل.
2. **افتح محادثة جديدة من مجلد العمل** (أو أعد تشغيل الوكيل)، فالمهارات لا تُحمَّل في محادثة كانت مفتوحة قبل التثبيت. وافتح `ابدأ-هنا.md` لتعرف كل مجلد.
3. **تأكد أنها ظهرت:** في Claude Code و Codex و Gemini CLI اكتب `/skills` وابحث عن أسماء تبدأ بـ `ie-`.
4. **ابدأ بالإعداد:** اكتب `/ie-setup` (في Codex: `$ie-setup`)، أو قل ببساطة «ابدأ» أو «تعلّم أسلوبي». أجب عمّا تريد وألصق 3 إلى 10 من منشوراتك.
5. **اطلب بكلامك العادي:** «اكتب لي ريل عن حماية الحساب». الوكيل يفهم من وصف المهارة أي واحدة يشغّل، أو نادِها بالاسم: `/ie-reel` في Claude Code، `$ie-reel` في Codex، وفي Gemini CLI تُفعَّل تلقائياً حسب الوصف.
6. **أجب عن الأسئلة الاختيارية** أو تجاوزها. في آخر العمل يعرض عليك الوكيل حفظ اختياراتك قالباً، فتصبح المرة القادمة أسرع.
7. **للمونتاج:** بعد السكربت اطلب `/ie-edit` وستحصل على خطة اللقطات والقطعات.

**في claude.ai (المحادثة العادية):** ارفع مجلد المهارة مضغوطاً (ZIP) من الإعدادات ثم المهارات، وفعّل تنفيذ الأكواد. الأدوات المشتركة `ie-tools` تحتاج أن تكون بجوار المهارات، وهذا لم أتحقق منه هناك. إن لم تعمل فالمهارات تُطبَّق يدوياً بلا الأرقام (راجع AGENTS.md).

## كيف يتم الربط بحسابك؟

**الحزمة لا تطلب منك كلمة مرور ولا رمز تحقق ولا توكن، أبداً.** وفي تحليل الأداء (`/ie-audit`) أنت تختار الطريقة:

1. **ترفق لقطات شاشة أو ملف تصدير** من «رؤى» (Insights)، أو تنسخ الأرقام. ضعها في مجلد `00-ملفاتي` ويقرؤها المساعد من هناك.
2. **تسمح للمساعد يتصفح صفحة «رؤى» حسابك بنفسه**، إن كان عنده متصفح يتحكم فيه. أنت تسجّل الدخول بنفسك، وهو يقرأ فقط: لا يضغط متابعة ولا إعجاب ولا نشر ولا يغيّر أي إعداد، ويتوقف عند أي شاشة دخول أو تحقق لتكملها أنت. يقرأ حسابك فقط وبهدوء، لأن الجمع الآلي مخالف لشروط إنستقرام. ثم يعرض لك جدول الأرقام التي قرأها قبل أن يحللها، لتصحح أي رقم.

- **موصّل (Connector) في وكيلك:** إن ربطت حسابك بنفسك من واجهة الوكيل، يستخدم المساعد وظائف القراءة فقط.
- **القاعدة:** إن طلب منك أي وكيل كلمة مرور إنستقرام أو رمز تحقق أو رمز استرداد فارفض.

## التثبيت الآمن

**ثبّت إصداراً محدداً، لا «أحدث نسخة».** هذا يضمن أن ما تثبّته هو ما فُحص:

```bash
git clone --depth 1 --branch v1.1.0 https://github.com/3ariqi/Instagram-everything.git
cd Instagram-everything
python3 -I skills/ie-tools/selfcheck.py .      # افحص قبل النسخ
python3 -I install.py --workspace <مجلدك> --agent claude --lang ar
```

أو كإضافة في Claude Code:

```
/plugin marketplace add 3ariqi/Instagram-everything
/plugin install instagram-everything@instagram-everything
```

ثم شغّل `/ie-selfcheck` بعد التثبيت وبعد كل تحديث.

## الإعداد

الأسهل أن تشغّل `/ie-setup`. أو يدوياً: انسخ `templates/config.md` إلى مجلد `الإعدادات` داخل مجلد عملك (`settings` إن اخترت الإنجليزية) واملأه: مجالك، لغتك ولهجتك، أسلوبك، جمهورك، وتوقيعك الذي يُضاف لنهاية السكربتات والكابشن. كل المهارات تقرأه.

## الأدوات

كل الأدوات في `skills/ie-tools/` مكتوبة بـ Python بالمكتبة القياسية فقط:

- **بلا اعتماديات خارجية**، وبلا اتصال بالشبكة، وبلا تشغيل أوامر نظام.
- تعمل على جهازك، ولا يُرفع أي نص لأي جهة.
- تفهم العربية والإنجليزية: تقطيع الكلمات، الترقيم، زمن النطق، والإيموجي المركّبة.

```bash
python3 skills/ie-tools/hookscore.py --hook "لا أحد يخبرك أن كلمة مرورك تسربت"
python3 skills/ie-tools/clean.py draft.txt --report
python3 skills/ie-tools/score.py draft.txt
python3 skills/ie-tools/scamcheck.py message.txt
```

## الأمان

- **لا تسجيل دخول نيابةً عنك، ولا طلب كلمات مرور، ولا كشط آلي، ولا نشر أو إرسال تلقائي.** هذه قواعد مكتوبة داخل كل مهارة.
- كل تعديل على المستودع يمر بفحص تلقائي (GitHub Actions) يرفض: الاتصال بالشبكة، تشغيل الأوامر، `eval`/`exec`، الأحرف الخفية، وعبارات حقن الأوامر.
- الفرع الرئيسي محمي: لا يمكن حذفه ولا الكتابة فوق تاريخه، وكل إصدار له وسم ثابت تثبّت منه.
- للإبلاغ عن ثغرة: استخدم **Report a vulnerability** من تبويب Security (إبلاغ خاص)، وراجع [SECURITY.md](SECURITY.md).

## الرخصة

MIT — استخدمها وطوّرها وانشرها، مع الإبقاء على ملف الرخصة.

---

## English

[![Release](https://img.shields.io/github/v/release/3ariqi/Instagram-everything)](https://github.com/3ariqi/Instagram-everything/releases/latest)

**Instagram Everything** is an Arabic-first pack of 21 agent skills (Claude Code, Codex, Gemini CLI and others) for running an Instagram account, with built-in security checks.

**Quick install:** send `https://github.com/3ariqi/Instagram-everything` to your agent and say "download and install". It asks your language (Arabic or English) and where to put your workspace, audits the pack, installs it and tells you the path.

- Reels, captions, carousels, stories, profile, weekly plan, comments, replies, DMs, research, audits, repurposing and cross-posting.
- Security and news: `/ie-scamguard` (scam message analysis), `/ie-harden` (account hardening), `/ie-news` (3-source fact-checked news in any field, written for that field), `/ie-selfcheck` (audits the pack itself), `/ie-update` (safe updates).
- v1.1.0: an organised workspace (one folder per kind of work, a START-HERE file, the pack kept apart), language chosen at install, field-aware writing, performance audits from screenshots or read-only browsing, and a SHA-256 manifest that detects any change to the installed pack.
- Unicode-aware tools: Arabic tokenization, Arabic punctuation, ZWJ emoji preserved.
- Standard-library Python only. No network, no subprocess, nothing uploaded. Nothing is posted or sent on your behalf.
- CI rejects network code, process execution, hidden Unicode and prompt-injection phrases on every change. `main` is protected against deletion and force pushes.

Manual install of the pinned release:

```bash
git clone --depth 1 --branch v1.1.0 https://github.com/3ariqi/Instagram-everything.git
cd Instagram-everything
python3 -I skills/ie-tools/selfcheck.py .
python3 -I install.py --workspace <folder> --agent claude --lang en
```

Guides: [user guide](docs/user-guide.pdf) and [developer guide](docs/developer-guide.pdf) (Arabic, PDF). Report vulnerabilities privately via **Report a vulnerability** under the Security tab ([SECURITY.md](SECURITY.md)).

By **Ahmed Taher** ([@3ariqi](https://github.com/3ariqi) · [3ariqi.com](https://3ariqi.com)). MIT licensed.
