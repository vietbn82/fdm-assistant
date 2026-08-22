---
description: Audit every Anycubic user preset against firmware and filament limits. Read-only.
---

Audit the Anycubic Slicer Next presets. **Do not write anything.**

1. Run `python acslicer_tune.py --audit --flow` from the project root.
2. Report findings grouped by severity, most severe first. For each one say
   whether the value is something the user set or something inherited from the
   Anycubic vendor profile — the fix differs.
3. Cross-check anything speed- or temperature-related against the four loaded
   slots in `Filaments.md`. A finding on a preset for filament that is not
   loaded is lower priority; say so.
4. Skip `INFO` noise unless there is nothing more serious to report.
5. End with the standard **⚠️ ACTION REQUIRED** section. If nothing needs the
   user, say "None".

Arguments (optional): $ARGUMENTS — a preset name to restrict the report to.
