#!/usr/bin/env python3
import json
import os
import shutil
import sys
import time

KIT = os.path.dirname(os.path.abspath(__file__))
CLAUDE = os.path.join(os.path.expanduser("~"), ".claude")
CLAUDE_MD = os.path.join(CLAUDE, "CLAUDE.md")
SETTINGS = os.path.join(CLAUDE, "settings.json")
START = "<!-- ste100-writing:start -->"
END = "<!-- ste100-writing:end -->"
REMINDER_TAG = "STE100"
REMINDER = (
    "Apply the STE100 writing rules from the session instructions. "
    "Before returning the answer, check for short sentences, active voice, "
    "one idea per sentence, and unnecessary words."
)


def read(path):
    if not os.path.exists(path):
        return ""
    with open(path) as f:
        return f.read()


def write(path, text):
    with open(path, "w") as f:
        f.write(text)


def backup(path):
    if os.path.exists(path):
        shutil.copy2(path, path + ".bak-" + time.strftime("%Y%m%d-%H%M%S"))


def read_settings():
    text = read(SETTINGS)
    if not text.strip():
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        sys.exit(SETTINGS + " is not valid JSON (" + str(error) + "). Fix it, then run this script again.")


def write_settings(settings):
    write(SETTINGS, json.dumps(settings, indent=2) + "\n")


def has_command(groups, tag):
    return any(tag in hook.get("command", "") for group in groups for hook in group.get("hooks", []))


def reminder_command():
    payload = json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": REMINDER,
        }
    })
    return "printf '%s' '" + payload.replace("'", "'\\''") + "'"


def install():
    os.makedirs(CLAUDE, exist_ok=True)
    settings = read_settings()

    claude_md = read(CLAUDE_MD)
    if START in claude_md:
        print("Writing rules:      already installed")
    else:
        rules = read(os.path.join(KIT, "writing-rules.md")).strip()
        backup(CLAUDE_MD)
        separator = "\n\n" if claude_md.strip() else ""
        write(CLAUDE_MD, claude_md.rstrip() + separator + START + "\n" + rules + "\n" + END + "\n")
        print("Writing rules:      added to ~/.claude/CLAUDE.md")

    hooks = settings.setdefault("hooks", {})
    changed = False

    prompt_hooks = hooks.setdefault("UserPromptSubmit", [])
    if has_command(prompt_hooks, REMINDER_TAG):
        print("Reminder hook:      already installed")
    else:
        prompt_hooks.append({"hooks": [{"type": "command", "command": reminder_command(), "timeout": 5}]})
        changed = True
        print("Reminder hook:      added to ~/.claude/settings.json")

    if changed:
        backup(SETTINGS)
        write_settings(settings)

    print("\nDone. Start a new Claude Code session to load the changes.")


def uninstall():
    settings = read_settings()
    claude_md = read(CLAUDE_MD)
    if START in claude_md and END in claude_md:
        backup(CLAUDE_MD)
        before = claude_md[: claude_md.index(START)].strip("\n")
        after = claude_md[claude_md.index(END) + len(END):].strip("\n")
        parts = [part for part in (before, after) if part.strip()]
        write(CLAUDE_MD, "\n\n".join(parts) + ("\n" if parts else ""))
        print("Writing rules:      removed from ~/.claude/CLAUDE.md")
    else:
        print("Writing rules:      not installed")

    hooks = settings.get("hooks", {})

    def is_ours(hook):
        command = hook.get("command", "")
        return REMINDER_TAG in command

    removed = sum(1 for groups in hooks.values() for group in groups for hook in group.get("hooks", []) if is_ours(hook))
    if removed:
        cleaned = {
            event: [
                {**group, "hooks": [hook for hook in group.get("hooks", []) if not is_ours(hook)]}
                for group in groups
                if any(not is_ours(hook) for hook in group.get("hooks", []))
            ]
            for event, groups in hooks.items()
        }
        cleaned = {event: groups for event, groups in cleaned.items() if groups}
        if cleaned:
            settings["hooks"] = cleaned
        else:
            settings.pop("hooks", None)
        backup(SETTINGS)
        write_settings(settings)
        print("Hooks:              removed " + str(removed) + " from ~/.claude/settings.json")
    else:
        print("Hooks:              not installed")

    print("\nDone. Start a new Claude Code session to load the changes.")


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "install":
        install()
    elif command == "uninstall":
        uninstall()
    else:
        sys.exit("Usage: ste.py install | ste.py uninstall")


main()
