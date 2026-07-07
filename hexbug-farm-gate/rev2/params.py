"""
Rev 2 — boom arm + retaining bar sized for f_skirt_post.stl.

Reference post (Fusion export): post axis Y, pin axis X.
Measured from cadquery/output/f_skirt_post.stl.
"""

from pathlib import Path

REV2_ROOT = Path(__file__).resolve().parent
REFERENCE_POST_STL = REV2_ROOT.parent / "cadquery" / "output" / "f_skirt_post.stl"

# --- Measured skirt post (f_skirt_post.stl) ---
POST_TOTAL_LENGTH_MM = 46.0
POST_HINGE_CENTER_FROM_END_MM = 2.7  # hinge centre to nearest post tip
POST_HINGE_CENTER_SPACING_MM = 40.6  # bottom pin to top pin along post
POST_SHAFT_DIAMETER_MM = 5.6  # mid-shaft OD (print mesh)
POST_HINGE_BOSS_OD_MM = 7.0
POST_HINGE_BOSS_THICKNESS_MM = 5.0  # lug extent along pin axis (STL X)
POST_HINGE_HOLE_DIAMETER_MM = 2.15  # 1.75 mm filament + 0.4 mm clearance

# --- Skirt layout (unchanged from gate v1) ---
SKIRT_BAR_COUNT = 10
SKIRT_HINGE_SPAN_MM = 80.0

# --- Boom ---
BOOM_LENGTH_MM = 110.0
BOOM_WIDTH_MM = 8.0
BOOM_HEIGHT_MM = 3.0
# Lug hangs below boom underside; pin centre offset from boom bottom
BOOM_HINGE_LUG_DROP_MM = POST_HINGE_BOSS_OD_MM / 2  # pin at lug centre

# --- Retaining bar (hangs from post bottom hinges) ---
RETAINING_BAR_HEIGHT_MM = 3.0
RETAINING_BAR_WIDTH_MM = BOOM_WIDTH_MM

# --- Integrated SG90 horn socket (at boom root, X = 0) ---
HORN_SOCKET_DIAMETER_MM = 20.0
HORN_SOCKET_THICKNESS_MM = 3.0
HORN_HOLE_DIAMETER_MM = 2.0
HORN_HOLE_SPAN_MM = 10.0  # cross pattern, centre-to-centre
HORN_CENTER_BOSS_DIAMETER_MM = 4.8  # spline / boss clearance
HORN_SCREW_DEPTH_MM = 2.5

# Print
CLEARANCE_MM = 0.3
