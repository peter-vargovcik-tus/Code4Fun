"""
Rev 2 — boom arm with integrated SG90 horn socket + skirt post hinge lugs.

Mates with f_skirt_post.stl (pin along Y in this model; post hangs in -Z).

Usage:
    pip install cadquery
    python generate_arm.py

Output: ../output/*.step and *.stl
"""

from __future__ import annotations

import sys
from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import params as p  # noqa: E402

OUTPUT_DIR = ROOT / "output"


def _pin_cutter(x: float, z: float, y_half: float = 6.0) -> cq.Workplane:
    return (
        cq.Workplane("XZ")
        .center(x, z)
        .circle(p.POST_HINGE_HOLE_DIAMETER_MM / 2)
        .extrude(y_half, both=True)
    )


def _hinge_lug(x: float, z_pin: float) -> cq.Workplane:
    """Round lug on boom / bar; pin along Y."""
    r = p.POST_HINGE_BOSS_OD_MM / 2
    ty = p.POST_HINGE_BOSS_THICKNESS_MM
    lug = (
        cq.Workplane("XZ")
        .center(x, z_pin)
        .circle(r)
        .extrude(ty, both=True)
    )
    return lug.cut(_pin_cutter(x, z_pin, ty / 2 + 1.0))


def _horn_socket() -> cq.Workplane:
    """SG90 cross-horn screw pattern + centre boss clearance."""
    plate = (
        cq.Workplane("XY")
        .circle(p.HORN_SOCKET_DIAMETER_MM / 2)
        .extrude(p.HORN_SOCKET_THICKNESS_MM)
    )

    plate = (
        plate.faces(">Z")
        .workplane()
        .pushPoints(
            [
                (-p.HORN_HOLE_SPAN_MM / 2, 0),
                (p.HORN_HOLE_SPAN_MM / 2, 0),
                (0, -p.HORN_HOLE_SPAN_MM / 2),
                (0, p.HORN_HOLE_SPAN_MM / 2),
            ]
        )
        .hole(p.HORN_HOLE_DIAMETER_MM, depth=p.HORN_SCREW_DEPTH_MM + 0.5)
    )

    plate = (
        plate.faces(">Z")
        .workplane()
        .hole(p.HORN_CENTER_BOSS_DIAMETER_MM, depth=p.HORN_SOCKET_THICKNESS_MM + 0.5)
    )
    return plate


def _skirt_hinge_x_positions() -> list[float]:
    start = (p.BOOM_LENGTH_MM - p.SKIRT_HINGE_SPAN_MM) / 2
    spacing = (
        p.SKIRT_HINGE_SPAN_MM / (p.SKIRT_BAR_COUNT - 1)
        if p.SKIRT_BAR_COUNT > 1
        else 0.0
    )
    return [start + i * spacing for i in range(p.SKIRT_BAR_COUNT)]


def make_boom_arm() -> cq.Workplane:
    """
    Single part: horn socket at root + boom beam + underside hinge lugs.

    Mount: horn socket flush on SG90 horn (Z up). Boom extends +X when closed.
    """
    socket = _horn_socket()

    boom = cq.Workplane("XY").box(
        p.BOOM_LENGTH_MM,
        p.BOOM_WIDTH_MM,
        p.BOOM_HEIGHT_MM,
        centered=(False, True, False),
    )
    boom = boom.translate((0, 0, p.HORN_SOCKET_THICKNESS_MM))

    arm = socket.union(boom)

    z_pin = p.HORN_SOCKET_THICKNESS_MM - p.BOOM_HINGE_LUG_DROP_MM
    for x in _skirt_hinge_x_positions():
        arm = arm.union(_hinge_lug(x, z_pin))

    return arm


def make_retaining_bar() -> cq.Workplane:
    """Bottom hinge bar — hangs from post lower donuts."""
    span = p.SKIRT_HINGE_SPAN_MM
    bar = (
        cq.Workplane("XY")
        .box(span, p.RETAINING_BAR_WIDTH_MM, p.RETAINING_BAR_HEIGHT_MM, centered=(True, True, False))
        .translate((span / 2, 0, 0))
    )

    spacing = span / (p.SKIRT_BAR_COUNT - 1) if p.SKIRT_BAR_COUNT > 1 else span
    z_pin = p.RETAINING_BAR_HEIGHT_MM + p.BOOM_HINGE_LUG_DROP_MM
    for i in range(p.SKIRT_BAR_COUNT):
        bar = bar.union(_hinge_lug(i * spacing, z_pin))

    return bar


def make_hinge_preview() -> cq.Workplane:
    """One hinge station for Fusion inspection (boom lug + bar lug, gap for post)."""
    x = 0.0
    z_boom_bottom = p.HORN_SOCKET_THICKNESS_MM
    z_pin_top = z_boom_bottom - p.BOOM_HINGE_LUG_DROP_MM
    z_pin_bot = z_pin_top - p.POST_HINGE_CENTER_SPACING_MM

    boom = cq.Workplane("XY").box(25, p.BOOM_WIDTH_MM, p.BOOM_HEIGHT_MM, centered=(False, True, False))
    boom = boom.translate((-5, 0, z_boom_bottom))
    boom = boom.union(_hinge_lug(x, z_pin_top))

    bar_top = z_pin_bot - p.BOOM_HINGE_LUG_DROP_MM
    bar = cq.Workplane("XY").box(
        20, p.RETAINING_BAR_WIDTH_MM, p.RETAINING_BAR_HEIGHT_MM, centered=(True, True, False)
    )
    bar = bar.translate((x, 0, bar_top - p.RETAINING_BAR_HEIGHT_MM))
    bar = bar.union(_hinge_lug(x, z_pin_bot))

    return boom.union(bar)


def _export(result: cq.Workplane, name: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    step = OUTPUT_DIR / f"{name}.step"
    stl = OUTPUT_DIR / f"{name}.stl"
    cq.exporters.export(result, str(step))
    cq.exporters.export(result, str(stl))
    print(f"  exported {step.name}, {stl.name}")


def main() -> None:
    print("Rev 2 — boom arm for f_skirt_post.stl")
    print(f"  reference post: {p.REFERENCE_POST_STL.name}")
    print(f"  post hinge spacing: {p.POST_HINGE_CENTER_SPACING_MM} mm")
    print(f"  skirt stations: {p.SKIRT_BAR_COUNT} over {p.SKIRT_HINGE_SPAN_MM} mm")
    _export(make_boom_arm(), "boom_arm")
    _export(make_retaining_bar(), "skirt_retaining_bar")
    _export(make_hinge_preview(), "hinge_joint_preview")
    print("Done.")


if __name__ == "__main__":
    main()
