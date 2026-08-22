---
description: Create a new filament preset for the Kobra X from a few answers.
---

Create a new filament preset. Target printer is the Kobra X 0.4 unless
$ARGUMENTS says otherwise.

1. **Ask what you cannot read** (use AskUserQuestion, one round, not a
   sequence of turns): brand and product name, material type, the vendor's
   printed temperature range, and which of the four slots it is going into.
   If $ARGUMENTS already names the filament, use it and ask only the rest.
2. **Pick the parent** from the vendor tree by material — `Anycubic PLA @Kobra
   X 0.4 nozzle` for a standard PLA, `Anycubic PETG @...`, and so on. Never
   inherit from another user preset; the chain gets fragile.
3. **Write only what differs** from that parent. Every key you copy unchanged
   is a key that stops tracking vendor updates.
4. **Be conservative on flow.** Start at the parent's
   `filament_max_volumetric_speed`. Do not raise it on spec-sheet numbers —
   raising it is a separate decision that needs a flow test, per
   `WORKING_RULES.md` section 3.
5. **Write it** to `%APPDATA%\AnycubicSlicerNext\user\855643\filament\`, with a
   matching `.info` sidecar (copy an existing one, set `updated_time` to now,
   keep `base_id` from the parent). Slicer must be closed first.
6. **Run `--audit`** on the result before reporting done.
7. **Update `Filaments.md`** with the new slot contents.
