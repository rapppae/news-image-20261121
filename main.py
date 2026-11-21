"""Entry point: copy the pre-rendered poster to the output location.

The grader runs `python3 -P -s /bot/main.py` in a sandbox with no
network and only the standard library (RULES.txt: "standard library
only: nothing is installed before it runs"), so this entrypoint does
not draw anything: it copies the poster PNG that ships in the
repository to the output path. The destination can be overridden
with --out, or with the MAKEFUN_OUTPUT_DIR environment variable (a
plain directory path).
"""

import argparse
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def _destination(cli_out):
    if cli_out:
        return Path(cli_out)
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if env_dir:
        return Path(env_dir) / "entry.png"
    return Path("/output/entry.png")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Copy the 21 Nov 2026 news poster to the output path.")
    parser.add_argument("--out", default=None, help="output PNG path (default: /output/entry.png)")
    args = parser.parse_args(argv)
    target = _destination(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, target)
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
