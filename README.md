# acslicer_tune

Reads Anycubic Slicer Next's preset store, resolves the full inheritance chain,
audits the resolved values against printer + filament physics, and optionally
writes fixes back.

Nothing here talks to the printer or the Anycubic cloud. It only touches files.

## Where the data lives

```
%APPDATA%\AnycubicSlicerNext\
  AnycubicSlicerNext.conf         app state + which machine/filament/process are paired
                                  (valid JSON followed by a "# MD5 checksum" line)
  system\Anycubic\{machine,process,filament}\*.json    read-only vendor presets
  user\<userid>\{machine,process,filament}\*.json      your presets (deltas via "inherits")
  user\<userid>\filament\base\*.json                   cached full snapshots - NOT the live preset
  user\<userid>\*.info                                 sync sidecar, holds updated_time
```

A user preset stores only the keys you changed plus `"inherits": "<parent name>"`.
The effective value of any setting is the flattened chain, which is what this
tool audits.

Two gotchas the tool handles:

- `filament\base\X.json` and `filament\X.json` share the same `"name"`. The
  top-level file is the live preset; the `base` copy must never win the index.
- Editing a `.json` without bumping `updated_time` in its `.info` sidecar lets
  cloud sync treat the file as stale and overwrite it. Every write bumps it.

**Close the slicer before writing.** It keeps presets in memory and flushes them
to disk on exit, clobbering outside edits.

## Usage

```bash
python acslicer_tune.py --list                  # every user preset + its parent
python acslicer_tune.py --show "<preset name>"  # fully resolved values
python acslicer_tune.py --audit                 # report only
python acslicer_tune.py --audit --flow          # + speeds the flow cap throttles
python acslicer_tune.py --audit --fix           # apply, after a full backup
python acslicer_tune.py --set "BBL PLA Lite|filament_max_volumetric_speed=15"
```

Every write first copies `user\` to `%APPDATA%\AnycubicSlicerNext\user_backup-tune-<tag>-<stamp>`.
Revert = delete `user\`, rename the backup back to `user`.

## What it checks

| Severity | Meaning |
|---|---|
| `ERR`  | internally inconsistent - the slicer or firmware will disagree with what you typed |
| `WARN` | valid but likely to hurt print quality |
| `FLOW` | speed exceeds the filament's volumetric cap, so the real speed is lower than the number shown (`--flow`) |
| `INFO` | cosmetic / leftover junk from preset copies |

Rules, by kind:

- **process** - layer height vs nozzle and `max_layer_height`; volumetric flow
  (`speed x layer_height x line_width` vs `filament_max_volumetric_speed`);
  speeds vs `machine_max_speed_x/y`; accelerations vs
  `machine_max_acceleration_extruding/travel`; overhang speed ladder must be
  non-increasing (0 means "disabled", not "stop"); outer wall not faster than
  inner; ironing speed/spacing; bridge flow; top/bottom shell thickness in mm;
  `support_top_z_distance` must be a whole number of layers.
- **filament** - nozzle temps inside the declared range; flow ratio sanity;
  pressure advance; absurd volumetric caps; bed above the softening point;
  first-layer bed cooler than later layers; stray pellet-extruder keys and
  `nil` values left behind by preset copies.
- **machine** - retraction length for a direct drive; negative
  `retract_restart_extra`; retraction speed; `z_hop` smaller than the layer it
  is supposed to clear.

## Known context for this setup (Anycubic Kobra X 0.4)

- Firmware limits: 450 mm/s X/Y, 10000 mm/s^2 travel accel, 6500 extruding,
  `max_layer_height` 0.28.
- Stock `Anycubic PLA @Kobra X` declares `filament_max_volumetric_speed` = 13,
  but Anycubic's own `0.20mm Standard` process asks for 27 mm3/s at the inner
  wall. The vendor profiles are internally inconsistent out of the box; the
  slicer silently throttles. `Anycubic PLA High Speed` uses 18 on the same
  hotend, which is the realistic ceiling for a well-behaved PLA.
