"""
Diagnostic: show why current skirt hinge holes don't align.
Pin must pass along Y; current model drills holes along Z.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import params as p
from generate_gate import make_boom_arm, make_skirt_post, make_skirt_retaining_bar

OUT = Path(__file__).resolve().parent / "output" / "diagnostics"
OUT.mkdir(parents=True, exist_ok=True)


def _save(fig, name):
    fig.savefig(OUT / name, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved {name}")


def diagram_expected_vs_actual():
    """Schematic of correct vs current hole axis."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Skirt hinge problem: hole axis must be Y (through clevis), not Z", fontweight="bold")

    for ax, title, correct in zip(axes, ["CORRECT (needed)", "CURRENT CAD (broken)"], [True, False]):
        ax.set_xlim(-6, 6)
        ax.set_ylim(-1, 8)
        ax.set_aspect("equal")
        ax.set_title(title, fontweight="bold", color="green" if correct else "red")
        ax.set_xlabel("Y (boom width) →")
        ax.set_ylabel("Z (height) →")
        ax.axhline(0, color="#d32f2f", lw=4, label="boom bottom")

        # Fork tabs (Y- and Y+)
        for yc, label in [(-3, "fork"), (3, "fork")]:
            ax.add_patch(Rectangle((yc - 1.25, -5), 2.5, 5, facecolor="#888", edgecolor="black"))
        # Post ear between forks
        ax.add_patch(Rectangle((-1.5, -5), 3, 5, facecolor="#424242", edgecolor="black", alpha=0.7))
        ax.text(0, -2.5, "post\near", ha="center", va="center", color="white", fontsize=8)

        if correct:
            # Pin along Y — horizontal arrow through all three
            ax.annotate("", xy=(4.5, -2.5), xytext=(-4.5, -2.5),
                        arrowprops=dict(arrowstyle="<->", color="#ffc107", lw=3))
            ax.text(0, -1, "filament pin\n(axis Y)", ha="center", color="#f57f17", fontweight="bold")
        else:
            # Pin along Z — vertical arrows in each part (don't meet)
            for yc in (-3, 0, 3):
                ax.annotate("", xy=(yc, 0.5), xytext=(yc, -4.5),
                            arrowprops=dict(arrowstyle="<->", color="#ffc107", lw=2))
            ax.text(0, 1.5, "holes drill\nalong Z ✗", ha="center", color="red", fontweight="bold")

        ax.grid(True, alpha=0.3)

    _save(fig, "hinge_axis_problem.png")


def diagram_assembly_side():
    """Side view (XZ): post vertical between boom and bar — shows Z vs hinge height."""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_title("Side view (XZ) — closed gate: where hinges should meet", fontweight="bold")

    boom_z = 65
    post_len = p.SKIRT_POST_LENGTH_MM
    fork_h = p.SKIRT_HINGE_BOSS_HEIGHT_MM
    bar_h = p.SKIRT_LOWER_RAIL_HEIGHT_MM

    # Boom
    ax.add_patch(Rectangle((10, boom_z), 80, p.BOOM_HEIGHT_MM, facecolor="#d32f2f", edgecolor="black"))
    ax.text(50, boom_z + 1.5, "boom", ha="center", fontsize=9)

    # Forks down from boom (current: holes on bottom face = Z axis)
    for x in (25, 45, 65):
        ax.add_patch(Rectangle((x - 3, boom_z - fork_h), 6, fork_h, facecolor="#888", edgecolor="black"))
        ax.plot([x, x], [boom_z - fork_h, boom_z - fork_h + 2], "y-", lw=2)  # wrong hole dir (Z)

    # Post
    post_top = boom_z - fork_h
    post_bot = post_top - post_len
    ax.plot([45, 45], [post_bot, post_top], color="#424242", lw=6, solid_capstyle="round")
    # Ears (wrong: holes on top/bottom face of ear = Z)
    ax.add_patch(Rectangle((42, post_top), 6, 5, facecolor="#616161", edgecolor="black"))
    ax.add_patch(Rectangle((42, post_bot - 5), 6, 5, facecolor="#616161", edgecolor="black"))

    # Retaining bar + forks up
    bar_z = post_bot - 5
    ax.add_patch(Rectangle((20, bar_z), 50, bar_h, facecolor="#757575", edgecolor="black"))
    for x in (25, 45, 65):
        ax.add_patch(Rectangle((x - 3, bar_z + bar_h), 6, fork_h, facecolor="#888", edgecolor="black"))

    # Where pin SHOULD be (one Y-axis line at hinge height)
    ax.axhline(post_top + 2.5, color="#4caf50", ls="--", lw=2, label="top hinge line (pin center)")
    ax.axhline(post_bot, color="#4caf50", ls="--", lw=2, label="bottom hinge line")

    ax.annotate("post top ear hole drills ↕ Z\nbut pin must go ↔ Y (into page)",
                xy=(52, post_top + 2), fontsize=9, color="red")

    ax.set_xlim(15, 75)
    ax.set_ylim(bar_z - 5, boom_z + 10)
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Z (mm)")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)
    _save(fig, "hinge_side_view_problem.png")


def diagram_front_view_correct():
    """Front view (looking along Y): how clevis should look."""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title("Front view (look along Y) — correct clevis alignment", fontweight="bold")

    # Fork | post ear | fork in XZ isn't right for front view...
    # Front view is X horizontal, Z vertical — we see forks on Y sides as depth
    # Better: cross-section in YZ plane at hinge X station

    ax.set_xlabel("Y (mm)")
    ax.set_ylabel("Z (mm)")

    y_neg, y_pos = -3.5, 3.5
    z0, zh = -5, 0

    ax.add_patch(Rectangle((y_neg - 1.25, z0), 2.5, zh - z0, facecolor="#b71c1c", label="boom fork"))
    ax.add_patch(Rectangle((y_pos - 1.25, z0), 2.5, zh - z0, facecolor="#b71c1c"))
    ax.add_patch(Rectangle((-1.5, z0), 3, zh - z0, facecolor="#424242", label="post ear"))

    # Correct pin: circle in YZ plane = dot at center, arrow along Y
    ax.plot([-4, 4], [-2.5, -2.5], color="#ffc107", lw=4, label="pin axis (Y)")
    ax.plot(0, -2.5, "o", color="#ffc107", markersize=12)

    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 2)
    ax.set_aspect("equal")
    ax.legend()
    ax.grid(True, alpha=0.3)
    _save(fig, "hinge_front_view_correct.png")


def main():
    print("Generating hinge diagnostic diagrams...")
    diagram_expected_vs_actual()
    diagram_assembly_side()
    diagram_front_view_correct()
    print(f"\nOpen folder: {OUT}")
    print("\nSummary of bugs in generate_gate.py:")
    print("  1. Fork holes use faces('<Z') or faces('>Z') -> drill along Z")
    print("  2. Post ear holes use faces('<Z')/'(>Z') -> drill along Z")
    print("  3. Pin must use faces('|Y') or faces('>Y') on all three parts")
    print("  4. Fork tabs + post ear must share one Y-axis line at hinge center")


if __name__ == "__main__":
    main()
