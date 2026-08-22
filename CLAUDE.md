# Anycubic Kobra X — slicer config assistant

This repo manages **Anycubic Slicer Next presets for a Kobra X 0.4**, not
application code. The presets live outside the repo, in
`%APPDATA%\AnycubicSlicerNext\`.

## Where things are

Two doc trees, split by how often they change:

**`docs/` — stable reference.** Changes rarely; treat as background knowledge.

| File | Read it when |
|---|---|
| `docs/working-rules.md` | before any preset write — the procedure and the ask/don't-ask table are binding |
| `docs/preset-model.md` | how the store is laid out, the four file traps, which tier owns which setting |
| `docs/device.md` | printer hardware: build volume, nozzle, kinematic ceilings |
| `docs/tool.md` | `tools/acslicer_tune.py` reference |
| `docs/capabilities.md` | the limits — what cannot be known or measured from here |

**`profiles/` — live state.** Changes whenever the printer setup changes. Re-read
rather than trusting memory of it.

| File | Holds |
|---|---|
| `profiles/printer.md` | machine-tier values in effect |
| `profiles/filament.md` | the four loaded spools and their presets — **the user maintains this** |
| `profiles/process.md` | the three purpose-based process presets |

**Root — working files.**

| File | Read it when |
|---|---|
| `TODO.md` | first, every session — open decisions and who they are blocked on |
| `PENDING_APPLY.md` | preset changes proposed but not written. Nothing here is applied until the user names the IDs |
| `CHANGELOG.md` | what has already been done. Write finished work here rather than letting it pile up in `TODO.md` |

## Non-negotiable

1. **Close the slicer before writing presets.** It holds them in memory and
   flushes on exit, erasing outside edits. Check with `Get-Process`.
2. **Back up `user\` before every write.** `tools/acslicer_tune.py` does this;
   by hand, do it yourself.
3. **Bump `updated_time` in the `.info` sidecar** of any preset JSON you edit,
   or cloud sync treats the file as stale and reverts it.
4. **Never write to `system\`.** A PreToolUse hook blocks it. Copy into `user\`
   and edit the copy.
5. **Never write `.conf`** unless you recompute the trailing MD5. It holds cloud
   tokens — strip `anycubic_cloud` and `anycubic_remote_printing` from anything
   you print or commit. **The GitHub remote is public.**
6. **Never write a preset the user has not approved by ID.** Findings and ideas
   go into `PENDING_APPLY.md` as proposals. `/apply P1 P4` is the only path from
   proposal to disk.
7. **Never commit or push on your own** — one narrow exception below. Not after
   finishing a task, not to "save progress", not because the tree is clean. Make
   the edits, say what changed, and stop. `git add`, `git commit`, `git push`
   happen only when the user asks in that turn — staging counts.

   **Exception: `presets/` only.** That directory is a mirror of the live preset
   store and may be committed and pushed unattended. Do it by running
   `python tools/preset_autocommit.py`, never by hand — the script enforces the
   scope, refuses if anything outside `presets/` is staged, and blocks anything
   that looks like a credential from reaching the public remote. A hand-rolled
   `git add presets/` has none of those guards. The exception covers no other
   path: docs, tools and config still wait for the user to ask.

## Preset model

A user preset stores only changed keys plus `"inherits": "<parent>"`. Effective
value = the flattened chain. Two parsing traps *(full list: `docs/preset-model.md` §5)*:

- `filament\base\X.json` shares its `"name"` with `filament\X.json`. The
  top-level file is the live preset; `base` must never win the index.
- `.conf` is JSON followed by a `# MD5 checksum` line — parse with `raw_decode`.

## Put values at the right layer

Flow ceiling → **filament**. Kinematic limits → **machine**. Geometry and
intent → **process**.

Never clamp a process speed to one filament's flow cap. The slicer enforces it
at slice time anyway, and the pin outlives the filament.

## Answering

Vietnamese unless the user writes English. Keep technical terms, key names,
preset names, CLI commands and error strings verbatim — never translate them.
Tables and bullets over prose; be short. Icons: 🟢 done 🔴 error 🟡 risk
🔵 info 📝 todo ⏳ blocked ❌ don't. End every reply with an
**⚠️ ACTION REQUIRED** section, or "None".

Docs language: `docs/` is Vietnamese (the user reads it). `CLAUDE.md`,
`.claude/**` and `README.md` stay English — model instructions and a public
front page.
