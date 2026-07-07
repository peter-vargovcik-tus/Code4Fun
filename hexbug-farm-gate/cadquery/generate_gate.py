"""
Generate hexbug farm gate parts as STEP files for import into Fusion 360.

Skirt hinges: round donut housings on posts, boom, and retaining bar (pin along Y).
Pin: 1.75 mm filament; holes = filament + 0.4 mm.

Usage:
    pip install cadquery
    python generate_gate.py

Output: ./output/*.step
"""

from __future__ import annotations

import sys
from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import params as p  # noqa: E402

OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def _hinge_hole() -> float:
    return p.SKIRT_HINGE_HOLE_DIAMETER_MM


def _fork_y_positions() -> tuple[float, float]:
    """Deprecated — kept for docs; donuts are centred on Y=0."""
    return (0.0, 0.0)


def _hinge_donut(z_center: float, x: float = 0.0) -> cq.Workplane:
    """Round hinge housing (donut puck in XZ, thickness along Y, pin along Y)."""
    r = p.SKIRT_HINGE_BOSS_OD_MM / 2
    ty = p.SKIRT_HINGE_BOSS_THICKNESS_MM
    donut = (
        cq.Workplane("XZ")
        .center(x, z_center)
        .circle(r)
        .extrude(ty, both=True)
    )
    return donut.cut(_pin_cutter_along_y(x, z_center, y_half_span=ty / 2 + 1.0))


def _add_boom_hinge(part: cq.Workplane, x: float) -> cq.Workplane:
    """Round lug under boom at hinge station."""
    z_pin = -p.SKIRT_HINGE_BOSS_HEIGHT_MM / 2
    return part.union(_hinge_donut(z_pin, x))


def _add_bar_hinge(part: cq.Workplane, x: float) -> cq.Workplane:
    """Round lug on top of retaining bar."""
    z_pin = p.SKIRT_LOWER_RAIL_HEIGHT_MM + p.SKIRT_HINGE_BOSS_HEIGHT_MM / 2
    return part.union(_hinge_donut(z_pin, x))


def _pin_cutter_along_y(x: float, z: float, y_half_span: float = 6.0) -> cq.Workplane:
    """Cylindrical cutter along Y — ensures through-hole at exact (x, z)."""
    return (
        cq.Workplane("XZ")
        .workplane(offset=0)
        .center(x, z)
        .circle(_hinge_hole() / 2)
        .extrude(y_half_span, both=True)
    )


def _export(result: cq.Workplane, name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{name}.step"
    cq.exporters.export(result, str(path))
    print(f"  exported {path.name}")
    return path


def make_base_assembly() -> cq.Workplane:
    """Desk base plate with left post socket and right boom-rest pillar."""
    plate = cq.Workplane("XY").box(
        p.BASE_LENGTH_MM,
        p.BASE_WIDTH_MM,
        p.BASE_THICKNESS_MM,
        centered=(False, True, False),
    )

    post_socket = (
        cq.Workplane("XY")
        .box(
            p.POST_WIDTH_MM + p.CLEARANCE_MM,
            p.POST_DEPTH_MM + p.CLEARANCE_MM,
            p.POST_SOCKET_DEPTH_MM + 0.5,
            centered=(True, True, False),
        )
        .translate((p.POST_CENTER_X_MM, 0, p.BASE_THICKNESS_MM - p.POST_SOCKET_DEPTH_MM))
    )
    plate = plate.cut(post_socket)

    pillar_h = p.BOOM_AXIS_HEIGHT_MM
    pillar = (
        cq.Workplane("XY")
        .box(p.PILLAR_WIDTH_MM, p.PILLAR_DEPTH_MM, pillar_h, centered=(True, True, False))
        .translate((p.PILLAR_CENTER_X_MM, 0, p.BASE_THICKNESS_MM))
    )

    rest_notch = (
        cq.Workplane("XY")
        .box(
            p.BOOM_WIDTH_MM + 1.0,
            p.PILLAR_DEPTH_MM + 1.0,
            p.PILLAR_REST_NOTCH_DEPTH_MM + 0.5,
            centered=(True, True, False),
        )
        .translate(
            (
                p.PILLAR_CENTER_X_MM,
                0,
                p.BASE_THICKNESS_MM + pillar_h - p.PILLAR_REST_NOTCH_DEPTH_MM,
            )
        )
    )
    pillar = pillar.cut(rest_notch)

    base = plate.union(pillar)

    for fx, fy in ((8, -p.BASE_WIDTH_MM / 2 + 6), (8, p.BASE_WIDTH_MM / 2 - 6),
                   (p.BASE_LENGTH_MM - 8, -p.BASE_WIDTH_MM / 2 + 6),
                   (p.BASE_LENGTH_MM - 8, p.BASE_WIDTH_MM / 2 - 6)):
        foot = cq.Workplane("XY").center(fx, fy).circle(4).extrude(-1.2)
        base = base.union(foot)

    return base


def make_gate_post() -> cq.Workplane:
    """Vertical post with SG90 servo pocket and horn access slot."""
    outer = cq.Workplane("XY").box(
        p.POST_WIDTH_MM, p.POST_DEPTH_MM, p.POST_HEIGHT_MM, centered=(True, True, False)
    )

    inner_w = p.SERVO_BODY_WIDTH_MM + p.CLEARANCE_MM
    inner_l = p.SERVO_BODY_LENGTH_MM + p.CLEARANCE_MM
    inner_h = p.SERVO_BODY_HEIGHT_MM + p.CLEARANCE_MM

    cavity = (
        cq.Workplane("XY")
        .box(inner_w, inner_l, inner_h, centered=(True, True, False))
        .translate((0, 0, p.POST_HEIGHT_MM - inner_h))
    )

    horn_slot = (
        cq.Workplane("XY")
        .box(p.POST_WIDTH_MM, 6, 12, centered=(True, True, False))
        .translate((0, p.POST_DEPTH_MM / 2 - 3, p.POST_HEIGHT_MM - 14))
    )

    flange_slot_w = p.SERVO_FLANGE_WIDTH_MM + p.CLEARANCE_MM
    flange_slot = (
        cq.Workplane("XY")
        .box(flange_slot_w, 4, p.SERVO_FLANGE_THICKNESS_MM + p.CLEARANCE_MM, centered=(True, True, False))
        .translate((0, p.POST_DEPTH_MM / 2 - 2, p.POST_HEIGHT_MM - inner_h - 4))
    )

    post = outer.cut(cavity).cut(horn_slot).cut(flange_slot)

    mount_holes = (
        post.faces(">Y")
        .workplane()
        .pushPoints([(-8, -4), (8, -4)])
        .hole(2.2, depth=p.POST_WALL_MM + 2)
    )

    return mount_holes


def make_boom_arm() -> cq.Workplane:
    """Boom with round hinge lugs (underside) for skirt posts. Swings upward."""
    boom = cq.Workplane("XY").box(
        p.BOOM_LENGTH_MM, p.BOOM_WIDTH_MM, p.BOOM_HEIGHT_MM, centered=(False, True, False)
    )

    skirt_start = (p.BOOM_LENGTH_MM - p.SKIRT_HINGE_SPAN_MM) / 2
    spacing = (
        p.SKIRT_HINGE_SPAN_MM / (p.SKIRT_BAR_COUNT - 1) if p.SKIRT_BAR_COUNT > 1 else 0.0
    )

    for i in range(p.SKIRT_BAR_COUNT):
        x = skirt_start + i * spacing
        boom = _add_boom_hinge(boom, x)

    adapter_pocket = (
        cq.Workplane("XY")
        .box(
            p.BOOM_MOUNT_TAB_LENGTH_MM,
            p.BOOM_MOUNT_TAB_WIDTH_MM,
            p.BOOM_HEIGHT_MM + 1,
            centered=(False, True, False),
        )
        .translate((0, 0, -0.5))
    )
    return boom.cut(adapter_pocket)


def make_skirt_retaining_bar() -> cq.Workplane:
    """Hanging retaining bar with round hinge lugs (top) for skirt posts."""
    span = p.SKIRT_HINGE_SPAN_MM
    rail = (
        cq.Workplane("XY")
        .box(span, p.BOOM_WIDTH_MM, p.SKIRT_LOWER_RAIL_HEIGHT_MM, centered=(True, True, False))
        .translate((span / 2, 0, 0))
    )

    spacing = span / (p.SKIRT_BAR_COUNT - 1) if p.SKIRT_BAR_COUNT > 1 else span
    for i in range(p.SKIRT_BAR_COUNT):
        x = i * spacing
        rail = _add_bar_hinge(rail, x)

    return rail


def make_skirt_post() -> cq.Workplane:
    """Skirt post with round donut housings at top/bottom; pin holes along Y."""
    post_len = p.SKIRT_POST_LENGTH_MM
    h = p.SKIRT_HINGE_BOSS_HEIGHT_MM
    z_bot = h / 2
    z_top = post_len - h / 2

    bar = cq.Workplane("XY").circle(p.SKIRT_BAR_DIAMETER_MM / 2).extrude(post_len)
    bar = bar.union(_hinge_donut(z_bot, 0))
    bar = bar.union(_hinge_donut(z_top, 0))
    bar = bar.cut(_pin_cutter_along_y(0, z_bot))
    bar = bar.cut(_pin_cutter_along_y(0, z_top))
    return bar


def make_skirt_lower_rail() -> cq.Workplane:
    return make_skirt_retaining_bar()


def make_skirt_assembly() -> cq.Workplane:
    """Closed-state preview: posts vertical, retaining bar hanging below."""
    rail = make_skirt_retaining_bar()
    spacing = (
        p.SKIRT_HINGE_SPAN_MM / (p.SKIRT_BAR_COUNT - 1) if p.SKIRT_BAR_COUNT > 1 else 0.0
    )
    assembly = rail
    for i in range(p.SKIRT_BAR_COUNT):
        post = make_skirt_post().translate((i * spacing, 0, p.SKIRT_LOWER_RAIL_HEIGHT_MM))
        assembly = assembly.union(post)
    return assembly


def make_horn_adapter() -> cq.Workplane:
    """Disk that mounts to SG90 horn and clamps the boom root."""
    disk = cq.Workplane("XY").circle(p.HORN_ADAPTER_DIAMETER_MM / 2).extrude(p.HORN_ADAPTER_THICKNESS_MM)

    horn_holes = (
        disk.faces(">Z")
        .workplane()
        .pushPoints(
            [
                (-p.HORN_HOLE_SPAN_MM / 2, 0),
                (p.HORN_HOLE_SPAN_MM / 2, 0),
                (0, -p.HORN_HOLE_SPAN_MM / 2),
                (0, p.HORN_HOLE_SPAN_MM / 2),
            ]
        )
        .hole(p.HORN_HOLE_DIAMETER_MM, depth=p.HORN_ADAPTER_THICKNESS_MM + 1)
    )

    tab = (
        cq.Workplane("XY")
        .box(
            p.BOOM_MOUNT_TAB_LENGTH_MM,
            p.BOOM_MOUNT_TAB_WIDTH_MM,
            p.HORN_ADAPTER_THICKNESS_MM,
            centered=(False, True, False),
        )
        .translate((p.HORN_ADAPTER_DIAMETER_MM / 2 - 2, 0, 0))
    )

    adapter = horn_holes.union(tab)

    boom_hole = (
        adapter.faces(">Z")
        .workplane()
        .center(p.BOOM_MOUNT_TAB_LENGTH_MM / 2 - 2, 0)
        .hole(2.2, depth=p.HORN_ADAPTER_THICKNESS_MM + 1)
    )

    return boom_hole


def make_hinge_joint_preview() -> cq.Workplane:
    """One hinge station: boom lug + post donuts + retaining-bar lug (Fusion inspection)."""
    spacing = (
        p.SKIRT_HINGE_SPAN_MM / (p.SKIRT_BAR_COUNT - 1) if p.SKIRT_BAR_COUNT > 1 else 0.0
    )
    x = spacing * 2
    skirt_start = (p.BOOM_LENGTH_MM - p.SKIRT_HINGE_SPAN_MM) / 2

    boom = cq.Workplane("XY").box(30, p.BOOM_WIDTH_MM, p.BOOM_HEIGHT_MM, centered=(False, True, False))
    boom = _add_boom_hinge(boom, x - skirt_start)

    post = make_skirt_post().translate((x, 0, p.SKIRT_LOWER_RAIL_HEIGHT_MM))

    bar = cq.Workplane("XY").box(20, p.BOOM_WIDTH_MM, p.SKIRT_LOWER_RAIL_HEIGHT_MM, centered=(True, True, False))
    bar = bar.translate((x, 0, 0))
    bar = _add_bar_hinge(bar, 0)

    return boom.union(post).union(bar)


def main() -> None:
    print("Generating hexbug farm gate parts...")
    print(f"  skirt hinge holes: {_hinge_hole():.2f} mm (filament {p.FILAMENT_DIAMETER_MM} + {p.SKIRT_HINGE_HOLE_OVERSIZE_MM})")
    _export(make_base_assembly(), "base_assembly")
    _export(make_gate_post(), "gate_post")
    _export(make_boom_arm(), "boom_arm")
    _export(make_skirt_retaining_bar(), "skirt_retaining_bar")
    _export(make_skirt_post(), "skirt_post")
    _export(make_skirt_assembly(), "skirt_assembly_preview")
    _export(make_hinge_joint_preview(), "hinge_joint_preview")
    _export(make_horn_adapter(), "horn_adapter")
    print("Done.")


if __name__ == "__main__":
    main()
