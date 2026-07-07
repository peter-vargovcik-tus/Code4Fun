"""
Shared dimensions for the hexbug farm gate (hinged skirt, 9g servo).
Edit here, then regenerate STEP files or re-run the Fusion script.
"""

# Gate geometry
GATE_OPENING_MM = 100.0
BOOM_LENGTH_MM = 110.0
BOOM_WIDTH_MM = 8.0
BOOM_HEIGHT_MM = 3.0

# Skirt — individual posts hinged to boom (top) and retaining bar (bottom).
# The retaining bar HANGS — it is not fixed to the base; posts support it.
SKIRT_DROP_MM = 30.0
SKIRT_BAR_COUNT = 10
SKIRT_BAR_DIAMETER_MM = 2.5
SKIRT_RETAINING_BAR_HEIGHT_MM = 3.0  # lower hanging bar (alias in code: SKIRT_LOWER_RAIL_*)
SKIRT_LOWER_RAIL_HEIGHT_MM = SKIRT_RETAINING_BAR_HEIGHT_MM
SKIRT_HINGE_SPAN_MM = 80.0
# Round donut hinge housings (rotate freely — no square blocks)
SKIRT_HINGE_BOSS_OD_MM = 7.0
SKIRT_HINGE_BOSS_HEIGHT_MM = 5.0  # extent along Z at each hinge
SKIRT_HINGE_BOSS_THICKNESS_MM = 3.0  # extent along Y (pin axis)
# Centre-to-centre between top and bottom hinge pins on one post (when vertical)
SKIRT_POST_LENGTH_MM = 26.0
SKIRT_LOWER_RAIL_OFFSET_MM = 15.0

# Boom motion — rotates upward (0° closed horizontal → 90° open vertical)
BOOM_CLOSED_ANGLE_DEG = 0.0
BOOM_OPEN_ANGLE_DEG = 90.0
BOOM_ROTATION_AXIS = "Y"  # servo pivots boom in XZ plane (lifts upward, no sweep push)

# Skirt hinge pins — cut from printer filament (not separate parts)
FILAMENT_DIAMETER_MM = 1.75  # standard 1.75 mm filament
SKIRT_HINGE_HOLE_OVERSIZE_MM = 0.4  # hole = filament + 0.4 mm for smooth rotation
SKIRT_HINGE_HOLE_DIAMETER_MM = FILAMENT_DIAMETER_MM + SKIRT_HINGE_HOLE_OVERSIZE_MM

# Clevis fork geometry on boom / retaining bar (round lugs mate with post donuts)
SKIRT_HINGE_FORK_TAB_WIDTH_MM = 2.5
SKIRT_HINGE_FORK_GAP_MM = 0.5

# Legacy pin exports (optional metal rod) — skirt uses filament instead
HINGE_PIN_DIAMETER_MM = FILAMENT_DIAMETER_MM
HINGE_PIN_LENGTH_MM = 14.0
HINGE_PIN_CLEARANCE_MM = 0.0

# SG90-class 9g micro servo
SERVO_BODY_LENGTH_MM = 23.0
SERVO_BODY_WIDTH_MM = 12.7
SERVO_BODY_HEIGHT_MM = 22.8  # body only (excluding horn)
SERVO_FLANGE_WIDTH_MM = 27.0
SERVO_FLANGE_THICKNESS_MM = 2.5
SERVO_HORN_AXIS_HEIGHT_MM = 27.0  # center of horn above mounting surface

# Gate post
POST_WIDTH_MM = 22.0
POST_DEPTH_MM = 24.0
POST_HEIGHT_MM = 75.0
POST_WALL_MM = 2.0

# Desk base — post on left, rest pillar on right (boom tip rests on pillar when closed)
BASE_LENGTH_MM = 145.0
BASE_WIDTH_MM = 55.0
BASE_THICKNESS_MM = 5.0
POST_CENTER_X_MM = 14.0  # post centre measured from left edge of base plate
POST_SOCKET_DEPTH_MM = 8.0
PILLAR_WIDTH_MM = 18.0
PILLAR_DEPTH_MM = 18.0
PILLAR_CENTER_X_MM = POST_CENTER_X_MM + BOOM_LENGTH_MM - 4.0
BOOM_AXIS_HEIGHT_MM = POST_HEIGHT_MM - 10.0  # boom underside above post footing (base top)
PILLAR_REST_NOTCH_DEPTH_MM = 1.5  # shallow cradle for boom tip

# Horn adapter (standard SG90 single-arm horn)
HORN_ADAPTER_DIAMETER_MM = 20.0
HORN_ADAPTER_THICKNESS_MM = 3.0
HORN_HOLE_DIAMETER_MM = 2.0
HORN_HOLE_SPAN_MM = 10.0  # center-to-center of horn screw holes
BOOM_MOUNT_TAB_WIDTH_MM = 8.0
BOOM_MOUNT_TAB_LENGTH_MM = 15.0

# Print tolerances
CLEARANCE_MM = 0.3
FIT_CLEARANCE_MM = 0.15
