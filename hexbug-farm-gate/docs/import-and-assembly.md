# Import and assembly

## Importing STEP files into Fusion 360

1. Open Fusion 360 → create a new design (or open your pen layout).
2. **Insert → Insert into current design** (or **File → Open** for a single part).
3. Select all files from `cadquery/output/`:
   - `base_assembly.step`
   - `gate_post.step`
   - `boom_arm.step`
   - `skirt_lower_rail.step`
   - `skirt_post.step` (×10 instances)
   - `skirt_assembly_preview.step` (optional reference)
   - `hinge_pin.step` (×2 instances, or use `hinge_pins_pair.step`)
   - `horn_adapter.step`
4. Each import is a separate body/component. Use **Move/Copy** to position them.

### Recommended assembly layout

```text
  [desk base plate]
  |                              |
  [post+servo]----[boom arm]-----[rest pillar]
                      |
                   [skirt]
```

- **Left:** `gate_post` drops into the socket on `base_assembly` (glue or screw optional).
- **Right:** boom tip rests in the notch on the **rest pillar** when the gate is closed.
- Post footing sits on the base top at `POST_CENTER_X_MM` from the left edge.

Coordinate convention in the STEP files:

- **Base** origin at the bottom-left corner of the plate (X = 0 at left edge, Z = 0 on desk).
- **Boom** extends along **+X** from the post; root (servo end) at post centre.
- **Skirt** span matches `SKIRT_HINGE_SPAN_MM` (80 mm); hinge ears at X = 0 and X = 80 relative to skirt origin.
- **Post** is centred on X/Y at its origin; place on base at `(POST_CENTER_X_MM, 0, BASE_THICKNESS_MM)`.

### Aligning skirt to boom

1. Position **boom** so the root mates with the horn adapter on the servo.
2. Align **skirt** hinge ears with the **underside hinge bosses** on the boom.
3. Insert **hinge pins** through ear → boss → ear (along **Y** axis).
4. With boom horizontal (closed), skirt should hang vertically; **stop tabs** block outward swing.

### Hinged skirt — individual posts + hanging retaining bar

Each **skirt post** hinges to the **boom** (top) and to the **retaining bar** (bottom).

The **retaining bar is not fixed** to the base or posts — it **hangs** and is held only by the skirt posts. As the boom lifts, posts and bar fold together.

1. Attach posts to boom clevis forks (top) and retaining bar clevis forks (bottom).
2. Insert **filament pin** (1.75 mm) through aligned holes — drill to **2.15 mm** if needed.
3. When the boom **lifts upward** (0° → 90°), the whole skirt folds.

Run `python animate_gate.py` — side view uses **Pymunk** rigid-body physics.

### Hinged skirt behaviour

| Gate state | Boom | Skirt |
|------------|------|-------|
| **Closed** | Horizontal, rests on right pillar | Posts vertical; retaining bar hangs below |
| **Open** | Vertical (lifted up) | Posts + bar fold upward together |

No second actuator — passive double hinges on each post.

## Fusion script notes

The script creates the same parts **spaced apart** so they don’t fuse together. After running:

1. Move **gate_post** to your pen corner.
2. Move **boom_arm** so its root (X = 0 end) meets the post horn area.
3. Move **skirt_assembly** under the boom; align hinge holes.
4. Place two **hinge_pin** bodies through the hinge stacks (or delete mesh pins and use metal rod).

To change sizes: edit parameters at the top of `build_gate.py` (mirror `params.py`), then re-run.

## Printing (Bambu Lab X1 Carbon)

| Part | Orientation | Settings |
|------|-------------|----------|
| `base_assembly` | Flat on build plate | 4 walls, 25% infill |
| `gate_post` | Upright (Z = post height) | 3 walls, 20% infill |
| `boom_arm` | Flat, hinge bosses up | 3 walls, 15% infill |
| `skirt_assembly` | Flat, hinge ears up | 3 walls, 15% infill |
| `hinge_pin` | On side (pin axis horizontal) | 100% infill, 0.2 mm layers |
| `horn_adapter` | Flat | 3 walls, 20% infill |

- **Material:** PLA for prototypes; PETG for hinge ears if you want more toughness.
- **Hinge pins:** Prefer **2 mm steel rod** cut to length — more durable than printed pins.
- **Hole fit:** If pins are tight, lightly drill to 2.2 mm or sand printed pins.

## Hardware

- 1× SG90 (or compatible) 9g micro servo
- 2× hinge pins: 2 mm rod × ~14 mm (or printed `hinge_pin`)
- 2× M2 × 6 mm screws — horn to adapter (check your horn hole spacing)
- 1× M2 × 8 mm screw — adapter tab to boom (optional, can glue)
- Servo mounting screws (usually included with servo)

## Servo mounting

1. Insert servo into post cavity from the front; flange sits in the side slot.
2. Route wire through the bottom or a hole you add in Fusion.
3. Attach horn → **horn_adapter** → **boom_arm** root.
4. **Closed position:** boom horizontal (adjust servo PWM / horn spline in software).
5. **Open position:** boom vertical; confirm skirt clears the post.

## Tweaking in Fusion

Imported STEP has no parametric history. Use:

- **Press Pull** — adjust thickness, move faces
- **Combine → Cut** — clearance for your exact servo
- **Fillet** — soften edges, strengthen hinge ears
- **Split body** — separate boom stripes for multi-color print (future)

## Changing dimensions

1. Edit `params.py`.
2. Regenerate: `python cadquery/generate_gate.py`
3. Re-import (or replace) STEP in Fusion.
4. Update matching values in `fusion/build_gate.py` if you use the script path.

Key parameters for the pen opening:

- `GATE_OPENING_MM` — width the gate blocks
- `BOOM_LENGTH_MM` — slightly longer than opening
- `SKIRT_DROP_MM` — how far bars hang (must block Hexbugs)
