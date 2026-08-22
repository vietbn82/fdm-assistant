#!/usr/bin/env python3
"""One-off: rebuild the user preset set around print purpose.

Viet cleared the unused presets by hand in the slicer and asked for what is
left to be optimised, plus a fresh process set named by purpose rather than by
layer height. This script does that in one pass so the result is reproducible
and reviewable, rather than a dozen loose --set calls.

Every preset written here stores only what differs from its vendor parent.
Speeds are deliberately NOT lowered to match the filament flow ceiling: that
limit belongs to the filament preset and the slicer already applies it at slice
time (docs/preset-model.md section 3).

Run with --dry to see the plan without touching anything.
"""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import acslicer_tune as t                                    # noqa: E402

USER = t.USER / "855643"
DRY = "--dry" in sys.argv
VERSION = "1.3.2606.12"

# ---------------------------------------------------------------- deletions
DELETE = [
    # no Kobra S1 in the workshop
    "filament/Anycubic PLA @Anycubic Kobra S1 0.4 nozzle - Copy",
    # merged into "PLA BBL Lite@KX 0.4"
    "filament/BBL PLA Lite",
    "filament/BBL PLA Lite @Anycubic Kobra X 0.4 nozzle",
    # replaced by the purpose-based set
    "process/0.12 mm - High Quality Novi @AC KX",
    "process/0.20mm - High Quality Novi @AC KX",
    "process/0.20mm - Standard Novi @AC KX",
    "process/0.20mm PLA Lite @AC KX - Copy",
    "process/0.20mm PLA Lite @AC KX - fix first layer",
    "process/0.20mm Standard @AC KX - Copy",
    "process/0.24mm Fast speed @AC KX",
]

PLA_PARENT = "Anycubic PLA @Anycubic Kobra X 0.4 nozzle"

# ---------------------------------------------------------------- filament
# Merge of the two BBL presets: neither was complete on its own. The bed
# temperatures contradicted each other (one said 50 steady / 45 first layer,
# the other the reverse); settled at a flat 50 so the first layer is never the
# cold one, without inventing a number neither preset had.
FILAMENT = {
    "PLA BBL Lite@KX 0.4": {
        "inherits": PLA_PARENT,
        "filament_vendor": ["BambuLab"],
        "filament_density": ["1.3"],
        "filament_flow_ratio": ["0.98"],
        "filament_max_volumetric_speed": ["15"],
        "nozzle_temperature_HS": ["205"],
        "nozzle_temperature_initial_layer_HS": ["210"],
        "nozzle_temperature_range_high": ["215"],
        "pressure_advance": ["0.025"],
        "adaptive_pressure_advance": ["1"],
        "hot_plate_temp": ["50"],
        "hot_plate_temp_initial_layer": ["50"],
        "textured_plate_temp": ["50"],
        "textured_plate_temp_initial_layer": ["50"],
        "close_fan_the_first_x_layers": ["2"],
        "slow_down_layer_time_HS": ["5"],
        "slow_down_min_speed": ["10"],
    },
    # Flow was copied across from the BBL preset without being measured. An
    # unknown generic PLA gets the vendor default until a flow test says more.
    "PLA Generic@KX 0.4": {
        "inherits": PLA_PARENT,
        "filament_max_volumetric_speed": ["13"],
        "nozzle_temperature_HS": ["210"],
        "nozzle_temperature_range_high": ["220"],
        "textured_plate_temp": ["45"],
        "textured_plate_temp_initial_layer": ["50"],
    },
}

# ---------------------------------------------------------------- machine
MACHINE = {
    "Anycubic Kobra X 0.4 nozzle - high quality": {
        "inherits": "Anycubic Kobra X 0.4 nozzle",
        "retraction_length": ["1"],
        "retraction_speed": ["35"],
        "deretraction_speed": ["35"],
        "retraction_minimum_travel": ["2"],
        # was -0.05: a negative restart under-extrudes after every retract
        "retract_restart_extra": ["0"],
        # was 0.16, below the 0.28 max layer height - the hop landed inside the
        # layer it was meant to clear
        "z_hop": ["0.4"],
    },
}

# ---------------------------------------------------------------- process
PROCESS = {
    # Sharpness. At 0.12 the flow ceiling is nowhere near binding (~297 mm/s),
    # so quality, not throughput, sets the speeds.
    "Novi 0.12 - FIGURE @AC KX": {
        "inherits": "0.12mm High Quality @Anycubic Kobra X 0.4 nozzle",
        "outer_wall_speed": "50",
        "sparse_infill_density": "12%",
        "sparse_infill_pattern": "gyroid",
        "ironing_type": "top",
        "seam_slope_type": "all",
        "detect_thin_wall": "1",
        "slowdown_for_curled_perimeters": "1",
    },
    # Strength. Walls carry load far more cheaply than infill, so the budget
    # goes into wall_loops rather than density.
    "Novi 0.20 - TOOL @AC KX": {
        "inherits": "0.20mm Standard @Anycubic Kobra X 0.4 nozzle",
        "wall_loops": "4",
        "wall_sequence": "inner-outer-inner wall",
        "sparse_infill_density": "25%",
        "sparse_infill_pattern": "gyroid",
        "bottom_shell_layers": "4",
        # dimensional accuracy on the outside; 200 is rough on a bedslinger
        "outer_wall_speed": "120",
    },
    # Throughput. Strip everything that is not load-bearing or dimensional.
    "Novi 0.28 - TEST @AC KX": {
        "inherits": "0.28mm Standard @Anycubic Kobra X 0.4 nozzle",
        "sparse_infill_density": "5%",
        "sparse_infill_pattern": "lightning",
        "top_shell_layers": "2",
        "bottom_shell_layers": "2",
        "brim_type": "no_brim",
    },
}

BASE_ID = {"machine": "GM040", "filament": "GFSA04", "process": "GP004"}
ID_KEY = {"machine": "printer_settings_id", "filament": "filament_settings_id",
          "process": "print_settings_id"}


def write(kind, name, body):
    p = USER / kind / f"{name}.json"
    data = dict(body)
    data["name"] = name
    data["from"] = "User"
    data["is_custom_defined"] = "0"
    data["version"] = VERSION
    ident = ID_KEY[kind]
    data[ident] = [name] if kind == "filament" else name
    if DRY:
        print(f"  WRITE {p.relative_to(t.ROOT)}  ({len(data)} keys)")
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True),
                 encoding="utf-8")
    info = p.with_suffix(".info")
    existed = info.exists()
    info.write_text(
        "sync_info = {}\nuser_id = \nsetting_id = \nbase_id = {}\n"
        "updated_time = {}\n".format(
            "update" if existed else "create", BASE_ID[kind], int(time.time())),
        encoding="utf-8")


def main():
    if not DRY:
        t.backup("restructure")

    print("delete:")
    for rel in DELETE:
        for suf in (".json", ".info"):
            p = USER / (rel + suf)
            if p.exists():
                print(f"  {p.relative_to(t.ROOT)}")
                if not DRY:
                    p.unlink()

    print("machine:")
    for n, b in MACHINE.items():
        write("machine", n, b)
    print("filament:")
    for n, b in FILAMENT.items():
        write("filament", n, b)
    print("process:")
    for n, b in PROCESS.items():
        write("process", n, b)

    if DRY:
        print("\n(dry run, nothing written)")


if __name__ == "__main__":
    main()
