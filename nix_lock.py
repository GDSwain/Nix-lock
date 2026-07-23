#!/usr/bin/env python3

from pathlib import Path
import os
import subprocess
import sys
import tempfile


STATE_DIR = Path(".nix-lock")
CANDIDATE_FILE = STATE_DIR / "candidate"


def capture() -> None:
    subprocess.run(
        ["nixos-rebuild", "build"],
        check=True,
    )

    result = Path("result")

    if not result.is_symlink():
        raise RuntimeError("nixos-rebuild completed, but no result symlink was found")

    closure_path = result.resolve(strict=True)

    if not str(closure_path).startswith("/nix/store/"):
        raise RuntimeError(f"Unexpected closure path: {closure_path}")

    STATE_DIR.mkdir(exist_ok=True)

    fd, temporary_name = tempfile.mkstemp(
        dir=STATE_DIR,
        prefix=".candidate.",
        text=True,
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as temporary_file:
            temporary_file.write(f"{closure_path}\n")

        os.replace(temporary_name, CANDIDATE_FILE)
    except Exception:
        Path(temporary_name).unlink(missing_ok=True)
        raise

    print()
    print("Candidate captured")
    print(f"Closure: {closure_path}")


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] != "capture":
        print("Usage: python3 nix_lock.py capture", file=sys.stderr)
        raise SystemExit(2)

    try:
        capture()
    except subprocess.CalledProcessError as error:
        print(
            f"Build failed with exit code {error.returncode}.",
            file=sys.stderr,
        )
        raise SystemExit(error.returncode)
    except Exception as error:
        print(f"Capture failed: {error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
