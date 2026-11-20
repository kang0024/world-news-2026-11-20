#!/usr/bin/env python3
"""News poster entry for make.fun news-image-20261120.

Writes the day's world-news poster to $MAKEFUN_OUTPUT_DIR/entry.png.
The image bytes live at ./entry.png in the repo (committed), and this
program copies them so both runs write identical bytes. No network,
standard library only.
"""

import os
import shutil
import sys
from pathlib import Path

REPO_IMAGE = Path(__file__).resolve().parent / "entry.png"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    if not REPO_IMAGE.exists():
        print("entry.png missing in repo", file=sys.stderr)
        return 2
    shutil.copyfile(REPO_IMAGE, dst)
    print(f"wrote {dst} ({dst.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
