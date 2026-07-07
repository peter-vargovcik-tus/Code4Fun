"""Export YZ cross-section image of fixed hinge (pin along Y)."""
from __future__ import annotations
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import cadquery as cq

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_gate import make_hinge_joint_preview

OUT = Path(__file__).resolve().parent / "output" / "diagnostics"
OUT.mkdir(parents=True, exist_ok=True)

# Export updated STEP already; render schematic
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title("FIXED: filament pin along Y (into page)", fontweight="bold", color="green")
ax.set_xlabel("Y (mm)")
ax.set_ylabel("Z (mm)")

y_neg, y_pos = -4.25, 4.25
for yc in (y_neg, y_pos):
    ax.add_patch(Rectangle((yc - 1.25, -5), 2.5, 5, facecolor="#b71c1c", edgecolor="black"))
ax.add_patch(Rectangle((-1.5, -5), 3, 5, facecolor="#424242", edgecolor="black"))
ax.plot([-5, 5], [-2.5, -2.5], color="#ffc107", lw=5)
ax.plot(0, -2.5, "o", color="#ffc107", markersize=14)
ax.text(0, 1, "single pin line\n(all holes align)", ha="center", fontweight="bold")
ax.set_xlim(-7, 7)
ax.set_ylim(-7, 3)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
fig.savefig(OUT / "hinge_axis_fixed.png", dpi=150, bbox_inches="tight")
print(f"saved {OUT / 'hinge_axis_fixed.png'}")
