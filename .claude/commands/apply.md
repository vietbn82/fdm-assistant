---
description: Audit then apply preset fixes, following the WORKING_RULES.md safety sequence.
---

Apply preset fixes. Follow `WORKING_RULES.md` section 2 and 3 exactly.

**Sequence — do not reorder, do not skip:**

1. **Check the slicer is closed.** Run
   `Get-Process | Where-Object { $_.ProcessName -match 'anycubic' }`.
   If it is running: stop here, tell the user to close it, do not kill it
   yourself unless they say so in this turn. It flushes memory to disk on exit
   and will erase anything written now.
2. **Dry run first.** `python acslicer_tune.py --audit --flow` and show what
   would change.
3. **Split the findings** by the table in `WORKING_RULES.md` section 3:
   - internal inconsistencies and leftover junk → apply
   - anything touching speed, flow, temperature, retraction → ask first
   - never `system\`, never `.conf`
4. **Apply** with `python acslicer_tune.py --audit --fix` (add `--flow` only if
   the user asked for flow clamps — remember these belong in the filament
   preset, not the process preset).
5. **Report** the backup path and every changed key as `old -> new`.
6. If the repo is clean otherwise, offer to commit the docs change describing
   what was tuned and why. Do not push without asking.

Arguments (optional): $ARGUMENTS — restrict to one preset, or `--flow` to
include flow clamps.
