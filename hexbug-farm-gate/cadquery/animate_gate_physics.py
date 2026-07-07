"""
Physics-based gate animation — parallelogram skirt kinematics (like real barrier gates).

Posts stay vertical; retaining bar stays parallel to boom; skirt folds on upward swing.

Usage:
    python animate_gate_physics.py
    python animate_gate.py
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path

import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import params as p  # noqa: E402

OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "animation"

C_BASE = "#795548"
C_POST = "#9e9e9e"
C_PILLAR = "#6d4c41"
C_BOOM = "#d32f2f"
C_SKIRT = "#424242"
C_RAIL = "#757575"
C_SERVO = "#1565c0"
C_HINGE = "#ffc107"
C_SHEEP = "#a5d6a7"


@dataclass
class ParallelogramGate:
    """Kinematic model: vertical posts + bar parallel to boom."""

    ox: float = field(default_factory=lambda: p.POST_CENTER_X_MM)
    z_base: float = field(default_factory=lambda: p.BASE_THICKNESS_MM)
    z_pivot: float = field(
        default_factory=lambda: p.BASE_THICKNESS_MM + p.BOOM_AXIS_HEIGHT_MM + p.BOOM_HEIGHT_MM / 2
    )
    skirt_start: float = field(
        default_factory=lambda: (p.BOOM_LENGTH_MM - p.SKIRT_HINGE_SPAN_MM) / 2
    )
    spacing: float = field(
        default_factory=lambda: (
            p.SKIRT_HINGE_SPAN_MM / (p.SKIRT_BAR_COUNT - 1)
            if p.SKIRT_BAR_COUNT > 1
            else 0.0
        )
    )
    post_s: list[float] = field(default_factory=list)
    post_length: float = field(default_factory=lambda: float(p.SKIRT_POST_LENGTH_MM))
    theta: float = 0.0

    def __post_init__(self) -> None:
        if not self.post_s:
            self.post_s = [self.skirt_start + i * self.spacing for i in range(p.SKIRT_BAR_COUNT)]

    def boom_angle_rad(self, t: float) -> float:
        return math.radians(
            p.BOOM_CLOSED_ANGLE_DEG + t * (p.BOOM_OPEN_ANGLE_DEG - p.BOOM_CLOSED_ANGLE_DEG)
        )

    def set_angle(self, theta_rad: float) -> None:
        self.theta = theta_rad

    def _boom_unit(self) -> tuple[float, float]:
        return (math.cos(self.theta), math.sin(self.theta))

    def _boom_normal_down(self) -> tuple[float, float]:
        """Unit vector pointing below boom (perpendicular, toward skirt)."""
        return (-math.sin(self.theta), -math.cos(self.theta))

    def _hinge_offset(self) -> float:
        return p.BOOM_HEIGHT_MM / 2 + p.SKIRT_HINGE_BOSS_HEIGHT_MM / 2

    def top_hinge(self, s: float) -> tuple[float, float]:
        """Hinge centre on boom underside at distance s from pivot."""
        ux, uz = self._boom_unit()
        nx, nz = self._boom_normal_down()
        off = self._hinge_offset()
        return (self.ox + s * ux + nx * off, self.z_pivot + s * uz + nz * off)

    def skirt_state(self) -> tuple[list[tuple[tuple[float, float], tuple[float, float]]], np.ndarray]:
        """
        Returns (post segments top→bottom, retaining bar corners).
        Posts constrained vertical; bar parallel to boom (parallelogram).
        """
        ux, uz = self._boom_unit()
        tops = [self.top_hinge(s) for s in self.post_s]
        bots = [(tx, tz - self.post_length) for tx, tz in tops]

        # Bar anchor: hinge 0 bottom lies on bar at same index along parallel link
        s0 = self.post_s[0]
        ax = bots[0][0] - s0 * ux
        az = bots[0][1] - s0 * uz

        half_rh = p.SKIRT_LOWER_RAIL_HEIGHT_MM / 2
        nx, nz = self._boom_normal_down()

        bar_corners = []
        for sign in (-1, 1):
            corner_offset = sign * half_rh
            p0 = (ax + nx * corner_offset, az + nz * corner_offset)
            p1 = (
                ax + p.SKIRT_HINGE_SPAN_MM * ux + nx * corner_offset,
                az + p.SKIRT_HINGE_SPAN_MM * uz + nz * corner_offset,
            )
            bar_corners.extend([p0, p1])

        posts = list(zip(tops, bots))
        return posts, np.array(bar_corners)

    def boom_corners(self) -> np.ndarray:
        hw = p.BOOM_HEIGHT_MM / 2
        local = np.array([[0, -hw], [p.BOOM_LENGTH_MM, -hw], [p.BOOM_LENGTH_MM, hw], [0, hw]])
        c, s = math.cos(self.theta), math.sin(self.theta)
        rot = np.array([[c, -s], [s, c]])
        world = (rot @ local.T).T
        world[:, 0] += self.ox
        world[:, 1] += self.z_pivot
        return world

    @property
    def rail_x1(self) -> float:
        return self.ox + self.skirt_start + p.SKIRT_HINGE_SPAN_MM


def _draw_frame(ax, gate: ParallelogramGate, t: float, show_sheep: bool = True) -> None:
    ax.clear()
    ax.set_facecolor("#eceff1")
    ax.set_xlim(-5, p.BASE_LENGTH_MM + 10)
    ax.set_ylim(-5, p.BASE_THICKNESS_MM + p.POST_HEIGHT_MM + 25)
    ax.set_aspect("equal")
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Z (mm)")
    deg = math.degrees(gate.theta)
    ax.set_title(
        f"Parallelogram skirt — boom {deg:.0f}° up  |  t={t:.0%}",
        fontsize=11,
        fontweight="bold",
    )

    ax.add_patch(Rectangle((0, 0), p.BASE_LENGTH_MM, p.BASE_THICKNESS_MM, facecolor=C_BASE, edgecolor="black", lw=0.8))
    ax.add_patch(Rectangle(
        (gate.ox - p.POST_WIDTH_MM / 2, gate.z_base), p.POST_WIDTH_MM, p.POST_HEIGHT_MM,
        facecolor=C_POST, edgecolor="black", lw=0.6,
    ))
    sz = gate.z_base + p.POST_HEIGHT_MM - p.SERVO_BODY_HEIGHT_MM - 2
    ax.add_patch(Rectangle(
        (gate.ox - p.SERVO_BODY_WIDTH_MM / 2, sz), p.SERVO_BODY_WIDTH_MM, p.SERVO_BODY_HEIGHT_MM,
        facecolor=C_SERVO, edgecolor="black", lw=0.5,
    ))
    ax.add_patch(Rectangle(
        (p.PILLAR_CENTER_X_MM - p.PILLAR_WIDTH_MM / 2, gate.z_base),
        p.PILLAR_WIDTH_MM, p.BOOM_AXIS_HEIGHT_MM,
        facecolor=C_PILLAR, edgecolor="black", lw=0.6,
    ))

    posts, bar_pts = gate.skirt_state()
    # Retaining bar (order corners for polygon)
    bar_poly = Polygon(bar_pts[[0, 1, 3, 2]], closed=True, facecolor=C_RAIL, edgecolor="black", lw=0.6, zorder=2)
    ax.add_patch(bar_poly)

    r_donut = p.SKIRT_HINGE_BOSS_OD_MM / 2 * 0.45
    for (top, bot) in posts:
        ax.plot(
            [top[0], bot[0]], [top[1], bot[1]],
            color=C_SKIRT, linewidth=p.SKIRT_BAR_DIAMETER_MM * 0.55,
            solid_capstyle="round", zorder=3,
        )
        for pt in (top, bot):
            ax.add_patch(Circle(pt, r_donut, facecolor=C_HINGE, edgecolor="black", lw=0.4, zorder=5))

    ax.add_patch(Polygon(gate.boom_corners(), closed=True, facecolor=C_BOOM, edgecolor="black", lw=0.8, zorder=4))
    ax.plot(gate.ox, gate.z_pivot, "+", color="black", markersize=10, markeredgewidth=2, zorder=6)

    if show_sheep:
        for sx in np.linspace(gate.ox + 20, gate.rail_x1 - 5, 5):
            ax.plot(sx, gate.z_base + 2, "o", color=C_SHEEP, markersize=8, zorder=1)

    ax.text(5, 12, "posts vertical · bar ∥ boom (parallelogram)", fontsize=7, color="#555", style="italic")
    ax.grid(True, alpha=0.25)


def _capture_frame(fig, dpi: int = 120) -> np.ndarray:
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", facecolor="white")
    buf.seek(0)
    return iio.imread(buf)


def render_parallelogram_mp4(
    out_path: Path,
    n_frames: int = 48,
    fps: int = 24,
) -> ParallelogramGate:
    gate = ParallelogramGate()
    frames: list[np.ndarray] = []

    for i in range(n_frames):
        t_lin = i / max(n_frames - 1, 1)
        t = 0.5 - 0.5 * math.cos(math.pi * t_lin)
        gate.set_angle(gate.boom_angle_rad(t))

        fig, ax = plt.subplots(figsize=(11, 6.5), facecolor="white")
        _draw_frame(ax, gate, t)
        frames.append(_capture_frame(fig))
        plt.close(fig)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    iio.imwrite(out_path, frames, fps=fps, codec="libx264", pixelformat="yuv420p", quality=8)
    print(f"  saved {out_path}")
    return gate


# Backward-compatible alias for animate_gate.py
GatePhysicsSim = ParallelogramGate


def _draw_physics_frame(ax, gate: ParallelogramGate, t: float, show_sheep: bool = True) -> None:
    _draw_frame(ax, gate, t, show_sheep)


def render_physics_mp4(
    out_path: Path,
    n_frames: int = 48,
    fps: int = 24,
    settle_steps: int = 0,
) -> ParallelogramGate:
    return render_parallelogram_mp4(out_path, n_frames=n_frames, fps=fps)


def main() -> None:
    print("Building parallelogram gate animation...")
    render_parallelogram_mp4(OUTPUT_DIR / "gate_action_side_physics.mp4")
    print("Done.")


if __name__ == "__main__":
    main()
