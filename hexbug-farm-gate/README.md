# Hexbug Farm Gate

Miniature train-style crossing gate for a farming simulation pen where "sheep" are Hexbugs or bristle bots. Operated by a **9g (SG90-class) servo** with a **hinged skirt** that folds up against the boom when the gate opens.

## Project layout

```
hexbug-farm-gate/
  params.py                 # shared dimensions — edit here first
  cadquery/
    generate_gate.py        # CadQuery → STEP export
    output/                 # generated .step files
  fusion/
    build_gate.py           # Fusion 360 API script
  docs/
    import-and-assembly.md
```

## Two approaches

| Approach | How | Best for |
|----------|-----|----------|
| **STEP import** | Run `cadquery/generate_gate.py`, import `.step` into Fusion | Version control, batch regeneration |
| **Fusion script** | Run `fusion/build_gate.py` inside Fusion 360 | Native bodies, easier on-model tweaks |

Both use the same dimensions (keep `fusion/build_gate.py` in sync when you change `params.py`).

## Assembly animation

```powershell
python animate_gate.py
```

Side-view MP4 uses **Pymunk** physics: rigid posts + **hanging** retaining bar (not fixed to base). Iso view is a kinematic preview only.

Also: `python animate_gate_physics.py` for side view only.

Creates `output/animation/gate_action_side.mp4` and `gate_action_iso.mp4`.

## Assembly images

```powershell
python render_assembly.py
```

Creates `cadquery/output/views/` with 6 angles each for assembled and exploded views, plus contact sheets. Includes desk base and SG90 servo.


```powershell
cd C:\Users\peter\Documents\Cursor\Code4Fun\hexbug-farm-gate\cadquery
pip install cadquery
python generate_gate.py
```

Import files from `cadquery/output/` into Fusion 360: **Insert → Insert into current design**.

## Quick start — Fusion script

1. Open Fusion 360, create or open a design.
2. **Utilities → Scripts and Add-Ins → Scripts**.
3. Click **+** (Create) or open `fusion/build_gate.py`.
4. **Run**. Bodies appear spaced apart — move into assembly position.

## Parts

| Part | Qty | Notes |
|------|-----|-------|
| `base_assembly` | 1 | Desk plate + right rest pillar; post socket on left |
| `gate_post` | 1 | SG90 servo pocket, horn slot |
| `boom_arm` | 1 | Hinge bosses + stop tabs |
| `skirt_retaining_bar` | 1 | Hanging bottom bar (not fixed to base) |
| `skirt_post` | 10 | Hinged top to boom, bottom to retaining bar |
| `horn_adapter` | 1 | Servo horn to boom |

**Skirt pins:** use **1.75 mm filament** snippets (hole diameter **2.15 mm** = filament + 0.4 mm). Clevis forks on boom / retaining bar; single ear on each post end.

## Defaults

- Gate opening: **100 mm**
- Hinged skirt (Option B): folds against boom when open
- Servo: SG90-class 9g micro servo
- Printer: tuned for Bambu Lab X1 Carbon (PLA/PETG, 0.2 mm layers)

## Next phase

Modular fence panels (not included in v1).

See [docs/import-and-assembly.md](docs/import-and-assembly.md) for assembly and print orientation.
