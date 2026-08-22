#!/usr/bin/env python3
"""PreToolUse guard: refuse any write that lands in the vendor preset tree.

Anycubic ships system\\Anycubic\\{machine,process,filament}\\*.json read-only.
Editing them breaks slicer updates and cannot be reverted from a user backup.
WORKING_RULES.md says "never touch system\\"; this makes it a hard stop.

Reads the PreToolUse payload on stdin, prints a deny decision if the target is
inside the vendor tree, otherwise prints nothing and exits 0 (= no opinion).
"""
import json
import os
import re
import sys

SYSTEM_DIR = os.path.join(
    os.environ.get("APPDATA", ""), "AnycubicSlicerNext", "system"
)


def norm(p):
    return os.path.normcase(os.path.normpath(p or ""))


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)          # unparseable payload: stay out of the way

    tool = payload.get("tool_name", "")
    inp = payload.get("tool_input", {}) or {}
    guard = norm(SYSTEM_DIR)
    if not guard:
        sys.exit(0)

    # Write / Edit / NotebookEdit carry an explicit path
    path = inp.get("file_path") or inp.get("notebook_path")
    if path and norm(path).startswith(guard):
        deny(f"{tool} targets the read-only Anycubic vendor preset tree "
             f"({SYSTEM_DIR}). WORKING_RULES.md forbids this. Copy the preset "
             f"into user\\ and edit the copy instead.")

    # Shell tools: look for the vendor path inside the command string
    cmd = inp.get("command") or ""
    if cmd:
        hay = norm(cmd).replace("/", "\\")
        needle = guard.replace("/", "\\")
        if needle in hay:
            writes = r"(>|>>|\bcp\b|\bmv\b|\brm\b|\bsed\b\s+-i|Set-Content|" \
                     r"Out-File|Remove-Item|Copy-Item|Move-Item|New-Item)"
            if re.search(writes, cmd, re.IGNORECASE):
                deny(f"This command writes into the read-only Anycubic vendor "
                     f"preset tree ({SYSTEM_DIR}). WORKING_RULES.md forbids it. "
                     f"Reading is fine; writing is not.")

    sys.exit(0)


if __name__ == "__main__":
    main()
