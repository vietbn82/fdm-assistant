#!/usr/bin/env python3
"""SessionStart: report the state Claude needs before touching any preset.

Claude starts every session with no memory of the last one. This injects the
three facts that decide whether a write is safe right now:
  - is the slicer holding the presets open?
  - when was the last backup, and how many are piling up?
  - what does git think changed?
"""
import glob
import json
import os
import re
import subprocess
import time

ROOT = os.path.join(os.environ.get("APPDATA", ""), "AnycubicSlicerNext")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run(args, cwd=None):
    try:
        r = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                           timeout=10)
        return r.stdout.strip()
    except Exception:
        return ""


def slicer_running():
    out = run(["tasklist", "/FI", "IMAGENAME eq AnycubicSlicerNext.exe", "/NH"])
    return "AnycubicSlicerNext" in out


def main():
    lines = []

    if not os.path.isdir(ROOT):
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "Anycubic Slicer Next config dir not found.",
        }}))
        return

    lines.append("SLICER: RUNNING - do not write presets, ask the user to close it"
                 if slicer_running() else
                 "SLICER: closed - safe to write presets")

    # copytree carries the source mtime across, so the directory timestamp is
    # the preset tree's age, not the backup's. The name holds the real one.
    baks = sorted(os.path.basename(p)
                  for p in glob.glob(os.path.join(ROOT, "user_backup-*")))
    if baks:
        stamped = [b for b in baks if re.search(r"(\d{8})-(\d{6})$", b)]
        newest = max(stamped, key=lambda b: re.search(r"(\d{8})-(\d{6})$",
                                                      b).group(0)) \
            if stamped else baks[-1]
        when = ""
        m = re.search(r"(\d{8})-(\d{6})$", newest)
        if m:
            t = time.mktime(time.strptime(m.group(0), "%Y%m%d-%H%M%S"))
            hrs = (time.time() - t) / 3600
            when = f", {hrs:.0f}h ago" if hrs < 48 else f", {hrs/24:.0f}d ago"
        lines.append(f"BACKUPS: {len(baks)} total, newest {newest}{when}")
    else:
        lines.append("BACKUPS: none")

    n = len(glob.glob(os.path.join(ROOT, "user", "*", "*", "*.json")))
    lines.append(f"USER PRESETS: {n} json files")

    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=REPO)
    dirty = run(["git", "status", "--porcelain"], cwd=REPO)
    if branch:
        state = f"{len(dirty.splitlines())} uncommitted" if dirty else "clean"
        lines.append(f"GIT: {branch}, {state}")
        last = run(["git", "log", "-1", "--format=%h %s (%cr)"], cwd=REPO)
        if last:
            lines.append(f"LAST COMMIT: {last}")

    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "Anycubic project status:\n" + "\n".join(
            "  " + x for x in lines),
    }}))


if __name__ == "__main__":
    main()
