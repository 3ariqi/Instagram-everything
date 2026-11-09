---
name: ie-dm
description: >-
  Write Instagram DMs that get replies, in Arabic or English: the keyword
  delivery, the first message to someone who engaged, a collab pitch, two
  follow-ups, and a safe reply to brand offers. Use when the user says "DM this
  person", "what do I send", "رسالة خاص", "اكتب لي رسالة", "تعاون", "pitch",
  "follow up", or has received a collaboration offer.
---

# ie-dm

## Check inbound offers first

If the user is replying to a message they **received** (a collab offer, a
brand deal, "support", a prize), run it through the scam checker before
writing anything:

```bash
echo "<their message>" | python3 <base>/../ie-tools/scamcheck.py -
```

If the verdict is SUSPICIOUS or SCAM LIKELY, hand over to `/ie-scamguard`
instead of drafting a friendly reply. Real brands send a company email from
their own domain, name a person, and never ask for an upfront fee, a password
or a login code.

## The three DMs worth writing

1. **The reply to a raised hand.** They commented the keyword, answered a
   poll, replied to a Story. They moved first. Most DMs worth sending are this.
2. **The warm approach.** Someone whose posts the user has genuinely engaged
   with for weeks.
3. **The collab pitch.** A specific idea for a specific account, with a reason
   it is them.

Cold messages to strangers who never interacted are the lowest-yield use of
the hour. Say so, offer the alternative (two weeks of real comments first),
then write it if they still want it.

## Before writing, ask in one batch

1. Who: handle, what they do, what started this.
2. The trigger: the actual reason to message today.
3. What the user wants: a conversation, a sale, a collab.

No trigger, no message. Say so.

## Keyword delivery

```
{name}، تفضّل: {the thing or where to find it}.
{one line on how to use it}
{an optional question they can answer in a few words}
```

Deliver first, with no gate. "Before I send it, what do you do?" is a bait and
switch and people remember it.

Automated keyword replies are allowed for professional accounts through
Instagram's own tools or an approved partner. Bulk messages to people who did
not interact are not, and they get accounts restricted.

## The warm first message

- Two to four sentences. Reference the specific thing, in their words.
- Give before asking: an answer, a tip, a resource.
- One small ask. No link and no calendar in message one.

## The collab pitch

Four lines: what you've watched them do, the specific idea, what they get,
what you need from them. Be concrete about who does what.

## Follow-ups: two, then stop

- **+4 days:** add something new. Never "just checking".
- **+10 days:** close the loop politely and say you'll stop.

## Never

- Never automate outreach, never message on a schedule people who didn't
  interact.
- Never invent a mutual, a shared experience or having watched something.
- Never put a pitch in the same message as a compliment.
- Never ask anyone for a password, a code or payment details, and never send
  your own.

## Output

The message, its character count, and the two follow-ups with their days, all
run through `<base>/../ie-tools/clean.py`. The user sends each one by hand.
