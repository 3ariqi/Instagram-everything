# Instagram Everything

**حزمة مهارات لـ Claude تدير محتوى إنستقرام بالعربي أولاً، وتفحص نفسها أمنياً.**

18 مهارة تكتب سكربتات الريلز والكابشن والكاروسيل والستوري، وتبحث عمّا ينجح في مجالك، وترد على التعليقات والرسائل، وتكشف رسائل الاحتيال، وتؤمّن حسابك، وتحوّل الأخبار التقنية إلى محتوى موثّق المصادر.

> مشروع من إعداد **م.أحمد طاهر** · [@3ariqi](https://github.com/3ariqi)
> تابعنا على منصات التواصل الاجتماعي: يوتيوب، إنستقرام، تيك توك، X — **@3ariqi**

---

## لماذا هذه الحزمة؟

| | الحزم المعتادة | Instagram Everything |
| --- | --- | --- |
| اللغة | إنجليزي فقط، وأدواتها تُفسد النص العربي | عربي وإنجليزي، تفهم الترقيم العربي واللهجات |
| الإيموجي المركّبة (👨‍💻 🇾🇪) | تُكسر | تبقى سليمة |
| الأمان | ثق بنا | فحص ذاتي تلقائي مع كل تعديل، وأمر `/ie-selfcheck` تشغّله بنفسك |
| النشر على إنستقرام | — | لا تنشر ولا ترسل أي شيء نيابةً عنك. أنت من ينشر |
| الحماية من الاحتيال | — | `/ie-scamguard` و`/ie-harden` |
| الأخبار التقنية | — | `/ie-technews` يتحقق من ثلاثة مصادر قبل كتابة أي سكربت |
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

### الأمان والأخبار (جديدة كلياً)
| الأمر | الوظيفة |
| --- | --- |
| `/ie-scamguard` | يحلل رسالة أو تعليقاً مشبوهاً: انتهاك حقوق مزيف، توثيق مزيف، تعاون احتيالي، تصيّد |
| `/ie-harden` | قائمة تأمين الحساب خطوة بخطوة |
| `/ie-technews` | خبر تقني ← تحقق من 3 مصادر ← سكربت ريل + كابشن بالمصادر |
| `/ie-selfcheck` | يفحص الحزمة نفسها قبل التثبيت وبعد أي تحديث |

## التثبيت الآمن

**ثبّت إصداراً محدداً، لا «أحدث نسخة».** هذا يضمن أن ما تثبّته هو ما فُحص:

```bash
git clone https://github.com/3ariqi/instagram-everything.git
cd instagram-everything
git checkout v1.0.0
python3 skills/ie-tools/selfcheck.py .      # افحص قبل النسخ
cp -r skills/ie-* ~/.claude/skills/
```

أو كإضافة في Claude Code:

```
/plugin marketplace add 3ariqi/instagram-everything
/plugin install instagram-everything@instagram-everything
```

ثم شغّل `/ie-selfcheck` بعد التثبيت وبعد كل تحديث.

## الإعداد

انسخ `templates/config.md` إلى `~/.claude/instagram/config.md` واملأه: لغتك ولهجتك، أسلوبك، جمهورك، وتوقيعك الذي يُضاف لنهاية السكربتات والكابشن. كل المهارات تقرأه.

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
- للإبلاغ عن ثغرة: راجع [SECURITY.md](SECURITY.md).

## شكر

الفكرة مستوحاة من [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) (رخصة MIT). هذه الحزمة أعيد بناؤها من الصفر: الكود والمهارات والبيانات مكتوبة من جديد بدعم العربية وطبقة أمان كاملة.

## الرخصة

MIT — استخدمها وطوّرها وانشرها، مع الإبقاء على ملف الرخصة.

---

## English

**Instagram Everything** is an Arabic-first pack of 18 Claude skills for running an Instagram account, with built-in security checks.

- Reels, captions, carousels, stories, profile, weekly plan, comments, replies, DMs, research, audits, repurposing and cross-posting.
- New: `/ie-scamguard` (scam message analysis), `/ie-harden` (account hardening), `/ie-technews` (3-source fact-checked tech news to Reel), `/ie-selfcheck` (audits the pack itself).
- Unicode-aware tools: Arabic tokenization, Arabic punctuation, ZWJ emoji preserved.
- Standard-library Python only. No network, no subprocess, nothing uploaded. Nothing is posted or sent on your behalf.
- CI rejects network code, process execution, hidden Unicode and prompt-injection phrases on every change.

Install a pinned release (`git checkout v1.0.0`), run `python3 skills/ie-tools/selfcheck.py .`, then copy `skills/ie-*` into `~/.claude/skills/`.

By **Ahmed Taher** ([@3ariqi](https://github.com/3ariqi)). Inspired by [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) (MIT), rebuilt from scratch. MIT licensed.
