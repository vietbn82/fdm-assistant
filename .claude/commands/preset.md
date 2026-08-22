---
description: Show one preset's fully resolved values and what it overrides from its parent.
---

Show the preset named in $ARGUMENTS.

1. `python acslicer_tune.py --show "$ARGUMENTS"` for the resolved values.
   If the name is not found, run `--list` and suggest the closest matches.
2. Also read the raw user JSON so you can separate the two things:
   - **what this preset actually sets** (its own keys)
   - **what it inherits** from the parent named in `inherits`
   Present the overrides first. That short list is the preset's real content;
   everything else is vendor default.
3. For each override, say in one line what it does and what it trades away.
4. Flag anything that is pinned to a value identical to the parent — a
   no-op override that only makes the preset harder to keep in sync.
