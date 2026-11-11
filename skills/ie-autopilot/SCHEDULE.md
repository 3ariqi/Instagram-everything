# Setting up the scheduled run

The autopilot needs one thing from the agent: start a new session in the user's
workspace folder at a set time and give it the prompt `/ie-autopilot run`
(Claude Code). For agents that do not take slash commands, use the plain
prompt `Use the ie-autopilot skill in run mode.` The run reads and writes files
in the workspace, so it must run **on the user's computer, in that folder**.

Agents change their scheduling features often. Before giving the user steps,
check your own current documentation or `--help`; the notes below were checked in
November 2026 and are a starting point, not a promise.

## Rules

1. Show the user exactly what will be created: the tool, the time, the folder,
   the prompt, and the permissions the run gets. Create it only on a clear yes.
2. Least permissions: the run needs to read and write files in the workspace,
   and web search for `ie-news`. It never needs a browser, a login or
   permission to run anything outside the workspace.
3. Pick a minute that is not :00 or :30 (for example 08:40), so the run does not
   compete with everyone else's.
4. Record the result under `## Scheduler` in `autopilot.md`: which tool, the
   task's name, the time, and how to pause or remove it.
5. Run once right away so the user sees a real result and approves any
   permission prompt (choose "always allow" for file writes in the workspace).

## Claude Code

- **Desktop app, local scheduled task (best fit).** Runs on the computer with
  the workspace's files, starts a fresh session on schedule, and keeps working
  after restarts. In the app: Code tab, **Scheduled**, **New task**, turn on
  **Only on this computer**, pick the workspace as the folder, prompt
  `/ie-autopilot run`, schedule Daily at the chosen time (or Custom with a cron
  line). The user can also ask Claude in any desktop session to create it.
  It only fires while the app is open and the computer awake; a missed run is
  caught up once on wake, which is why `due --once-per-day` exists.
- **Cloud scheduled tasks:** not suitable. They run on a fresh copy in the
  cloud, without the workspace on the user's computer.
- **`/loop`:** not suitable. It lives only while that session stays open and
  recurring loops expire after seven days.
- **Terminal only (no desktop app):** use the operating system's scheduler
  (below) with `claude -p "/ie-autopilot run"` started in the workspace folder,
  with permissions limited to editing files in that folder.

## Codex

- **Codex app automations:** schedule a task in the workspace with the prompt
  `Use the ie-autopilot skill in run mode.` They work best while the computer is
  awake and Codex is running.
- **CLI only:** the operating system's scheduler with
  `codex exec --sandbox workspace-write "Use the ie-autopilot skill in run mode."`
  started in the workspace folder.

## Gemini CLI and other agents

No built-in scheduler. Use the operating system's scheduler with the agent's
non-interactive mode, started in the workspace folder, for example
`gemini --approval-mode auto_edit -p "Use the ie-autopilot skill in run mode."`. Check `--help` first:
these flags have changed between versions. Prefer a mode that auto-approves
file edits only, never one that approves everything.

## The operating system's scheduler

Write a small script in `<settings>/` that changes to the workspace folder and
starts the agent's command, show it to the user, and register it only on a yes:

- **Windows:** Task Scheduler. `schtasks /Create /SC DAILY /ST 08:40 /TN "ie-autopilot" /TR "<script path>"`.
  Remove with `schtasks /Delete /TN "ie-autopilot"`.
- **macOS:** a LaunchAgent plist in `~/Library/LaunchAgents/` with
  `StartCalendarInterval`, loaded with `launchctl`.
- **Linux:** one `crontab -e` line: `40 8 * * * cd "<workspace>" && <command>`.

The computer must be on at that time. The agent also has to be signed in on the
computer, as it is for any normal session.

## No scheduler at all

Some assistants (chat apps, or a computer that is rarely on) cannot run on a
schedule. Say so plainly. The autopilot still works: at the start of every
session it checks the queue and offers to prepare what is due, and the user can
say "prepare what's due" (جهّز المستحق) at any time.
