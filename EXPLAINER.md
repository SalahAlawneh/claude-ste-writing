# The STE100 Writing Stack

This kit uses two advisory mechanisms to push Claude Code toward Simplified Technical English:

| Item | Value |
|---|---|
| Mechanisms | 2 installed |
| Enforcement | Advisory only |
| Scope | All projects on this machine |

## The problem this solves

A rule in `CLAUDE.md` is read once, when the session starts. It then sits at the top of the context while the conversation grows beneath it. Nothing checks whether Claude Code obeys it.

So the rule works early and fades later. The fix is not a better rule. The fix is to move the rule closer to the moment Claude Code writes.

## When each mechanism fires

| Time | Mechanism | Effect |
|---|---|---|
| Session start | The rules load | Once per session. The distance to the answer grows all session long. |
| Every message you send | The reminder is injected | Once per prompt, immediately before Claude Code answers. |

Both mechanisms are advisory. They remind Claude Code to write clearly.

## The two mechanisms

### 1. The rules themselves

Location: `~/.claude/CLAUDE.md`

A section named `Writing: Simplified Technical English` holds the rules, three worked examples, and a self-check list. It applies to every project on this machine, in every Git worktree.

One adjustment separates this kit from the published standard: it asks for ASD-STE100 principles, not the restricted vocabulary. Technical terms such as `idempotency`, `webhook`, `coroutine`, and `rate limiter` stay.

### 2. The per-message reminder

Location: `hooks.UserPromptSubmit` in `~/.claude/settings.json`

This hook runs every time you send a message. It prints one JSON object, and Claude Code injects the text into the context directly ahead of the answer. You type nothing.

It costs one `printf` and about forty tokens per message. It does not eliminate drift, but it reduces the distance that causes drift.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Apply the STE100 writing rules from the session instructions. Before returning the answer, check for short sentences, active voice, one idea per sentence, and unnecessary words."
  }
}
```

## What the rules ask for

ASD-STE100 documentation states its guidance as paired examples. These three pairs are written into the installed rules.

| Not approved | Approved |
|---|---|
| The application will perform an evaluation of the incoming request prior to the execution of the synchronization process. | The application checks the request before it starts the synchronization. |
| In the event that synchronization is unsuccessful, the operation will be retried. | If synchronization fails, retry the operation. |
| This issue may potentially occur due to the fact that the connection has already been terminated. | This issue can occur because the connection is already closed. |

The rules behind those pairs:

- Write short sentences under 20 to 25 words.
- Put one main idea in each sentence.
- Use active voice.
- Use simple words outside technical terms.
- Avoid idioms.
- Use the same word for the same concept every time.
- Make every reference unambiguous.

## Where this still fails

Prose cannot be enforced by this kit. Claude Code's sentences go straight to the terminal, and no tool call exists to inspect them before you read them.

| Failure mode | Why it happens |
|---|---|
| Long sessions | The rules sit far above the work. The per-message hook shortens that distance but does not remove the effect. |
| Quoting and relaying | Error output, log lines, and subagent reports arrive in their own voice, and Claude Code may carry that voice forward. |
| Matching a house style | A formal PR template or a file's existing voice can pull against the rules. |
| Uncertainty | Hedging produces the vague wording the rules forbid. |
| Mid-turn work | The reminder fires once per message, not once per tool call, so a long turn gets it only at the start. |

## Operating it

Run `/hooks` to see, edit, or remove the reminder hook. It lives in `~/.claude/settings.json`, so it affects only your machine.

Two manual controls remain:

- Say `STE` and ask Claude Code to rewrite the last answer.
- Say `long session` and ask Claude Code to re-run the checklist before the next answer.

The files touched by this kit are `~/.claude/CLAUDE.md` and `~/.claude/settings.json`.
