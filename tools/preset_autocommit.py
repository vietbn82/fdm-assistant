#!/usr/bin/env python3
"""Mirror the live preset store into presets\\ and commit it, unattended.

Runs from a Windows scheduled task. The trigger is "the slicer is not running",
not "a file changed": Anycubic Slicer Next keeps presets in memory and rewrites
them on exit, so anything captured while it is open may be a state it is about
to overwrite. Waiting until the process is gone is what makes the snapshot real.

Scope is deliberately narrow. This only ever stages presets\\ - it will refuse
to run if anything else is staged, and it never touches docs, tools or config.
The remote is public, so it also refuses to commit a file that looks like it
carries a credential.

Exit codes: 0 nothing to do or committed fine, 1 refused, 2 error.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MIRROR_REL = "presets"
LOG = REPO / ".git" / "preset-autocommit.log"
PROCESS = "AnycubicSlicerNext.exe"

# The remote is public. Nothing matching these may be committed unattended.
SECRET_PATTERNS = [
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),   # email
    re.compile(r"\baccess[_-]?token\b", re.I),
    re.compile(r"\brefresh[_-]?token\b", re.I),
    re.compile(r"\bpassword\b", re.I),
    re.compile(r"\bsecret\b", re.I),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\"]+", re.I),                  # local path
]


def log(msg):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{stamp}  {msg}"
    print(line)
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                       text=True, timeout=120)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} -> {r.returncode}: "
                           f"{r.stderr.strip()}")
    return r.stdout.strip()


def slicer_running():
    r = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {PROCESS}", "/NH"],
                       capture_output=True, text=True, timeout=30)
    return PROCESS.lower() in r.stdout.lower()


def scan_for_secrets(paths):
    hits = []
    for rel in paths:
        p = REPO / rel
        if not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for pat in SECRET_PATTERNS:
            m = pat.search(text)
            if m:
                hits.append(f"{rel}: {pat.pattern}")
                break
    return hits


def summarize(paths):
    """One line naming what actually changed, so the log is readable."""
    kinds = {}
    for rel in paths:
        parts = Path(rel).parts
        if len(parts) >= 2:
            kinds[parts[1]] = kinds.get(parts[1], 0) + 1
    return ", ".join(f"{n} {k}" for k, n in sorted(kinds.items())) or "presets"


def main():
    if not (REPO / ".git").exists():
        log("ERROR: not a git repo"); return 2

    if slicer_running():
        log("skip: slicer is running, its presets are not final yet"); return 0

    # Refuse to run alongside unrelated staged work.
    staged = [l for l in git("diff", "--cached", "--name-only").splitlines() if l]
    outside = [l for l in staged if not l.startswith(MIRROR_REL + "/")]
    if outside:
        log(f"REFUSED: {len(outside)} file(s) already staged outside "
            f"{MIRROR_REL}/ - {outside[:3]}"); return 1

    sys.path.insert(0, str(REPO / "tools"))
    try:
        import acslicer_tune as t
        t.export_presets()
    except Exception as e:
        log(f"ERROR: export failed: {e}"); return 2

    # Ask git, not the export delta: a previous run may have written the mirror
    # without committing it, and that still needs to be recorded.
    dirty = [l for l in git("status", "--porcelain", "--", MIRROR_REL)
             .splitlines() if l]
    if not dirty:
        log("no change"); return 0

    rels = [l[3:].strip().strip('"') for l in dirty]
    secrets = scan_for_secrets(rels)
    if secrets:
        log(f"REFUSED: possible sensitive content, not committing: {secrets}")
        return 1

    git("add", "--", MIRROR_REL)

    # Nothing outside presets/ may reach the commit, even by accident.
    staged = [l for l in git("diff", "--cached", "--name-only").splitlines() if l]
    outside = [l for l in staged if not l.startswith(MIRROR_REL + "/")]
    if outside:
        git("reset", "--", MIRROR_REL, check=False)
        log(f"REFUSED: staging escaped {MIRROR_REL}/: {outside[:3]}"); return 1

    msg = (f"chore(presets): sync after slicer close - {summarize(staged)}\n\n"
           f"Captured automatically once Anycubic Slicer Next exited, so the "
           f"files are the version it flushed to disk rather than a mid-session\n"
           f"state. {len(staged)} file(s) changed.\n\n"
           f"Automated snapshot - no explanation of intent. Changes made through "
           f"a Claude session carry that in their own commit message.")
    git("commit", "-m", msg)
    head = git("log", "-1", "--format=%h %s")
    log(f"committed {len(staged)} file(s): {head}")

    try:
        git("push")
        log("pushed")
    except Exception as e:
        log(f"WARN: commit is local, push failed: {e}")
        return 0
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        log(f"ERROR: {e}")
        sys.exit(2)
