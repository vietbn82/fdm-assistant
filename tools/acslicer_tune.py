#!/usr/bin/env python3
"""
acslicer_tune.py - read Anycubic Slicer Next presets, audit them, optionally fix.

Usage:
  python acslicer_tune.py --list
  python acslicer_tune.py --show "<preset name>"
  python acslicer_tune.py --audit                 # report only (safe)
  python acslicer_tune.py --audit --fix           # write fixes + backup
  python acslicer_tune.py --audit --fix --yes     # no prompt
"""
import argparse, json, os, re, shutil, sys, time
from pathlib import Path

ROOT = Path(os.environ["APPDATA"]) / "AnycubicSlicerNext"
SYS = ROOT / "system" / "Anycubic"
USER = ROOT / "user"

KINDS = ("machine", "process", "filament")


# ---------------------------------------------------------------- loading
def _load(p):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"  !! unreadable {p.name}: {e}", file=sys.stderr)
        return None


def build_index():
    """name -> {kind, path, data, origin}"""
    idx = {}
    for kind in KINDS:
        base = SYS / kind
        if not base.is_dir():
            continue
        for p in base.rglob("*.json"):
            d = _load(p)
            if d and "name" in d:
                idx[d["name"]] = dict(kind=kind, path=p, data=d, origin="system")
    # user presets override system on name collision
    if USER.is_dir():
        for udir in USER.iterdir():
            if not udir.is_dir():
                continue
            for kind in KINDS:
                kd = udir / kind
                if not kd.is_dir():
                    continue
                # top-level file is the live preset; filament/base/*.json is a
                # cached full snapshot under the SAME name - never let it win
                for p in sorted(kd.rglob("*.json"),
                                key=lambda q: "base" in q.parts):
                    d = _load(p)
                    if d and "name" in d:
                        if d["name"] in idx and idx[d["name"]]["origin"].startswith("user"):
                            continue
                        idx[d["name"]] = dict(kind=kind, path=p, data=d,
                                              origin="user:" + udir.name)
    return idx


def write_preset(path, data):
    """Write the json and bump the .info sidecar so cloud sync sees it as newer."""
    path.write_text(json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True),
                    encoding="utf-8")
    info = path.with_suffix(".info")
    if info.exists():
        now = str(int(time.time()))
        lines = []
        for ln in info.read_text(encoding="utf-8").splitlines():
            if ln.strip().startswith("updated_time"):
                ln = f"updated_time = {now}"
            lines.append(ln)
        info.write_text("\n".join(lines) + "\n", encoding="utf-8")


def backup(tag):
    stamp = time.strftime("%Y%m%d-%H%M%S")
    dst = ROOT / f"user_backup-tune-{tag}-{stamp}"
    shutil.copytree(USER, dst)
    print(f"backup: {dst}")
    return dst


# ---------------------------------------------------------------- export
REPO = Path(__file__).resolve().parent.parent
MIRROR = REPO / "presets"


def _mirror_pairs():
    """(live path, repo path) for every preset worth tracking.

    Drops the userid directory level so nothing identifying reaches the public
    remote, and skips filament\\base\\ - those are cache snapshots that share a
    "name" with the real preset and would only produce confusing double diffs.
    """
    out = []
    if not USER.is_dir():
        return out
    for udir in sorted(USER.iterdir()):
        if not udir.is_dir():
            continue
        for kind in KINDS:
            kd = udir / kind
            if not kd.is_dir():
                continue
            for p in sorted(kd.rglob("*")):
                if p.is_dir() or "base" in p.relative_to(kd).parts:
                    continue
                if p.suffix not in (".json", ".info"):
                    continue
                out.append((p, MIRROR / kind / p.name))
    return out


def _normalized(src):
    """Bytes to write into the mirror: JSON re-serialized for stable diffs."""
    raw = src.read_bytes()
    if src.suffix != ".json":
        return raw
    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception:
        return raw
    return (json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True)
            + "\n").encode("utf-8")


def export_presets(write=True):
    """Copy live presets into presets\\. Returns the list of changed repo paths."""
    changed = []
    seen = set()
    for src, dst in _mirror_pairs():
        seen.add(dst)
        want = _normalized(src)
        if dst.exists() and dst.read_bytes() == want:
            continue
        changed.append(dst)
        if write:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(want)
    # presets deleted on disk must disappear from the mirror too
    if MIRROR.is_dir():
        for stale in sorted(MIRROR.rglob("*")):
            if stale.is_file() and stale not in seen:
                changed.append(stale)
                if write:
                    stale.unlink()
    return changed


def resolve(name, idx, _seen=None):
    """Flatten the inherits chain into one dict."""
    _seen = _seen or set()
    if name in _seen or name not in idx:
        return {}
    _seen.add(name)
    e = idx[name]
    out = resolve(e["data"].get("inherits", ""), idx, _seen)
    out.update(e["data"])
    return out


# ---------------------------------------------------------------- helpers
def num(v, ref=None):
    """'150' -> 150.0 ; '60%' -> 0.6*ref ; ['x'] -> first elem."""
    if isinstance(v, list):
        v = v[0] if v else None
    if v is None:
        return None
    s = str(v).strip()
    if s in ("", "nil", "default"):
        return None
    if s.endswith("%"):
        try:
            pct = float(s[:-1]) / 100.0
        except ValueError:
            return None
        return pct * ref if ref is not None else None
    m = re.match(r"^-?\d+(\.\d+)?", s)
    return float(m.group()) if m else None


def width(cfg, key, nozzle):
    w = num(cfg.get(key), nozzle)
    return w if w else nozzle


# ---------------------------------------------------------------- rules
# speed key -> (line-width key, uses-initial-layer-height)
FLOW_MAP = {
    "outer_wall_speed": ("outer_wall_line_width", False),
    "inner_wall_speed": ("inner_wall_line_width", False),
    "sparse_infill_speed": ("sparse_infill_line_width", False),
    "internal_solid_infill_speed": ("internal_solid_infill_line_width", False),
    "top_surface_speed": ("top_surface_line_width", False),
    "gap_infill_speed": ("inner_wall_line_width", False),
    "initial_layer_speed": ("initial_layer_line_width", True),
    "initial_layer_infill_speed": ("initial_layer_line_width", True),
}
OVERHANG_ORDER = ["overhang_1_4_speed", "overhang_2_4_speed",
                  "overhang_3_4_speed", "overhang_4_4_speed",
                  "overhang_totally_speed"]


def audit_process(name, cfg, own, machine, filament, findings):
    """cfg = fully resolved, own = only the keys this user preset itself sets."""
    def add(sev, msg, key=None, new=None):
        findings.append(dict(preset=name, sev=sev, msg=msg, key=key, new=new))

    nozzle = num(machine.get("nozzle_diameter")) or 0.4
    lh = num(cfg.get("layer_height")) or 0.2
    ilh = num(cfg.get("initial_layer_print_height")) or lh
    max_lh = num(machine.get("max_layer_height")) or 0.75 * nozzle
    mvs = num(filament.get("filament_max_volumetric_speed")) or 0
    vmax_xy = num(machine.get("machine_max_speed_x")) or 1e9
    amax = num(machine.get("machine_max_acceleration_extruding")) or 1e9
    atrav = num(machine.get("machine_max_acceleration_travel")) or 1e9

    # --- layer height sanity
    if lh > max_lh:
        add("ERR", f"layer_height {lh} > printer max_layer_height {max_lh}",
            "layer_height", f"{max_lh}")
    if lh > 0.75 * nozzle:
        add("WARN", f"layer_height {lh} > 75% of nozzle {nozzle} (poor layer bonding)")
    if ilh > max_lh:
        add("ERR", f"initial_layer_print_height {ilh} > max_layer_height {max_lh}",
            "initial_layer_print_height", f"{max_lh}")

    # --- volumetric flow ceiling
    # NOTE Anycubic's own stock profiles already exceed the PLA flow cap, so a
    # violation is only the *user's* problem when the user set the value. Either
    # way the slicer silently throttles, so the typed number is fiction.
    if mvs:
        for skey, (wkey, first) in FLOW_MAP.items():
            sp = num(cfg.get(skey))
            if sp is None:
                continue
            h = ilh if first else lh
            w = width(cfg, wkey, nozzle)
            flow = sp * h * w
            if flow > mvs * 1.001:
                safe = int(mvs / (h * w))
                src = "you set" if skey in own else "inherited"
                add("FLOW",
                    f"{skey}={sp:g} ({src}) wants {flow:.1f} mm3/s, filament caps at "
                    f"{mvs:g} - real speed is {safe} mm/s (h={h:g} w={w:g})",
                    skey, str(safe))

    # --- kinematics ceiling
    for skey in list(FLOW_MAP) + ["travel_speed", "bridge_speed"]:
        sp = num(cfg.get(skey))
        if sp is not None and sp > vmax_xy:
            add("ERR", f"{skey}={sp:g} > machine_max_speed_x/y {vmax_xy:g}",
                skey, str(int(vmax_xy)))
    for akey, cap in (("default_acceleration", amax),
                      ("outer_wall_acceleration", amax),
                      ("inner_wall_acceleration", amax),
                      ("travel_acceleration", atrav),
                      ("bridge_acceleration", amax),
                      ("initial_layer_acceleration", amax)):
        a = num(cfg.get(akey))
        if a is not None and a > cap:
            add("ERR", f"{akey}={a:g} > firmware cap {cap:g}", akey, str(int(cap)))

    # --- overhang speed ladder must be non-increasing
    # 0 means "no override, print at normal speed" - not a real ladder entry
    ow_ref = num(cfg.get("outer_wall_speed"))
    vals = [(k, num(cfg.get(k), ow_ref)) for k in OVERHANG_ORDER]
    vals = [(k, v) for k, v in vals if v]
    for (k1, v1), (k2, v2) in zip(vals, vals[1:]):
        if v2 > v1:
            add("WARN", f"{k2}={v2:g} faster than {k1}={v1:g} - overhang ladder inverted",
                k2, str(int(v1)))

    # --- outer wall should not outrun inner wall
    iw = num(cfg.get("inner_wall_speed"))
    if ow_ref and iw and ow_ref > iw:
        add("WARN", f"outer_wall_speed {ow_ref:g} > inner_wall_speed {iw:g} - surface quality loss")

    # --- ironing
    if cfg.get("ironing_type", "no ironing") not in ("no ironing", "", None):
        isp = num(cfg.get("ironing_speed"))
        ispc = num(cfg.get("ironing_spacing"))
        if isp and isp > 30:
            add("WARN", f"ironing_speed {isp:g} > 30 - ironing shears instead of smearing",
                "ironing_speed", "20")
        if ispc and ispc < 0.08:
            add("WARN", f"ironing_spacing {ispc:g} very tight - over-extrudes top surface")

    # --- bridges
    bf = num(cfg.get("bridge_flow"))
    if bf and bf > 1.05:
        add("WARN", f"bridge_flow {bf:g} > 1.05 - drooping bridges")
    bs = num(cfg.get("bridge_speed"))
    if bs and bs < 20:
        add("INFO", f"bridge_speed {bs:g} very slow - bridges may sag from heat soak")

    # --- shells
    tl, bl = num(cfg.get("top_shell_layers")), num(cfg.get("bottom_shell_layers"))
    if tl and lh and tl * lh < 0.6:
        add("WARN", f"top shell {tl:g}x{lh:g} = {tl*lh:.2f}mm < 0.6mm - pillowing risk")
    if bl and lh and bl * lh < 0.4:
        add("WARN", f"bottom shell {bl:g}x{lh:g} = {bl*lh:.2f}mm < 0.4mm")

    # --- support
    if str(cfg.get("enable_support")) == "1":
        tz = num(cfg.get("support_top_z_distance"))
        if tz is not None and lh and tz > 0:
            rem = tz % lh
            if min(rem, lh - rem) > 1e-6:
                add("WARN",
                    f"support_top_z_distance {tz:g} not a multiple of layer_height {lh:g}",
                    "support_top_z_distance", f"{round(tz/lh)*lh:g}")


def audit_filament(name, cfg, own, machine, findings):
    def add(sev, msg, key=None, new=None):
        findings.append(dict(preset=name, sev=sev, msg=msg, key=key, new=new))

    hi = num(cfg.get("nozzle_temperature_range_high"))
    lo = num(cfg.get("nozzle_temperature_range_low"))
    for k in ("nozzle_temperature", "nozzle_temperature_initial_layer",
              "nozzle_temperature_HS", "nozzle_temperature_initial_layer_HS"):
        t = num(cfg.get(k))
        if t is None:
            continue
        if hi and t > hi:
            add("ERR", f"{k}={t:g} above declared nozzle_temperature_range_high {hi:g}",
                "nozzle_temperature_range_high", str(int(t)))
        if lo and t < lo:
            add("WARN", f"{k}={t:g} below nozzle_temperature_range_low {lo:g}")

    fr = num(cfg.get("filament_flow_ratio"))
    if fr and not (0.85 <= fr <= 1.15):
        add("WARN", f"filament_flow_ratio {fr:g} outside 0.85-1.15 - likely a typo")

    pa = num(cfg.get("pressure_advance"))
    if pa is not None and pa > 0.2:
        add("WARN", f"pressure_advance {pa:g} very high for direct drive PLA")

    mvs = num(cfg.get("filament_max_volumetric_speed"))
    if mvs and mvs > 30:
        add("WARN", f"filament_max_volumetric_speed {mvs:g} mm3/s beyond what a 0.4 "
                    f"hotend can melt - flow cap effectively disabled")

    # noise checks look only at what this preset itself writes, not the parent
    for k in ("pellet_flow_coefficient", "pellet_flow_coefficient_0"):
        if k in own:
            add("INFO", f"'{k}' is a pellet-extruder key, meaningless on an FDM "
                        f"profile - stray value from a preset copy")
    # A filament_* key set to "nil" is NOT noise: it means "do not override the
    # machine preset". Deleting it lets the vendor parent's real value win, which
    # silently replaces whatever the machine preset was tuned to. Flag the
    # opposite case instead - an override the user may not know is in effect.
    for k, mk in (("filament_retraction_length", "retraction_length"),
                  ("filament_retraction_speed", "retraction_speed"),
                  ("filament_z_hop", "z_hop"),
                  ("filament_wipe_distance", "wipe_distance")):
        v = num(cfg.get(k))
        if v is None:
            continue                       # "nil" -> machine value applies, fine
        mv = num(machine.get(mk))
        if mv is not None and abs(v - mv) > 1e-9:
            add("WARN", f"{k}={v:g} overrides the machine preset's {mk}={mv:g}. "
                        f"The filament wins, so the machine value never applies. "
                        f"Set it to \"nil\" to defer to the machine.",
                k, "nil")

    # PLA runs on a 60C bed as standard practice even though Tg is ~54C, and
    # elefant_foot_compensation exists to absorb the squish. Warning at +5 fired
    # on the vendor's own default and taught nothing; only a real overshoot is
    # worth reporting.
    tv = num(cfg.get("temperature_vitrification"))
    bed = num(cfg.get("hot_plate_temp")) or num(cfg.get("textured_plate_temp"))
    if tv and bed and bed > tv + 15:
        add("WARN", f"bed {bed:g}C is {bed-tv:g}C above softening point "
                    f"temperature_vitrification {tv:g}C - elephant foot, and the "
                    f"part may soften enough to shift")

    hp = num(cfg.get("hot_plate_temp"))
    hp1 = num(cfg.get("hot_plate_temp_initial_layer"))
    if hp and hp1 and hp1 < hp:
        add("WARN", f"hot_plate_temp_initial_layer {hp1:g} < hot_plate_temp {hp:g} - "
                    f"first layer cooler than the rest, adhesion risk",
            "hot_plate_temp_initial_layer", str(int(hp)))
    tp = num(cfg.get("textured_plate_temp"))
    tp1 = num(cfg.get("textured_plate_temp_initial_layer"))
    if tp and tp1 and tp1 < tp:
        add("WARN", f"textured_plate_temp_initial_layer {tp1:g} < textured_plate_temp "
                    f"{tp:g} - first layer cooler than the rest, adhesion risk",
            "textured_plate_temp_initial_layer", str(int(tp)))


def audit_machine(name, cfg, findings):
    def add(sev, msg, key=None, new=None):
        findings.append(dict(preset=name, sev=sev, msg=msg, key=key, new=new))

    rl = num(cfg.get("retraction_length"))
    rre = num(cfg.get("retract_restart_extra"))
    rs = num(cfg.get("retraction_speed"))
    zh = num(cfg.get("z_hop"))
    lh_max = num(cfg.get("max_layer_height")) or 0.28

    if rl is not None and rl > 2.0:
        add("WARN", f"retraction_length {rl:g}mm is bowden-sized for direct drive - "
                    f"clogs / stringing on restart")
    if rre is not None and rre < 0:
        add("WARN", f"retract_restart_extra {rre:g} (negative) under-extrudes after "
                    f"every retract - use 0 unless measured", "retract_restart_extra", "0")
    if rs is not None and rs > 60:
        add("WARN", f"retraction_speed {rs:g} mm/s can grind filament")
    if zh is not None and 0 < zh < lh_max:
        add("WARN", f"z_hop {zh:g} < max layer height {lh_max:g} - hop lands inside the "
                    f"layer it should clear, nozzle still collides", "z_hop", "0.4")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--show", metavar="NAME")
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--yes", action="store_true")
    ap.add_argument("--flow", action="store_true",
                    help="also report speeds the filament flow cap silently throttles")
    ap.add_argument("--export", action="store_true",
                    help="mirror live presets into presets\\ for git tracking")
    ap.add_argument("--check-drift", action="store_true",
                    help="report whether presets\\ matches the live store; exit 1 if not")
    ap.add_argument("--set", action="append", default=[], metavar="PRESET|key=value",
                    help="force a value on one user preset; repeatable")
    a = ap.parse_args()

    if a.check_drift:
        changed = export_presets(write=False)
        if changed:
            print(f"drift: {len(changed)} file(s) differ between the live store "
                  f"and presets\\")
            for p in changed[:10]:
                print("  " + p.relative_to(REPO).as_posix())
            if len(changed) > 10:
                print(f"  ... and {len(changed)-10} more")
            sys.exit(1)
        print("presets\\ matches the live store")
        return

    if a.export:
        changed = export_presets()
        if not changed:
            print("presets\\ already up to date")
        else:
            print(f"exported, {len(changed)} file(s) changed:")
            for p in changed:
                print("  " + p.relative_to(REPO).as_posix())
        return

    idx = build_index()
    users = {n: e for n, e in idx.items() if e["origin"].startswith("user")}

    if a.list:
        print(f"{len(idx)} presets indexed, {len(users)} user-owned\n")
        for n, e in sorted(users.items(), key=lambda kv: (kv[1]["kind"], kv[0])):
            print(f"  [{e['kind']:8}] {n}\n              inherits: {e['data'].get('inherits','-')}")
        return

    if a.set:
        backup("set")
        for spec in a.set:
            pname, _, kv = spec.partition("|")
            key, _, val = kv.partition("=")
            e = users.get(pname)
            if not e:
                sys.exit(f"no user preset named {pname!r}")
            d = _load(e["path"])
            old = d.get(key)
            # filament/machine keys are per-extruder lists; process keys are scalars
            d[key] = [val] if (e["kind"] in ("filament", "machine")
                               and not isinstance(old, str)) else val
            write_preset(e["path"], d)
            print(f"  {pname}: {key} {old} -> {d[key]}")
        print()
        idx = build_index()
        users = {n: x for n, x in idx.items() if x["origin"].startswith("user")}

    if a.show:
        cfg = resolve(a.show, idx)
        if not cfg:
            sys.exit(f"no preset named {a.show!r}")
        print(json.dumps({k: v for k, v in sorted(cfg.items()) if "gcode" not in k},
                         indent=2, ensure_ascii=False))
        return

    if not a.audit:
        ap.print_help()
        return

    # the .conf has a trailing "# MD5 checksum ..." line after the JSON body
    raw = (ROOT / "AnycubicSlicerNext.conf").read_text(encoding="utf-8")
    conf, _ = json.JSONDecoder().raw_decode(raw)
    pair = {}
    for p in conf.get("anycubic_presets", []):
        pair[p.get("process", "")] = (p.get("machine", ""), p.get("filament", ""))

    findings = []
    for n, e in sorted(users.items()):
        cfg = resolve(n, idx)
        own = e["data"]
        if e["kind"] == "process":
            mname, fname = pair.get(n, ("", ""))
            if not mname:
                comp = cfg.get("compatible_printers") or []
                mname = comp[0] if comp else ""
                dfp = idx.get(mname, {}).get("data", {}).get("default_filament_profile")
                fname = dfp[0] if dfp else ""
            audit_process(n, cfg, own, resolve(mname, idx), resolve(fname, idx), findings)
        elif e["kind"] == "filament":
            comp = cfg.get("compatible_printers") or []
            audit_filament(n, cfg, own, resolve(comp[0] if comp else "", idx), findings)
        else:
            audit_machine(n, cfg, findings)

    if not a.flow:
        findings = [f for f in findings if f["sev"] != "FLOW"]

    order = {"ERR": 0, "WARN": 1, "FLOW": 2, "INFO": 3}
    findings.sort(key=lambda f: (order[f["sev"]], f["preset"]))

    cur = None
    for f in findings:
        if f["preset"] != cur:
            cur = f["preset"]
            print(f"\n=== {cur}  [{users[cur]['kind']}]")
        fixable = f"   -> set {f['key']} = {f['new']}" if a.fix and f["key"] else ""
        print(f"  {f['sev']:4}  {f['msg']}{fixable}")

    n = lambda s: sum(1 for f in findings if f["sev"] == s)
    print(f"\n{n('ERR')} errors, {n('WARN')} warnings, {n('FLOW')} flow-capped, "
          f"{n('INFO')} notes across {len(users)} user presets")
    if not a.flow:
        print("(--flow also lists speeds the filament flow cap silently throttles)")

    if not a.fix:
        print("\n(report only - re-run with --fix to apply the '->' changes)")
        return

    todo = [f for f in findings if f["key"] and f["sev"] in ("ERR", "WARN", "FLOW")]
    if not todo:
        print("nothing auto-fixable")
        return
    if not a.yes:
        if input(f"\napply {len(todo)} changes? [y/N] ").strip().lower() != "y":
            return

    backup("fix")
    by_preset = {}
    for f in todo:
        by_preset.setdefault(f["preset"], []).append(f)
    for pname, fs in by_preset.items():
        p = users[pname]["path"]
        d = _load(p)
        for f in fs:
            old = d.get(f["key"])
            d[f["key"]] = [f["new"]] if isinstance(old, list) else f["new"]
            print(f"  {pname}: {f['key']} {old} -> {f['new']}")
        write_preset(p, d)
    print("\ndone - restart Anycubic Slicer Next to reload presets")


if __name__ == "__main__":
    main()
