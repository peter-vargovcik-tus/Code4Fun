"""
Animate hexbug farm gate: boom lifts UPWARD (no horizontal sweep).

Side view uses **Pymunk physics** — rigid posts with real joints (no stretching).
Iso view uses a kinematic preview.

Usage:
    python animate_gate.py              # side MP4 (physics) + iso MP4
    python animate_gate_physics.py      # physics side MP4 only

Output:
    output/animation/gate_action_side.mp4   — side view (XZ), clearest motion
    output/animation/gate_action_iso.mp4    — isometric 3D view
    output/animation/frames/                — individual PNG frames
"""

from __future__ import annotations

import math
import sys
from io import BytesIO
from pathlib import Path

import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import params as p  # noqa: E402

OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "animation"
FRAMES_DIR = OUTPUT_DIR / "frames"

# Colours
C_BASE = "#795548"
C_POST = "#9e9e9e"
C_PILLAR = "#6d4c41"
C_BOOM = "#d32f2f"
C_SKIRT = "#424242"
C_RAIL = "#757575"
C_SERVO = "#1565c0"
C_HINGE = "#ffc107"
C_FLOOR = "#eceff1"
C_SHEEP = "#a5d6a7"  # hexbug placeholder dots


def _deg(rad: float) -> float:
    return math.degrees(rad)


def _rad(deg: float) -> float:
    return math.radians(deg)


class GateKinematics:
    """Boom rotates upward in XZ plane around Y axis at post centre."""

    def __init__(self) -> None:
        self.ox = p.POST_CENTER_X_MM
        self.oy = 0.0
        self.z_base = p.BASE_THICKNESS_MM
        self.z_pivot = self.z_base + p.BOOM_AXIS_HEIGHT_MM + p.BOOM_HEIGHT_MM / 2
        self.skirt_start = (p.BOOM_LENGTH_MM - p.SKIRT_HINGE_SPAN_MM) / 2
        self.spacing = (
            p.SKIRT_HINGE_SPAN_MM / (p.SKIRT_BAR_COUNT - 1)
            if p.SKIRT_BAR_COUNT > 1
            else 0.0
        )
        self.post_s = [self.skirt_start + i * self.spacing for i in range(p.SKIRT_BAR_COUNT)]
        self.z_rail = self._closed_rail_z()
        self.rail_x0 = self.ox + self.skirt_start
        self.rail_x1 = self.rail_x0 + p.SKIRT_HINGE_SPAN_MM

    def _closed_rail_z(self) -> float:
        top_z = (
            self.z_pivot
            - p.BOOM_HEIGHT_MM / 2
            - p.SKIRT_HINGE_BOSS_HEIGHT_MM
        )
        return top_z - p.SKIRT_POST_LENGTH_MM - p.SKIRT_LOWER_RAIL_HEIGHT_MM / 2

    def _bottom_positions(self) -> list[tuple[float, float]]:
        return [(self.ox + s, self.z_rail + p.SKIRT_LOWER_RAIL_HEIGHT_MM / 2) for s in self.post_s]

    def boom_angle_rad(self, t: float) -> float:
        """t in [0,1] → angle from closed (0°) to open (90°)."""
        return _rad(p.BOOM_CLOSED_ANGLE_DEG + t * (p.BOOM_OPEN_ANGLE_DEG - p.BOOM_CLOSED_ANGLE_DEG))

    def boom_corners_xz(self, theta: float) -> np.ndarray:
        """Boom rectangle corners in XZ (closed profile extruded in Y)."""
        half_w = p.BOOM_WIDTH_MM / 2
        half_h = p.BOOM_HEIGHT_MM / 2
        local = np.array(
            [
                [0, -half_h],
                [p.BOOM_LENGTH_MM, -half_h],
                [p.BOOM_LENGTH_MM, half_h],
                [0, half_h],
            ]
        )
        c, s = math.cos(theta), math.sin(theta)
        rot = np.array([[c, -s], [s, c]])
        world = (rot @ local.T).T
        world[:, 0] += self.ox
        world[:, 1] += self.z_pivot
        return world

    def top_hinge_xz(self, theta: float, s_along_boom: float) -> tuple[float, float]:
        """Skirt top hinge on boom underside at distance s from root."""
        cx = self.ox + s_along_boom * math.cos(theta)
        cz = self.z_pivot + s_along_boom * math.sin(theta)
        down_x = -math.sin(theta)
        down_z = -math.cos(theta)
        offset = p.BOOM_HEIGHT_MM / 2 + p.SKIRT_HINGE_BOSS_HEIGHT_MM / 2
        return (cx + down_x * offset, cz + down_z * offset)

    def skirt_posts(self, theta: float) -> list[tuple[tuple[float, float], tuple[float, float]]]:
        """Each post as (bottom hinge, top hinge) in XZ."""
        bottoms = self._bottom_positions()
        return [(btm, self.top_hinge_xz(theta, s)) for btm, s in zip(bottoms, self.post_s)]

    def boom_tip_xz(self, theta: float) -> tuple[float, float]:
        return self.top_hinge_xz(theta, p.BOOM_LENGTH_MM)  # approx tip on centreline


def _draw_side_frame(ax, kin: GateKinematics, theta: float, t: float, show_sheep: bool = True) -> None:
    ax.clear()
    ax.set_facecolor(C_FLOOR)
    ax.set_xlim(-5, p.BASE_LENGTH_MM + 10)
    ax.set_ylim(-5, p.BASE_THICKNESS_MM + p.POST_HEIGHT_MM + 20)
    ax.set_aspect("equal")
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Z (mm)")

    angle_deg = _deg(theta)
    ax.set_title(
        f"Gate action — boom lifts UP ({angle_deg:.0f}°)  |  t={t:.0%}",
        fontsize=11,
        fontweight="bold",
    )

    # Desk / base
    ax.add_patch(
        Rectangle(
            (0, 0), p.BASE_LENGTH_MM, p.BASE_THICKNESS_MM,
            facecolor=C_BASE, edgecolor="black", linewidth=0.8,
        )
    )

    # Left post
    px = kin.ox - p.POST_WIDTH_MM / 2
    ax.add_patch(
        Rectangle(
            (px, kin.z_base), p.POST_WIDTH_MM, p.POST_HEIGHT_MM,
            facecolor=C_POST, edgecolor="black", linewidth=0.6,
        )
    )

    # Servo (schematic)
    sz = kin.z_base + p.POST_HEIGHT_MM - p.SERVO_BODY_HEIGHT_MM - 2
    ax.add_patch(
        Rectangle(
            (kin.ox - p.SERVO_BODY_WIDTH_MM / 2, sz),
            p.SERVO_BODY_WIDTH_MM, p.SERVO_BODY_HEIGHT_MM,
            facecolor=C_SERVO, edgecolor="black", linewidth=0.5, alpha=0.9,
        )
    )

    # Right rest pillar
    px2 = p.PILLAR_CENTER_X_MM - p.PILLAR_WIDTH_MM / 2
    ax.add_patch(
        Rectangle(
            (px2, kin.z_base), p.PILLAR_WIDTH_MM, p.BOOM_AXIS_HEIGHT_MM,
            facecolor=C_PILLAR, edgecolor="black", linewidth=0.6,
        )
    )

    # Lower rail (fixed)
    ax.add_patch(
        Rectangle(
            (kin.rail_x0, kin.z_rail),
            p.SKIRT_HINGE_SPAN_MM, p.SKIRT_LOWER_RAIL_HEIGHT_MM,
            facecolor=C_RAIL, edgecolor="black", linewidth=0.5,
        )
    )

    # Skirt posts
    for (bx, bz), (tx, tz) in kin.skirt_posts(theta):
        ax.plot([bx, tx], [bz, tz], color=C_SKIRT, linewidth=p.SKIRT_BAR_DIAMETER_MM * 0.55, solid_capstyle="round")
        ax.plot(bx, bz, "o", color=C_HINGE, markersize=4, zorder=5)
        ax.plot(tx, tz, "o", color=C_HINGE, markersize=4, zorder=5)

    # Boom
    boom_poly = Polygon(
        kin.boom_corners_xz(theta),
        closed=True, facecolor=C_BOOM, edgecolor="black", linewidth=0.8, zorder=4,
    )
    ax.add_patch(boom_poly)

    # Pivot marker
    ax.plot(kin.ox, kin.z_pivot, "+", color="black", markersize=10, markeredgewidth=2, zorder=6)
    ax.annotate("servo pivot", (kin.ox + 2, kin.z_pivot + 3), fontsize=7, color="#333")

    # Hexbug / sheep placeholders under gate (not pushed sideways — boom lifts up)
    if show_sheep:
        for sx in np.linspace(kin.ox + 20, kin.rail_x1 - 5, 5):
            ax.plot(sx, kin.z_base + 2, "o", color=C_SHEEP, markersize=8, zorder=2)
        ax.annotate(
            "hexbugs (not swept — boom rises)",
            (kin.ox + 25, kin.z_base + 8),
            fontsize=7,
            color="#2e7d32",
            style="italic",
        )

    # Motion arrow hint at start
    if t < 0.15:
        ax.annotate(
            "", xy=(kin.ox + 5, kin.z_pivot + 25), xytext=(kin.ox + 5, kin.z_pivot + 5),
            arrowprops=dict(arrowstyle="->", color="#1565c0", lw=2),
        )
        ax.text(kin.ox + 8, kin.z_pivot + 18, "lifts up", fontsize=7, color="#1565c0")

    ax.axhline(kin.z_base, color="#bbb", linewidth=0.5)
    ax.grid(True, alpha=0.25)


def _boom_box_3d(kin: GateKinematics, theta: float) -> np.ndarray:
    """8 corners of boom box in 3D."""
    xz = kin.boom_corners_xz(theta)
    hw = p.BOOM_WIDTH_MM / 2
    pts = []
    for x, z in xz:
        pts.append([x, -hw, z])
        pts.append([x, hw, z])
    return np.array(pts)


def _box_faces(corners: np.ndarray) -> list:
    """Triangulate box from 8 corners (bottom 0,1,2,3 / top 4,5,6,7 alternating y)."""
    # corners: [x,-hw,z], [x,hw,z] pairs for each xz corner
    idx = list(range(8))
    faces = [
        [0, 2, 6], [0, 6, 4],
        [1, 5, 7], [1, 7, 3],
        [0, 1, 3], [0, 3, 2],
        [4, 6, 7], [4, 7, 5],
        [0, 4, 5], [0, 5, 1],
        [2, 3, 7], [2, 7, 6],
    ]
    return [[corners[i] for i in f] for f in faces]


def _draw_iso_frame(ax, kin: GateKinematics, theta: float, t: float) -> None:
    ax.clear()
    ax.set_facecolor("#fafafa")

    def add_box(x0, y0, z0, dx, dy, dz, color, alpha=0.95):
        corners = np.array([
            [x0, y0, z0], [x0+dx, y0, z0], [x0+dx, y0+dy, z0], [x0, y0+dy, z0],
            [x0, y0, z0+dz], [x0+dx, y0, z0+dz], [x0+dx, y0+dy, z0+dz], [x0, y0+dy, z0+dz],
        ])
        faces = [
            [0,1,2],[0,2,3],[4,5,6],[4,6,7],[0,1,5],[0,5,4],
            [1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7],
        ]
        ax.add_collection3d(Poly3DCollection(
            [[corners[i] for i in f] for f in faces],
            facecolor=color, edgecolor="black", linewidth=0.2, alpha=alpha,
        ))

    add_box(0, -p.BASE_WIDTH_MM/2, 0, p.BASE_LENGTH_MM, p.BASE_WIDTH_MM, p.BASE_THICKNESS_MM, C_BASE)
    add_box(kin.ox - p.POST_WIDTH_MM/2, -p.POST_DEPTH_MM/2, kin.z_base,
            p.POST_WIDTH_MM, p.POST_DEPTH_MM, p.POST_HEIGHT_MM, C_POST)
    add_box(p.PILLAR_CENTER_X_MM - p.PILLAR_WIDTH_MM/2, -p.PILLAR_DEPTH_MM/2, kin.z_base,
            p.PILLAR_WIDTH_MM, p.PILLAR_DEPTH_MM, p.BOOM_AXIS_HEIGHT_MM, C_PILLAR)
    add_box(kin.rail_x0, -p.BOOM_WIDTH_MM/2, kin.z_rail,
            p.SKIRT_HINGE_SPAN_MM, p.BOOM_WIDTH_MM, p.SKIRT_LOWER_RAIL_HEIGHT_MM, C_RAIL)

    boom_pts = _boom_box_3d(kin, theta)
    ax.add_collection3d(Poly3DCollection(
        _box_faces(boom_pts), facecolor=C_BOOM, edgecolor="black", linewidth=0.3, alpha=0.95,
    ))

    for (bx, bz), (tx, tz) in kin.skirt_posts(theta):
        ax.plot([bx, tx], [0, 0], [bz, tz], color=C_SKIRT, linewidth=2)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(f"Isometric — boom {_deg(theta):.0f}° up", fontsize=10, fontweight="bold")
    ax.view_init(elev=20, azim=-55)
    ax.set_xlim(-10, p.BASE_LENGTH_MM + 10)
    ax.set_ylim(-35, 35)
    ax.set_zlim(0, p.POST_HEIGHT_MM + 20)
    ax.set_box_aspect((1.5, 0.5, 0.7))


def _capture_frame(fig, dpi: int = 120) -> np.ndarray:
    """Rasterise the current figure to an RGB numpy array."""
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", facecolor="white")
    buf.seek(0)
    return iio.imread(buf)


def _make_mp4(
    kin: GateKinematics,
    out_path: Path,
    n_frames: int = 48,
    fps: int = 24,
    figsize=(10, 6),
    three_d: bool = False,
    dpi: int = 120,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    frames: list[np.ndarray] = []

    for i in range(n_frames):
        t = i / (n_frames - 1)
        te = 0.5 - 0.5 * math.cos(math.pi * t)
        theta = kin.boom_angle_rad(te)

        fig = plt.figure(figsize=figsize, facecolor="white")
        ax = fig.add_subplot(111, projection="3d" if three_d else None)
        if three_d:
            _draw_iso_frame(ax, kin, theta, te)
        else:
            _draw_side_frame(ax, kin, theta, te)
        frames.append(_capture_frame(fig, dpi=dpi))
        plt.close(fig)

    iio.imwrite(
        out_path,
        frames,
        fps=fps,
        codec="libx264",
        pixelformat="yuv420p",
        quality=8,
    )
    print(f"  saved {out_path}")


def _save_key_frames(kin: GateKinematics) -> None:
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    for label, t in [("closed", 0.0), ("quarter", 0.25), ("half", 0.5), ("open", 1.0)]:
        theta = kin.boom_angle_rad(t)
        fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
        _draw_side_frame(ax, kin, theta, t)
        path = FRAMES_DIR / f"side_{label}.png"
        fig.savefig(path, dpi=140, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        print(f"  saved {path.name}")


def main() -> None:
    from animate_gate_physics import _draw_physics_frame, GatePhysicsSim, render_physics_mp4

    print("Building gate animation...")
    kin = GateKinematics()

    # Side view: parallelogram kinematics (vertical posts, bar parallel to boom)
    print("  side view — parallelogram skirt kinematics")
    sim = render_physics_mp4(OUTPUT_DIR / "gate_action_side.mp4")

    # Key frames
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    for label, t in [("closed", 0.0), ("quarter", 0.25), ("half", 0.5), ("open", 1.0)]:
        sim.set_angle(sim.boom_angle_rad(t))
        fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
        _draw_physics_frame(ax, sim, t)
        path = FRAMES_DIR / f"side_{label}.png"
        fig.savefig(path, dpi=140, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        print(f"  saved {path.name}")

    # Iso view: kinematic preview (3D rigid-body not modelled here)
    print("  iso view — kinematic preview")
    _make_mp4(
        kin,
        OUTPUT_DIR / "gate_action_iso.mp4",
        n_frames=36, fps=20, figsize=(9, 7), three_d=True,
    )

    print("\nSummary:")
    print(f"  Pivot: ({kin.ox:.0f}, {kin.z_pivot:.0f}) mm")
    print(f"  Boom: {p.BOOM_CLOSED_ANGLE_DEG:.0f} to {p.BOOM_OPEN_ANGLE_DEG:.0f} deg (upward)")
    print(f"  Skirt: {p.SKIRT_BAR_COUNT} posts + hanging bar (parallelogram)")
    print(f"  Hinge housings: {p.SKIRT_HINGE_BOSS_OD_MM:.0f} mm OD donuts, pin along Y")
    print("Done.")


if __name__ == "__main__":
    main()
