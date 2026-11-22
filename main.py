#!/usr/bin/env python3
"""Deliver the committed entry.png into the runner's output folder."""

import os
import shutil
from pathlib import Path


def deliver() -> Path:
    source = Path(__file__).resolve().parent / "entry.png"
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    target_dir.mkdir(parents=True, exist_ok=True)
    destination = target_dir / source.name
    shutil.copyfile(source, destination)
    return destination


if __name__ == "__main__":
    placed = deliver()
    print(f"delivered: {placed} ({placed.stat().st_size} bytes)")
