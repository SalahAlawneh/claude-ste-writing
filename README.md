# Simple English for Claude Code

This kit makes Claude Code write in Simplified Technical English. It follows the ASD-STE100 principles: short sentences, active voice, one idea per sentence, and no unnecessary words.

It keeps technical terms. Words such as *webhook*, *idempotency* and *coroutine* stay.

## What it installs

1. **Writing rules.** The installer adds a section to `~/.claude/CLAUDE.md`. Claude Code reads this file at the start of every session, in every project.
2. **A reminder before every answer.** The installer adds a `UserPromptSubmit` hook to `~/.claude/settings.json`. Each time you send a message, the hook adds one sentence that tells Claude to apply the rules. Without it, the rules fade in long sessions.

## Requirements

- macOS or Linux
- Claude Code
- `python3`

## Install

```bash
cd claude-ste-writing
./install.sh
```

Then start a new Claude Code session.

The installer backs up each file before it changes it. Backup files use the suffix `.bak-YYYYMMDD-HHMMSS`. You can run the installer more than once; it never adds a duplicate.

If `~/.claude/settings.json` is not valid JSON, or if its `hooks` section has an unexpected shape, the installer stops before it changes your files.

## Check that it works

In a new session, run `/hooks`. The `UserPromptSubmit` event lists the reminder.

## Remove

```bash
./uninstall.sh
```

This removes the rules section and the reminder hook. It keeps all your other settings.

## Limits

The reminder is text. It makes simple English more likely, but nothing checks the answer. If an answer reads badly, tell Claude "STE" and ask for a rewrite.

## Files

| File | Purpose |
|---|---|
| `install.sh` | Installs the kit |
| `uninstall.sh` | Removes the kit |
| `EXPLAINER.md` | Explains how the two parts work |
| `kit/writing-rules.md` | The rules that go into `CLAUDE.md` |
| `kit/ste.py` | The install and uninstall logic |
