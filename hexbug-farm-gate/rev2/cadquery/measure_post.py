"""Print key dimensions from f_skirt_post.stl (requires numpy-stl)."""

from __future__ import annotations

import struct
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import params as p  # noqa: E402


def _load_vertices(path: Path) -> np.ndarray:
    try:
        from stl import mesh

        m = mesh.Mesh.from_file(str(path))
        return m.vectors.reshape(-1, 3)
    except ImportError:
        with path.open("rb") as f:
            f.read(80)
            n = struct.unpack("<I", f.read(4))[0]
            pts = []
            for _ in range(n):
                f.read(12)
                pts.append(struct.unpack("<3f", f.read(12)))
                f.read(2)
        return np.array(pts)


def main() -> None:
    path = p.REFERENCE_POST_STL
    if not path.exists():
        print(f"Missing {path}")
        return

    pts = _load_vertices(path)
    ext = pts.max(0) - pts.min(0)
    print(f"File: {path.name}")
    print(f"  bounds min {pts.min(0)}")
    print(f"  bounds max {pts.max(0)}")
    print(f"  extents (Fusion axes) {ext}")
    print(f"  rev2 params: length={p.POST_TOTAL_LENGTH_MM}, hinge spacing={p.POST_HINGE_CENTER_SPACING_MM}")


if __name__ == "__main__":
    main()
