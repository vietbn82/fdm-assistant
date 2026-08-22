# fdm-assistant

Slicer configuration for an **Anycubic Kobra X 0.4** running Anycubic Slicer
Next. Not application code — the presets this repo manages live outside it, in
`%APPDATA%\AnycubicSlicerNext\`. What is versioned here is the tooling, the
documentation, and the decisions.

## Layout

```
CLAUDE.md            project context, auto-loaded by Claude Code
TODO.md              open decisions, grouped by who they are blocked on
PENDING_APPLY.md     proposed preset changes — nothing applied until approved by ID

docs/                stable reference — rarely changes
  working-rules.md   how Viet and Claude work together — binding
  preset-model.md    store layout, the four file traps, which tier owns what
  device.md          printer hardware: build volume, nozzle, kinematic ceilings
  tool.md            acslicer_tune reference
  capabilities.md    what is automated, what is still manual

profiles/            live state — changes with the printer setup
  printer.md         machine-tier values in effect
  filament.md        the four loaded spools and their presets
  process.md         the seven process presets, FIG / TOOL / TEST proposal

tools/
  acslicer_tune.py   read, audit and fix presets
.claude/
  settings.json      permissions + hooks
  commands/          /audit /apply /preset /newfilament
  hooks/             vendor-tree write guard, session status report
```

## Quick start

```bash
python tools/acslicer_tune.py --list     # user presets and their parents
python tools/acslicer_tune.py --audit    # findings, writes nothing
```

Inside Claude Code, `/audit` runs the same thing and reads the result against
the filaments actually loaded.

## Before changing anything

**Close the slicer first.** It holds presets in memory and flushes them to disk
on exit, erasing outside edits.

Everything else worth knowing is in `docs/working-rules.md` — the backup
sequence, the `.info` sidecar requirement, and which changes get made without
asking versus which need a decision first.

🟡 This remote is **public**. `.gitignore` excludes `*.conf` (encrypted cloud
tokens, device id), preset backups, and slicer logs. Keep it that way.
