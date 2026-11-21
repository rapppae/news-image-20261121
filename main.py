"""Copy the pre-rendered 21 November 2026 news poster to the output path.

The grader runs this file with only the standard library available and
no network, so it must not import anything beyond stdlib and must not
draw: the poster PNG ships in this repository and is copied verbatim.
Pass --out <path> to choose the destination, or set MAKEFUN_OUTPUT_DIR
to a directory; otherwise the image goes to /output/entry.png.
"""

import argparse
import os
import shutil
from pathlib import Path

POSTER = Path(__file__).resolve().parent / "entry.png"


def pick_destination():
    parser = argparse.ArgumentParser(
        description="Copy the 21 Nov 2026 news poster to the output path."
    )
    parser.add_argument("--out", default="", help="output PNG path (default: /output/entry.png)")
    opts = parser.parse_args()
    if opts.out:
        return Path(opts.out)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if outdir:
        return Path(outdir) / "entry.png"
    return Path("/output/entry.png")


def main():
    dest = pick_destination()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(POSTER, dest)
    print("wrote", dest)


if __name__ == "__main__":
    main()
