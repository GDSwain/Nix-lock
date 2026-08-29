#!/usr/bin/env python3

from pathlib import Path
import os
import subprocess
import sys
import tempfile


def get_state_dir() -> Path:
    xdg_state_home = os.environ.get("XDG_STATE_HOME")

    if xdg_state_home:
        return Path(xdg_state_home).expanduser() / "nix-lock"

    return Path.home() / ".local" / "state" / "nix-lock"


STATE_DIR = get_state_dir()
CANDIDATE_ROOT = STATE_DIR / "candidate"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=True,
        text=True,
        capture_output=True,
    )


def is_store_path(path: Path) -> bool:
    try:
        path.relative_to("/nix/store")
    except ValueError:
        return False

    return True


def read_candidate() -> Path | None:
    if not CANDIDATE_ROOT.is_symlink():
        return None

    try:
        candidate = CANDIDATE_ROOT.resolve(strict=True)
    except FileNotFoundError:
        raise RuntimeError(
            f"Candidate root is broken: {CANDIDATE_ROOT}"
        ) from None

    if not is_store_path(candidate):
        raise RuntimeError(
            f"Candidate root points outside the Nix store: {candidate}"
        )

    return candidate


def add_gc_root(root: Path, closure: Path) -> None:
    if root.exists() or root.is_symlink():
        raise RuntimeError(f"GC root already exists: {root}")

    run(
        [
            "nix-store",
            "--add-root",
            str(root),
            "--indirect",
            "-r",
            str(closure),
        ]
    )

    if not root.is_symlink():
        raise RuntimeError(f"Nix did not create the GC root: {root}")

    rooted_closure = root.resolve(strict=True)

    if rooted_closure != closure:
        raise RuntimeError(
            "GC root points to an unexpected closure: "
            f"{rooted_closure}"
        )


def remove_root(root: Path) -> None:
    if root.exists() or root.is_symlink():
        root.unlink()


def capture() -> None:
    old_candidate = read_candidate()

    subprocess.run(
        ["nixos-rebuild", "build"],
        check=True,
    )

    result = Path("result")

    if not result.is_symlink():
        raise RuntimeError(
            "nixos-rebuild completed, but no result symlink was found"
        )

    closure_path = result.resolve(strict=True)

    if not is_store_path(closure_path):
        raise RuntimeError(f"Unexpected closure path: {closure_path}")

    expected_switch_program = (
        closure_path / "bin" / "switch-to-configuration"
    )

    if not expected_switch_program.is_file():
        raise RuntimeError(
            "Built path does not appear to be a NixOS system closure: "
            f"{closure_path}"
        )

    STATE_DIR.mkdir(parents=True, exist_ok=True)

    temporary_root = Path(
        tempfile.mktemp(
            dir=STATE_DIR,
            prefix=".candidate-new.",
        )
    )

    try:
        # Protect the new closure before touching the old candidate.
        add_gc_root(temporary_root, closure_path)

        # Remove only the root owned by Nix-Lock.
        remove_root(CANDIDATE_ROOT)

        try:
            # Install the stable, human-readable candidate root.
            add_gc_root(CANDIDATE_ROOT, closure_path)
        except Exception:
            # Restore the previous candidate if replacement fails.
            if old_candidate is not None:
                add_gc_root(CANDIDATE_ROOT, old_candidate)

            raise

    finally:
        remove_root(temporary_root)

    # The Nix-Lock root now protects the closure. The build result link is
    # no longer needed and should not provide a second, hidden reference.
    result.unlink(missing_ok=True)

    print()
    print("Candidate captured and locked")
    print(f"Closure: {closure_path}")
    print(f"GC root: {CANDIDATE_ROOT}")

    if old_candidate is not None:
        print(f"Previous candidate released: {old_candidate}")


def status() -> None:
    candidate = read_candidate()

    if candidate is None:
        print("No locked candidate exists.")
        return

    switch_program = candidate / "bin" / "switch-to-configuration"

    print("Locked candidate")
    print(f"Closure: {candidate}")
    print(f"GC root: {CANDIDATE_ROOT}")
    print("Store path: present")
    print("GC protection: present")

    if switch_program.is_file():
        print("NixOS system closure: valid")
    else:
        print("NixOS system closure: INVALID")


def deploy() -> None:
    candidate = read_candidate()

    if candidate is None:
        raise RuntimeError("No locked candidate exists.")

    switch_program = candidate / "bin" / "switch-to-configuration"

    if not switch_program.is_file():
        raise RuntimeError(
            "Locked candidate is not a valid NixOS system closure: "
            f"{candidate}"
        )

    current_system = Path("/run/current-system").resolve(strict=True)

    print("Deploying locked candidate")
    print(f"Current:   {current_system}")
    print(f"Candidate: {candidate}")
    print()

    if current_system == candidate:
        print("Candidate is already active.")
        return

    subprocess.run(
        ["sudo", str(switch_program), "switch"],
        check=True,
    )

    active_system = Path("/run/current-system").resolve(strict=True)

    if active_system != candidate:
        raise RuntimeError(
            "Deployment completed, but the active system does not "
            f"match the candidate: {active_system}"
        )

    print()
    print("Candidate deployed")
    print(f"Active system: {active_system}")


def main() -> None:
    valid_commands = {"capture", "status", "deploy"}

    if len(sys.argv) != 2 or sys.argv[1] not in valid_commands:
        print(
            "Usage: python3 nix_lock.py {capture|status|deploy}",
            file=sys.stderr,
        )
        raise SystemExit(2)

    try:
        command = sys.argv[1]

        if command == "capture":
            capture()
        elif command == "status":
            status()
        else:
            deploy()

    except subprocess.CalledProcessError as error:
        stderr = error.stderr.strip() if error.stderr else ""

        print(
            f"Command failed with exit code {error.returncode}.",
            file=sys.stderr,
        )

        if stderr:
            print(stderr, file=sys.stderr)

        raise SystemExit(error.returncode)

    except Exception as error:
        print(f"Nix-Lock failed: {error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
