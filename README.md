# fdm-assistant

Slicer configuration for an **Anycubic Kobra X 0.4** running Anycubic Slicer
Next. Not application code — the presets this repo manages live outside it, in
`%APPDATA%\AnycubicSlicerNext\`. What is versioned here is the tooling, the
documentation, the decisions, and a mirror of the presets themselves.

## How it works

Anycubic Slicer Next stores presets as JSON under `%APPDATA%`, split across
three tiers — printer, filament, process — where each preset records only the
keys it changes and inherits the rest from a vendor parent. That makes the
effective value of any setting a chain, not a number you can read off a file.

This repo adds four things on top of that store:

**A tool that understands the chain.** `tools/acslicer_tune.py` flattens the
inheritance, then checks the result against what the printer and the filament
can physically do — flow ceilings, kinematic limits, layer-height bounds — and
reports where the numbers in the UI are fiction. It can apply fixes, always
behind a full backup.

**A written contract.** `docs/working-rules.md` sets out what gets changed
without asking, what needs a decision first, and what is never touched. It is
binding on both sides, and Claude reloads it every session.

**A proposal queue.** Findings do not become edits on their own. They land in
`PENDING_APPLY.md` with the exact command that would apply them, and stay there
until approved by ID. `TODO.md` holds the decisions those proposals are waiting on.

**Automatic preset history.** A scheduled task notices when the slicer has
closed, mirrors the live presets into `presets/`, and commits them. Every
setting change ends up in git with a diff, so a bad tweak can be found and
reverted instead of guessed at.

The loop in practice: audit finds something → it becomes a proposal → you
approve it by ID → the tool applies it behind a backup → you print and judge
the result → the outcome gets written back into `profiles/`.

Start with `docs/working-rules.md`. Everything else follows from it.

## Layout

```
CLAUDE.md            project context, auto-loaded by Claude Code
TODO.md              open decisions, grouped by who they are blocked on
PENDING_APPLY.md     proposed preset changes — nothing applied until approved by ID
CHANGELOG.md         what has been done, newest first

docs/                stable reference — rarely changes
  working-rules.md   how Viet and Claude work together — binding, read first
  preset-model.md    store layout, the four file traps, which tier owns what
  device.md          printer hardware: build volume, nozzle, kinematic ceilings
  tool.md            acslicer_tune reference
  capabilities.md    what Claude can and cannot do here

profiles/            live state — changes with the printer setup
  printer.md         machine-tier values in effect
  filament.md        the four loaded spools and their presets
  process.md         the three purpose-based process presets

presets/             mirror of the live store, written by --export. Do not hand-edit.
tools/
  acslicer_tune.py   read, audit and fix presets
  preset_autocommit.py   scheduled snapshot once the slicer closes
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
on exit, erasing outside edits — and the preset autocommit task deliberately
waits for it to exit for the same reason.

The rest — the backup sequence, the `.info` sidecar requirement, the
ask/don't-ask split — is in **[`docs/working-rules.md`](docs/working-rules.md)**.

🟡 This remote is **public**. `.gitignore` excludes `*.conf` (encrypted cloud
tokens, device id), preset backups, and slicer logs. The autocommit script also
refuses to push anything that looks like a credential. Keep it that way.
