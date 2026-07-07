"""
Render assembled and exploded views of the hexbug farm gate (includes SG90 servo + desk base).

Usage:
    python render_assembly.py

Output:
    output/views/assembly_closed_<angle>.png
    output/views/assembly_exploded_<angle>.png
    output/views/assembly_closed_all_angles.png  (contact sheet)
"""

from __future__ import annotations

import sys
from pathlib import Path

import cadquery as cq
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import params as p  # noqa: E402
from generate_gate import (  # noqa: E402
    make_base_assembly,
    make_boom_arm,
    make_gate_post,
    make_horn_adapter,
    make_skirt_assembly,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "views"

COLORS = {
    "base": "#795548",
    "post": "#9e9e9e",
    "boom": "#d32f2f",
    "skirt": "#616161",
    "pin": "#ffc107",
    "adapter": "#ff9800",
    "servo": "#1565c0",
    "horn": "#212121",
}

# Camera presets: (elevation°, azimuth°, label)
VIEW_ANGLES: dict[str, tuple[float, float, str]] = {
    "iso": (24, -52, "Isometric"),
    "front": (8, -90, "Front"),
    "back": (8, 90, "Back"),
    "right": (5, 0, "Right"),
    "left": (5, 180, "Left"),
    "top": (90, -90, "Top"),
}


def make_servo_body() -> cq.Workplane:
    body = cq.Workplane("XY").box(
        p.SERVO_BODY_WIDTH_MM,
        p.SERVO_BODY_LENGTH_MM,
        p.SERVO_BODY_HEIGHT_MM,
        centered=(True, True, False),
    )
    ear_y = p.SERVO_BODY_LENGTH_MM / 2 + 1.5
    for x in (-p.SERVO_FLANGE_WIDTH_MM / 2 + 3, p.SERVO_FLANGE_WIDTH_MM / 2 - 3):
        ear = (
            cq.Workplane("XY")
            .center(x, ear_y)
            .box(6, 3, p.SERVO_FLANGE_THICKNESS_MM, centered=(True, True, False))
        )
        body = body.union(ear)
    wire = (
        cq.Workplane("XY")
        .center(-p.SERVO_BODY_WIDTH_MM / 2 + 2, -p.SERVO_BODY_LENGTH_MM / 2 + 4)
        .box(4, 8, 6, centered=(True, True, False))
    )
    return body.union(wire)


def make_servo_horn() -> cq.Workplane:
    hub = cq.Workplane("XY").circle(3.5).extrude(4)
    arm = cq.Workplane("XY").box(18, 4, 2, centered=(False, True, False)).translate((3, 0, 4))
    return hub.union(arm)


def _mesh_from_wp(wp: cq.Workplane, loc: tuple[float, float, float], tol: float = 0.35):
    verts, tris = wp.val().tessellate(tol)
    pts = np.array([(v.x + loc[0], v.y + loc[1], v.z + loc[2]) for v in verts])
    return pts, tris


def _add_part(ax, wp, loc, color, alpha=0.95, tol=0.35) -> None:
    pts, tris = _mesh_from_wp(wp, loc, tol)
    polys = [[pts[i] for i in tri] for tri in tris]
    ax.add_collection3d(
        Poly3DCollection(
            polys,
            facecolor=color,
            edgecolor=(0, 0, 0, 0.1),
            linewidth=0.12,
            alpha=alpha,
        )
    )


def _post_origin() -> tuple[float, float, float]:
    return (p.POST_CENTER_X_MM, 0.0, p.BASE_THICKNESS_MM)


def _hinge_x_positions() -> tuple[float, float]:
    ox, _, _ = _post_origin()
    local = (
        (p.BOOM_LENGTH_MM - p.SKIRT_HINGE_SPAN_MM) / 2,
        (p.BOOM_LENGTH_MM + p.SKIRT_HINGE_SPAN_MM) / 2,
    )
    return (ox + local[0], ox + local[1])


def _skirt_rail_position() -> tuple[float, float, float]:
    ox, oy, oz = _post_origin()
    boom_z = oz + p.BOOM_AXIS_HEIGHT_MM
    rail_z = (
        boom_z
        - p.BOOM_HEIGHT_MM
        - p.SKIRT_HINGE_BOSS_HEIGHT_MM
        - p.SKIRT_POST_LENGTH_MM
        - p.SKIRT_LOWER_RAIL_HEIGHT_MM
    )
    skirt_start = (p.BOOM_LENGTH_MM - p.SKIRT_HINGE_SPAN_MM) / 2
    return (ox + skirt_start, oy, rail_z)


def assembly_positions_fixed() -> dict[str, tuple[float, float, float]]:
    ox, oy, oz = _post_origin()
    inner_h = p.SERVO_BODY_HEIGHT_MM + p.CLEARANCE_MM
    boom_z = oz + p.BOOM_AXIS_HEIGHT_MM
    rail_x, rail_y, rail_z = _skirt_rail_position()

    return {
        "base": (0.0, 0.0, 0.0),
        "post": (ox, oy, oz),
        "servo": (ox, oy + 2.0, oz + p.POST_HEIGHT_MM - inner_h),
        "horn": (ox, oy + p.POST_DEPTH_MM / 2 - 6, oz + p.POST_HEIGHT_MM - 16),
        "adapter": (ox + 2.0, oy + p.POST_DEPTH_MM / 2 - 8, oz + p.POST_HEIGHT_MM - 18),
        "boom": (ox, oy, boom_z),
        "skirt": (rail_x, rail_y, rail_z),
    }


def exploded_offsets() -> dict[str, tuple[float, float, float]]:
    return {
        "base": (0.0, 0.0, 0.0),
        "post": (0.0, 0.0, 25.0),
        "servo": (0.0, -30.0, 35.0),
        "horn": (0.0, -20.0, 45.0),
        "adapter": (-25.0, -15.0, 40.0),
        "boom": (0.0, 0.0, 45.0),
        "skirt": (0.0, 0.0, -45.0),
    }


def _part_list():
    return [
        ("base", make_base_assembly(), COLORS["base"]),
        ("post", make_gate_post(), COLORS["post"]),
        ("servo", make_servo_body(), COLORS["servo"]),
        ("horn", make_servo_horn(), COLORS["horn"]),
        ("adapter", make_horn_adapter(), COLORS["adapter"]),
        ("boom", make_boom_arm(), COLORS["boom"]),
        ("skirt", make_skirt_assembly(), COLORS["skirt"]),
    ]


def _legend_items():
    return [
        ("Desk base + rest pillar", COLORS["base"]),
        ("Gate post", COLORS["post"]),
        ("SG90 servo", COLORS["servo"]),
        ("Servo horn", COLORS["horn"]),
        ("Horn adapter", COLORS["adapter"]),
        ("Boom arm (lifts up)", COLORS["boom"]),
        ("Skirt + retaining bar", COLORS["skirt"]),
    ]


def _draw_assembly(ax, exploded: bool) -> None:
    base_pos = assembly_positions_fixed()
    offsets = exploded_offsets() if exploded else {k: (0.0, 0.0, 0.0) for k in base_pos}

    for key, wp, color in _part_list():
        bx, by, bz = base_pos[key]
        ox, oy, oz = offsets[key]
        alpha = 0.88 if key == "servo" and not exploded else 0.95
        _add_part(ax, wp, (bx + ox, by + oy, bz + oz), color, alpha=alpha)

    # Desk surface hint
    gx = np.linspace(-10, p.BASE_LENGTH_MM + 10, 2)
    gy = np.linspace(-p.BASE_WIDTH_MM, p.BASE_WIDTH_MM, 2)
    gxx, gyy = np.meshgrid(gx, gy)
    gzz = np.zeros_like(gxx) - 0.1
    ax.plot_surface(gxx, gyy, gzz, color="#cfd8dc", alpha=0.4, shade=False)


def _configure_axes(ax, title: str, elev: float, azim: float) -> None:
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.view_init(elev=elev, azim=azim)
    ax.set_box_aspect((1.5, 0.55, 0.75))
    ax.set_xlim(-15, p.BASE_LENGTH_MM + 15)
    ax.set_ylim(-40, 40)
    ax.set_zlim(-3, p.BASE_THICKNESS_MM + p.POST_HEIGHT_MM + 15)

    for label, color in _legend_items():
        ax.scatter([], [], [], color=color, s=60, label=label)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0), fontsize=7, framealpha=0.9)


def _render_single(exploded: bool, angle_key: str, elev: float, azim: float, label: str, out_path: Path) -> None:
    mode = "Exploded" if exploded else "Assembled (Closed)"
    fig = plt.figure(figsize=(12, 8), facecolor="white")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#fafafa")
    _draw_assembly(ax, exploded)
    _configure_axes(ax, f"Hexbug Farm Gate — {mode} — {label}", elev, azim)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved {out_path.name}")


def _render_contact_sheet(exploded: bool, out_path: Path) -> None:
    mode = "Exploded" if exploded else "Assembled"
    fig = plt.figure(figsize=(18, 11), facecolor="white")
    keys = list(VIEW_ANGLES.keys())

    for i, key in enumerate(keys):
        elev, azim, label = VIEW_ANGLES[key]
        ax = fig.add_subplot(2, 3, i + 1, projection="3d")
        ax.set_facecolor("#fafafa")
        _draw_assembly(ax, exploded)
        ax.view_init(elev=elev, azim=azim)
        ax.set_box_aspect((1.5, 0.55, 0.75))
        ax.set_xlim(-15, p.BASE_LENGTH_MM + 15)
        ax.set_ylim(-40, 40)
        ax.set_zlim(-3, p.BASE_THICKNESS_MM + p.POST_HEIGHT_MM + 15)
        ax.set_title(label, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

    fig.suptitle(f"Hexbug Farm Gate — {mode} — All Angles", fontsize=14, fontweight="bold", y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved {out_path.name}")


def main() -> None:
    print("Rendering multi-angle assembly views...")
    prefix_closed = "assembly_closed"
    prefix_exploded = "assembly_exploded"

    for key, (elev, azim, label) in VIEW_ANGLES.items():
        _render_single(
            exploded=False,
            angle_key=key,
            elev=elev,
            azim=azim,
            label=label,
            out_path=OUTPUT_DIR / f"{prefix_closed}_{key}.png",
        )
        _render_single(
            exploded=True,
            angle_key=key,
            elev=elev,
            azim=azim,
            label=label,
            out_path=OUTPUT_DIR / f"{prefix_exploded}_{key}.png",
        )

    _render_contact_sheet(exploded=False, out_path=OUTPUT_DIR / f"{prefix_closed}_all_angles.png")
    _render_contact_sheet(exploded=True, out_path=OUTPUT_DIR / f"{prefix_exploded}_all_angles.png")

    # Legacy single-file paths for convenience
    import shutil

    legacy_dir = OUTPUT_DIR.parent
    shutil.copy(OUTPUT_DIR / f"{prefix_closed}_iso.png", legacy_dir / "assembly_closed.png")
    shutil.copy(OUTPUT_DIR / f"{prefix_exploded}_iso.png", legacy_dir / "assembly_exploded.png")

    print("Done.")


if __name__ == "__main__":
    main()
