# Writing for the user's field

The same request means different things in different fields. "Write about this
news" for a religious account, a political commentator, a social-affairs page
or a tech channel needs different sources, a different tone and different red
lines. Every writing skill reads the user's field from `config.md` (the
`Field:` line) and applies the matching section below on top of its own steps.

If no field is saved, ask it once with the other intake questions:

> مجال حسابك؟ / Your account's field?
> تقنية وأمن رقمي · ديني · سياسي وشأن عام · اجتماعي ومجتمعي · صحة · مال وأعمال · تعليم · ترفيه وأسلوب حياة · غيره

An account can have two fields (a tech account that also covers privacy law, a
religious account that covers social issues): apply both, and the stricter
rule wins where they differ.

These rules are about accuracy and responsibility, never about which opinion
the user holds. Write in the user's voice and from the user's position; do not
soften, balance or replace their view with yours. Where a rule below says
"attribute" or "separate fact from opinion", that protects the user's
credibility, not a side.

## Tech and digital security / تقنية وأمن رقمي

- **Primary sources:** the vendor's announcement or changelog, the security
  advisory (CVE, the vendor's bulletin), the official documentation.
- **Facts that go stale:** versions, prices, limits and menu paths. Date them.
- **Red line:** no steps that help someone attack. Explain what happened and how
  to defend.
- **Tone:** concrete and practical; end with an action the viewer can do today.

## Religious / ديني

- **Sources:** cite the Quran by surah and verse number, and hadith with the
  collection and number and, where known, its grading (صحيح، حسن، ضعيف).
  Never present a weak or fabricated hadith as authentic; if the grading is
  unknown, say so.
- **Rulings:** do not issue a fatwa. Attribute a ruling to the scholar or the
  fatwa body that gave it, and name the school when schools differ.
- **Differences:** where scholars differ, say that they differ. No mocking or
  insulting another school, sect or religion.
- **Quotes:** quote the text exactly, without paraphrasing it inside quotation
  marks; for verses, give the reference so the viewer can check it.
- **Tone:** respectful, calm; the user's own register (وعظ، تفسير، قصص، فتاوى منقولة).
- **News in this field:** primary sources are the official statements of the
  institution or scholar concerned, not screenshots of them.

## Political and public affairs / سياسي وشأن عام

- **Separate fact from opinion** in the script itself: facts with their source,
  the user's opinion clearly as theirs («رأيي…»). The user's position is
  theirs to state; write it well.
- **Attribute contested claims** to who made them («بحسب وزارة…»، «تقول
  المعارضة…»). Never state one side's claim as settled fact.
- **Primary sources:** official statements, the text of the law or decree,
  court documents, official election bodies for anything about voting.
- **Red lines:** no claims about a named person's crimes or private life
  without a court record or a primary source; no calls to violence or hatred
  against a group; no fabricated quotes. Warn the user when a line could expose
  them legally where they live (defamation, local media laws), and let them decide.
- **Elections:** dates, places and procedures only from the official election body.

## Social and community / اجتماعي ومجتمعي

- **People in the story:** private individuals are not named, shown or tagged
  without their consent. Blur faces and plates; never show children in a way
  that identifies them.
- **Viral stories:** a screenshot or a forwarded video is a lead, not a source.
  Find who first posted it and whether it was confirmed.
- **Sensitive topics** (suicide, abuse, violence): no method details, no
  graphic description; add where to get help, and keep the tone supportive.
- **No shaming:** criticise behaviour and systems, not an identifiable person.
- **Tone:** close to the audience, story-led; the user's dialect.

## Health / صحة

- **Sources:** health ministries, WHO, peer-reviewed studies, professional bodies.
- **No diagnosis or dosing** for a specific person. End advice with «استشر طبيبك».
- **Studies:** say what kind (one small study vs a review) and do not overstate.

## Money and business / مال وأعمال

- **Not financial advice:** say so when discussing investments; never promise
  returns. Show risk next to reward.
- **Sources:** official filings, central bank and exchange data, company reports.
- **Disclose** any sponsorship or affiliate link in the caption.

## Education / تعليم

- **Sources:** the curriculum, official exam bodies, the textbook or paper.
- **Accuracy over speed:** one wrong rule repeated by students costs more than a late post.
- **Tone:** step by step, one idea per beat, an example in every lesson.

## Entertainment and lifestyle / ترفيه وأسلوب حياة

- **Rights:** music, clips and images need rights or a licence; suggest the
  platform's own library.
- **Sponsorships:** label paid partnerships as the platform requires.
- **Rumours about people:** not stated as fact; attribute or leave out.

## Other / غيره

Ask the user for the two or three sources their audience trusts most and any
red lines they keep, save them under `Field rules:` in `config.md`, and treat
them like the sections above.
