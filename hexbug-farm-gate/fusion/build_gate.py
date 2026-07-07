"""
Fusion 360 script: build hexbug farm gate with hinged skirt.

Run inside Fusion 360:
  Utilities -> Scripts and Add-Ins -> Scripts -> + (or Open) -> Run

Sync dimensions with ../params.py when changing sizes.
"""

import adsk.core
import adsk.fusion
import math
import traceback

# --- Parameters (mirror of params.py) ---
GATE_OPENING_MM = 100.0
BOOM_LENGTH_MM = 110.0
BOOM_WIDTH_MM = 8.0
BOOM_HEIGHT_MM = 3.0

SKIRT_DROP_MM = 30.0
SKIRT_BAR_COUNT = 10
SKIRT_BAR_DIAMETER_MM = 2.5
SKIRT_LOWER_RAIL_HEIGHT_MM = 3.0
SKIRT_TOP_RAIL_HEIGHT_MM = 3.0
SKIRT_HINGE_SPAN_MM = 80.0

HINGE_PIN_DIAMETER_MM = 2.0
HINGE_PIN_LENGTH_MM = 14.0
HINGE_BOSS_HEIGHT_MM = 5.0
HINGE_EAR_THICKNESS_MM = 3.0
HINGE_EAR_WIDTH_MM = 8.0
HINGE_PIN_CLEARANCE_MM = 0.25

SERVO_BODY_WIDTH_MM = 12.7
SERVO_BODY_LENGTH_MM = 23.0
SERVO_BODY_HEIGHT_MM = 22.8
SERVO_FLANGE_WIDTH_MM = 27.0
SERVO_FLANGE_THICKNESS_MM = 2.5

POST_WIDTH_MM = 22.0
POST_DEPTH_MM = 24.0
POST_HEIGHT_MM = 75.0

BASE_LENGTH_MM = 145.0
BASE_WIDTH_MM = 55.0
BASE_THICKNESS_MM = 5.0
POST_CENTER_X_MM = 14.0
POST_SOCKET_DEPTH_MM = 8.0
PILLAR_WIDTH_MM = 18.0
PILLAR_DEPTH_MM = 18.0
PILLAR_CENTER_X_MM = POST_CENTER_X_MM + BOOM_LENGTH_MM - 4.0
BOOM_AXIS_HEIGHT_MM = POST_HEIGHT_MM - 10.0
PILLAR_REST_NOTCH_DEPTH_MM = 1.5

HORN_ADAPTER_DIAMETER_MM = 20.0
HORN_ADAPTER_THICKNESS_MM = 3.0
HORN_HOLE_DIAMETER_MM = 2.0
HORN_HOLE_SPAN_MM = 10.0
BOOM_MOUNT_TAB_WIDTH_MM = 8.0
BOOM_MOUNT_TAB_LENGTH_MM = 15.0

CLEARANCE_MM = 0.3
FIT_CLEARANCE_MM = 0.15


def _mm(value):
    return value / 10.0  # Fusion internal units are cm


def _box(comp, name, x, y, z, cx, cy, cz):
    """Create a box feature; cx/cy/cz are center offsets in mm."""
    sketches = comp.sketches
    xy = comp.xYConstructionPlane
    sk = sketches.add(xy)
    lines = sk.sketchCurves.sketchLines
    half_x, half_y = x / 2, y / 2
    lines.addTwoPointRectangle(
        adsk.core.Point3D.create(_mm(cx - half_x), _mm(cy - half_y), 0),
        adsk.core.Point3D.create(_mm(cx + half_x), _mm(cy + half_y), 0),
    )
    prof = sk.profiles.item(0)
    extrudes = comp.features.extrudeFeatures
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(_mm(z)))
    feat = extrudes.add(ext_input)
    body = feat.bodies.item(0)
    body.name = name
    return body


def _cylinder(comp, name, diameter, height, cx, cy, cz=0):
    sketches = comp.sketches
    xy = comp.xYConstructionPlane
    sk = sketches.add(xy)
    sk.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(_mm(cx), _mm(cy), 0),
        _mm(diameter / 2),
    )
    prof = sk.profiles.item(0)
    extrudes = comp.features.extrudeFeatures
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(_mm(height)))
    feat = extrudes.add(ext_input)
    body = feat.bodies.item(0)
    body.name = name
    if cz != 0:
        move_bodies(comp, [body], 0, 0, cz)
    return body


def move_bodies(comp, bodies, dx, dy, dz):
    transforms = comp.features.moveFeatures
    coll = adsk.core.ObjectCollection.create()
    for b in bodies:
        coll.add(b)
    transform = adsk.core.Matrix3D.create()
    transform.translation = adsk.core.Vector3D.create(_mm(dx), _mm(dy), _mm(dz))
    move_input = transforms.createInput(coll, transform)
    transforms.add(move_input)


def combine_union(comp, target, tool_bodies):
    tools = adsk.core.ObjectCollection.create()
    for b in tool_bodies:
        tools.add(b)
    combines = comp.features.combineFeatures
    comb_input = combines.createInput(target, tools)
    comb_input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    combines.add(comb_input)


def combine_cut(comp, target, tool_bodies):
    tools = adsk.core.ObjectCollection.create()
    for b in tool_bodies:
        tools.add(b)
    combines = comp.features.combineFeatures
    comb_input = combines.createInput(target, tools)
    comb_input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
    combines.add(comb_input)


def build_gate_post(comp):
    post = _box(comp, "gate_post", POST_WIDTH_MM, POST_DEPTH_MM, POST_HEIGHT_MM, 0, 0, POST_HEIGHT_MM / 2)

    cavity = _box(
        comp,
        "servo_cavity",
        SERVO_BODY_WIDTH_MM + CLEARANCE_MM,
        SERVO_BODY_LENGTH_MM + CLEARANCE_MM,
        SERVO_BODY_HEIGHT_MM + CLEARANCE_MM,
        0,
        0,
        POST_HEIGHT_MM - (SERVO_BODY_HEIGHT_MM + CLEARANCE_MM) / 2,
    )
    combine_cut(comp, post, [cavity])

    horn_slot = _box(comp, "horn_slot", POST_WIDTH_MM, 6, 12, 0, POST_DEPTH_MM / 2 - 3, POST_HEIGHT_MM - 7)
    combine_cut(comp, post, [horn_slot])

    flange_slot = _box(
        comp,
        "flange_slot",
        SERVO_FLANGE_WIDTH_MM + CLEARANCE_MM,
        4,
        SERVO_FLANGE_THICKNESS_MM + CLEARANCE_MM,
        0,
        POST_DEPTH_MM / 2 - 2,
        POST_HEIGHT_MM - SERVO_BODY_HEIGHT_MM - 6,
    )
    combine_cut(comp, post, [flange_slot])
    cavity.deleteMe()

    move_bodies(comp, [post], 0, 0, 0)
    return post


def build_boom_arm(comp, offset_x=0, offset_y=40):
    boom = _box(
        comp,
        "boom_arm",
        BOOM_LENGTH_MM,
        BOOM_WIDTH_MM,
        BOOM_HEIGHT_MM,
        BOOM_LENGTH_MM / 2 + offset_x,
        offset_y,
        BOOM_HEIGHT_MM / 2,
    )

    hinge_x = [
        offset_x + (BOOM_LENGTH_MM - SKIRT_HINGE_SPAN_MM) / 2,
        offset_x + (BOOM_LENGTH_MM + SKIRT_HINGE_SPAN_MM) / 2,
    ]
    bosses = []
    for x in hinge_x:
        boss = _box(
            comp,
            "hinge_boss",
            HINGE_EAR_WIDTH_MM,
            HINGE_EAR_THICKNESS_MM,
            HINGE_BOSS_HEIGHT_MM,
            x,
            offset_y,
            -HINGE_BOSS_HEIGHT_MM / 2,
        )
        pin_hole = _cylinder(
            comp,
            "pin_hole",
            HINGE_PIN_DIAMETER_MM + 2 * HINGE_PIN_CLEARANCE_MM,
            HINGE_EAR_THICKNESS_MM + 2,
            x,
            offset_y,
            0,
        )
        combine_cut(comp, boss, [pin_hole])
        pin_hole.deleteMe()
        bosses.append(boss)

        tab = _box(comp, "stop_tab", 6, 2, 4, x, offset_y + BOOM_WIDTH_MM / 2 - 1, -2)
        bosses.append(tab)

    combine_union(comp, boom, bosses)
    for b in bosses:
        if b.isValid:
            b.deleteMe()

    pocket = _box(
        comp,
        "adapter_pocket",
        BOOM_MOUNT_TAB_LENGTH_MM,
        BOOM_MOUNT_TAB_WIDTH_MM,
        BOOM_HEIGHT_MM + 1,
        offset_x + BOOM_MOUNT_TAB_LENGTH_MM / 2,
        offset_y,
        BOOM_HEIGHT_MM / 2,
    )
    combine_cut(comp, boom, [pocket])
    pocket.deleteMe()

    return boom


def build_skirt_assembly(comp, offset_x=0, offset_y=-40):
    span = SKIRT_HINGE_SPAN_MM
    cx = offset_x + span / 2
    cy = offset_y

    top_rail = _box(
        comp,
        "skirt_top_rail",
        span,
        BOOM_WIDTH_MM,
        SKIRT_TOP_RAIL_HEIGHT_MM,
        cx,
        cy,
        SKIRT_TOP_RAIL_HEIGHT_MM / 2,
    )

    lower_rail = _box(
        comp,
        "skirt_lower_rail",
        span,
        BOOM_WIDTH_MM,
        SKIRT_LOWER_RAIL_HEIGHT_MM,
        cx,
        cy,
        -SKIRT_DROP_MM + SKIRT_LOWER_RAIL_HEIGHT_MM / 2,
    )

    parts = [top_rail, lower_rail]

    bar_len = SKIRT_DROP_MM - SKIRT_TOP_RAIL_HEIGHT_MM / 2 - SKIRT_LOWER_RAIL_HEIGHT_MM / 2
    spacing = span / (SKIRT_BAR_COUNT - 1) if SKIRT_BAR_COUNT > 1 else span

    for i in range(SKIRT_BAR_COUNT):
        x = offset_x + i * spacing
        bar = _cylinder(
            comp,
            "skirt_bar",
            SKIRT_BAR_DIAMETER_MM,
            bar_len,
            x,
            cy,
            -SKIRT_TOP_RAIL_HEIGHT_MM / 2 - bar_len / 2,
        )
        parts.append(bar)

    for x in (offset_x, offset_x + span):
        ear = _box(
            comp,
            "hinge_ear",
            HINGE_EAR_WIDTH_MM,
            HINGE_EAR_THICKNESS_MM,
            HINGE_EAR_WIDTH_MM,
            x,
            cy,
            HINGE_EAR_WIDTH_MM / 2 + SKIRT_TOP_RAIL_HEIGHT_MM,
        )
        pin_hole = _cylinder(
            comp,
            "ear_pin_hole",
            HINGE_PIN_DIAMETER_MM + 2 * HINGE_PIN_CLEARANCE_MM,
            HINGE_EAR_THICKNESS_MM + 2,
            x,
            cy,
            HINGE_EAR_WIDTH_MM / 2 + SKIRT_TOP_RAIL_HEIGHT_MM,
        )
        combine_cut(comp, ear, [pin_hole])
        pin_hole.deleteMe()
        parts.append(ear)

    skirt = parts[0]
    combine_union(comp, skirt, parts[1:])
    for b in parts[1:]:
        if b.isValid:
            b.deleteMe()

    skirt.name = "skirt_assembly"
    return skirt


def build_horn_adapter(comp, offset_x=0, offset_y=80):
    disk = _cylinder(
        comp,
        "horn_adapter",
        HORN_ADAPTER_DIAMETER_MM,
        HORN_ADAPTER_THICKNESS_MM,
        offset_x,
        offset_y,
        HORN_ADAPTER_THICKNESS_MM / 2,
    )

    tab = _box(
        comp,
        "boom_tab",
        BOOM_MOUNT_TAB_LENGTH_MM,
        BOOM_MOUNT_TAB_WIDTH_MM,
        HORN_ADAPTER_THICKNESS_MM,
        offset_x + HORN_ADAPTER_DIAMETER_MM / 2 + BOOM_MOUNT_TAB_LENGTH_MM / 2 - 2,
        offset_y,
        HORN_ADAPTER_THICKNESS_MM / 2,
    )
    combine_union(comp, disk, [tab])
    tab.deleteMe()

    # Horn screw holes (simplified as through cuts)
    hole_positions = [
        (offset_x - HORN_HOLE_SPAN_MM / 2, offset_y),
        (offset_x + HORN_HOLE_SPAN_MM / 2, offset_y),
        (offset_x, offset_y - HORN_HOLE_SPAN_MM / 2),
        (offset_x, offset_y + HORN_HOLE_SPAN_MM / 2),
    ]
    holes = []
    for hx, hy in hole_positions:
        h = _cylinder(comp, "horn_hole", HORN_HOLE_DIAMETER_MM, HORN_ADAPTER_THICKNESS_MM + 2, hx, hy, HORN_ADAPTER_THICKNESS_MM / 2)
        holes.append(h)
    combine_cut(comp, disk, holes)
    for h in holes:
        if h.isValid:
            h.deleteMe()

    boom_screw = _cylinder(
        comp,
        "boom_screw",
        2.2,
        HORN_ADAPTER_THICKNESS_MM + 2,
        offset_x + HORN_ADAPTER_DIAMETER_MM / 2 + BOOM_MOUNT_TAB_LENGTH_MM / 2 - 2,
        offset_y,
        HORN_ADAPTER_THICKNESS_MM / 2,
    )
    combine_cut(comp, disk, [boom_screw])
    boom_screw.deleteMe()

    return disk


def build_base_assembly(comp, offset_x=0, offset_y=0):
    plate = _box(
        comp,
        "base_plate",
        BASE_LENGTH_MM,
        BASE_WIDTH_MM,
        BASE_THICKNESS_MM,
        BASE_LENGTH_MM / 2 + offset_x,
        offset_y,
        BASE_THICKNESS_MM / 2,
    )

    post_socket = _box(
        comp,
        "post_socket",
        POST_WIDTH_MM + CLEARANCE_MM,
        POST_DEPTH_MM + CLEARANCE_MM,
        POST_SOCKET_DEPTH_MM + 0.5,
        POST_CENTER_X_MM + offset_x,
        offset_y,
        BASE_THICKNESS_MM - POST_SOCKET_DEPTH_MM / 2,
    )
    combine_cut(comp, plate, [post_socket])
    post_socket.deleteMe()

    pillar_h = BOOM_AXIS_HEIGHT_MM
    pillar = _box(
        comp,
        "rest_pillar",
        PILLAR_WIDTH_MM,
        PILLAR_DEPTH_MM,
        pillar_h,
        PILLAR_CENTER_X_MM + offset_x,
        offset_y,
        BASE_THICKNESS_MM + pillar_h / 2,
    )

    rest_notch = _box(
        comp,
        "rest_notch",
        BOOM_WIDTH_MM + 1.0,
        PILLAR_DEPTH_MM + 1.0,
        PILLAR_REST_NOTCH_DEPTH_MM + 0.5,
        PILLAR_CENTER_X_MM + offset_x,
        offset_y,
        BASE_THICKNESS_MM + pillar_h - PILLAR_REST_NOTCH_DEPTH_MM / 2,
    )
    combine_cut(comp, pillar, [rest_notch])
    rest_notch.deleteMe()

    combine_union(comp, plate, [pillar])
    pillar.deleteMe()
    plate.name = "base_assembly"
    return plate


def build_hinge_pin(comp, offset_x=0, offset_y=-80):
    return _cylinder(
        comp,
        "hinge_pin",
        HINGE_PIN_DIAMETER_MM + 2 * FIT_CLEARANCE_MM,
        HINGE_PIN_LENGTH_MM,
        offset_x,
        offset_y,
        HINGE_PIN_LENGTH_MM / 2,
    )


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            ui.messageBox("Open a Fusion design first.")
            return

        root = design.rootComponent
        build_base_assembly(root, offset_x=0, offset_y=-120)
        build_gate_post(root)
        build_boom_arm(root, offset_x=50, offset_y=0)
        build_skirt_assembly(root, offset_x=50, offset_y=-50)
        build_horn_adapter(root, offset_x=0, offset_y=50)
        build_hinge_pin(root, offset_x=0, offset_y=-80)
        build_hinge_pin(root, offset_x=25, offset_y=-80)

        ui.messageBox(
            "Hexbug farm gate parts created.\n\n"
            "Bodies are spaced apart for visibility — move into assembly position.\n"
            "See docs/import-and-assembly.md for hinge orientation."
        )
    except:
        if ui:
            ui.messageBox(f"Failed:\n{traceback.format_exc()}")

