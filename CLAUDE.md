# Anycubic Kobra X — slicer config assistant

This repo manages **Anycubic Slicer Next presets for a Kobra X 0.4**, not
application code. The presets themselves live outside the repo, in
`%APPDATA%\AnycubicSlicerNext\`.

## Read these before acting

| File | When |
|---|---|
| `TODO.md` | first, every session — everything still open, and who it is blocked on |
| `WORKING_RULES.md` | before any write to a preset — the safety sequence and the ask/don't-ask table are binding |
| `Device_Software.md` | printer limits, data layout, known vendor-profile bugs |
| `Filaments.md` | what is actually loaded in the four slots right now |
| `PRINT_PROFILES.md` | the three print purposes and which preset serves each |
| `README.md` | how `acslicer_tune.py` works |
| `CAPABILITIES.md` | what is automated and what is still manual |

## Non-negotiable

1. **Close the slicer before writing presets.** It holds them in memory and
   flushes on exit, erasing outside edits. Check with `Get-Process`.
2. **Back up `user\` before every write.** `acslicer_tune.py` does this; if you
   write by hand, do it yourself.
3. **Bump `updated_time` in the `.info` sidecar** of any preset JSON you edit,
   or cloud sync treats the file as stale and reverts it.
4. **Never write to `system\`.** A PreToolUse hook blocks it. Copy into
   `user\` and edit the copy.
5. **Never write `.conf`** unless you recompute the trailing MD5. It contains
   cloud tokens — filter `anycubic_cloud` and `anycubic_remote_printing` out of
   anything you print or commit. The GitHub remote is **public**.

## Preset model

A user preset stores only changed keys plus `"inherits": "<parent>"`. Effective
value = the flattened chain. Two traps:

- `filament\base\X.json` shares its `"name"` with `filament\X.json`. The
  top-level file is the live preset; `base` must never win the index.
- `.conf` is JSON followed by a `# MD5 checksum` line — parse with `raw_decode`.

## Put values at the right layer

- Flow ceiling → **filament** preset
- Kinematic limits → **machine** preset
- Geometry and intent → **process** preset

Never clamp a process speed to one filament's flow cap; the slicer already
enforces that at slice time, and the pin outlives the filament.

## Answering

Vietnamese unless asked otherwise. Keep technical terms, key names, preset
names, CLI commands and error strings verbatim — never translate them.
Bullets and tables over prose. Status icons: 🟢 done 🔴 error 🟡 risk
🔵 info 📝 todo ⏳ blocked ❌ don't. End every reply with an
**⚠️ ACTION REQUIRED** section, or "None".
