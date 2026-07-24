"""Build Ohana-Agent distribution artifacts."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def remove_directory(path: Path) -> None:
    """Remove a directory if it exists."""
    if path.exists():
        shutil.rmtree(path)


def main() -> int:
    print("Cleaning previous artifacts...")

    remove_directory(ROOT / "build")
    remove_directory(ROOT / "dist")

    for egg_info in ROOT.glob("*.egg-info"):
        shutil.rmtree(egg_info)

    print("Building wheel and source distribution...")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "build",
        ],
        cwd=ROOT,
        check=True,
    )

    print()
    print("Build completed successfully.")
    print()

    for artifact in sorted((ROOT / "dist").iterdir()):
        print(f" - {artifact.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
