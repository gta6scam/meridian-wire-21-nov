#!/usr/bin/env python3
"""Hand-in program: copy entry.png into the make.fun output directory."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))
    print("entry.png ->", os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
