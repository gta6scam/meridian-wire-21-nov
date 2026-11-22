#!/usr/bin/env python3
# Hand-in entry point for The Meridian Wire (NI21 round 5, @yutulboy).
#
# The artwork is finished at build time and committed next to this file
# as entry.png, so at grading time there is nothing left to render: this
# program only places a copy of that PNG where the runner expects it.
# The destination folder comes from the MAKEFUN_OUTPUT_DIR environment
# variable, with /output as the fallback when it is unset or empty.

import os
import shutil
import sys

FALLBACK_DIR = "/output"
ARTWORK_NAME = "entry.png"


def artwork_path():
    # Anchor on this file's own folder rather than the caller's working
    # directory, so the copy succeeds wherever the runner invokes us from.
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, ARTWORK_NAME)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_DIR
    os.makedirs(out_dir, exist_ok=True)
    placed = os.path.join(out_dir, ARTWORK_NAME)
    shutil.copyfile(artwork_path(), placed)
    print("entry.png -> %s (%d bytes)" % (placed, os.path.getsize(placed)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
