#!/usr/bin/env python3
import tarfile
from pathlib import Path

to_include = [
    "apps",
    "common",
    "data",
    "static",
    "templates",
    "LICENSE",
    "run.py",
]

def exclude_pycache(tarinfo):
    parts = Path(tarinfo.name).parts
    if "__pycache__" in parts:
        return None
    return tarinfo


def create_archive():
    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / 'data' / 'source_leak.tar'

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tarfile.open(output_path, "w") as tar:
        for name in to_include:
            src = project_root / name
            if src.exists():
                tar.add(src, arcname=name, filter=exclude_pycache)
            else:
                print(f"[!] Skipping missing: {src}")

    print(f"Archive created at: {output_path}")

if __name__ == "__main__":
    create_archive()
