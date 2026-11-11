# What each platform allows

Read the user's platform line out to them before they choose **send** mode for
it. Checked in November 2026; platforms change these rules, so if a platform
shows something different, believe the platform.

The common thread: **every platform's terms forbid automating its website or
app without permission.** Sending replies through the browser is the user's
own choice, made with this in view. Draft mode, or an official connector,
avoids the problem.

| platform | official way to reply by software | browser automation | risk if it goes wrong |
| --- | --- | --- | --- |
| Instagram | Yes: the Instagram API can read, reply to, hide and delete comments on a professional account's own posts (a connector you authorised) | The terms forbid collecting information in an automated way without permission, and Meta's spam rules target engaging at very high frequency | Actions limited for a while ("try again later"); repeated, an account restriction |
| YouTube | Yes: the YouTube Data API, with the channel owner's consent (a connector) | The terms forbid accessing the service by any automated means without YouTube's prior written permission | Comments held, features limited, or channel action |
| TikTok | No public API for comment replies | The terms forbid bots that extract content; the international terms also forbid automated scripts that interact with the service | Comment limits, reduced reach, or a ban |
| X | Only through the X API, and automated replies are allowed only to people who asked for them | The rules forbid "scripting the X website" and warn this "may result in the permanent suspension" of the account | **Permanent suspension**: keep X in draft mode |

## What to say before send mode (one platform at a time)

> **<platform>:** what the platform says (from the table). The pack keeps it
> slow (40 to 120 seconds between replies), small (at most N a night), and
> stops at the first warning, but it cannot promise the account will not be
> limited. Do you want me to send replies by myself on <platform>? (yes / no,
> keep drafts)

Only a clear yes counts. Write the date as `consent:` on that platform's line.

## Sources

- Instagram API, comment moderation: https://developers.facebook.com/documentation/instagram-platform/comment-moderation
- Instagram terms (automated collection, Nov 2021 change): https://opentermsarchive.org/en/memos/instagram-blocks-data-retrieval-and-clarifies-what-information-it-retrieves/
- YouTube terms of service: https://www.youtube.com/terms
- X automation rules: https://help.x.com/en/rules-and-policies/x-automation
- Platform rules compared (Instagram, TikTok, YouTube, X): https://www.blotato.com/research/social-media-automation-rulebook
