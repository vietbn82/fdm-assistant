---
description: Apply approved preset changes from PENDING_APPLY.md, following the safety sequence.
---

Apply preset changes. `PENDING_APPLY.md` is the bucket; $ARGUMENTS names which IDs the
user approved (e.g. `P1 P4`, or `nhóm 2`). **Apply only what they named.**

If $ARGUMENTS is empty, do not apply anything — show the pending list grouped by
status and ask which IDs to run.

**Sequence — do not reorder, do not skip:**

1. **Check the slicer is closed.** Run
   `Get-Process | Where-Object { $_.ProcessName -match 'anycubic' }`.
   Running: stop, tell the user to close it. Do not kill it yourself unless
   they say so in this turn — it flushes memory to disk on exit and will erase
   whatever you write now.
2. **Re-read the current value** of every key you are about to change. `PENDING_APPLY.md`
   may be stale. If the "Hiện tại" column no longer matches, say so and stop —
   something changed the preset since the entry was written.
3. **Refuse the blocked ones.** Anything marked 🔴 has an unmet technical
   dependency; anything marked ⏳ needs its condition met first. Say which and why.
4. **Run the exact commands** from the approved entries. The backup happens
   inside `tools/acslicer_tune.py`.
5. **Verify** with `python tools/acslicer_tune.py --audit` — the change should
   not introduce a new finding.
6. **Move the applied entries** out of their group and into the
   "Đã áp dụng" section at the bottom of `PENDING_APPLY.md`, with the date and the
   backup path. Update `TODO.md` if an entry closes an item there.
7. **Report** the backup path and every changed key as `old -> new`.

❌ Do not commit. Say what changed and stop.

## Finding new problems

If the user asks for an audit rather than an apply, run
`python tools/acslicer_tune.py --audit --flow` and add anything new to
`PENDING_APPLY.md` as a proposal — do not write it to the presets.
