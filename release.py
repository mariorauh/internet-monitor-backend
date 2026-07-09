#!/usr/bin/env python3

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def run(command: list[str], cwd: Path) -> None:
    """Execute a command and abort on failure."""

    print(f"> {' '.join(command)}")

    result = subprocess.run(command, cwd=cwd)

    if result.returncode != 0:
        sys.exit(result.returncode)


def update_addon_version(config_file: Path, version: str) -> None:
    """Update the version inside config.yaml."""

    text = config_file.read_text(encoding="utf-8")

    text = re.sub(
        r'^version:\s*".*"$',
        f'version: "{version}"',
        text,
        flags=re.MULTILINE,
    )

    config_file.write_text(text, encoding="utf-8")
    
    
def update_backend_version(config_file: Path, version: str) -> None:
    """Update APP_VERSION inside backend config.py."""

    text = config_file.read_text(encoding="utf-8")

    text = re.sub(
        r'^APP_VERSION\s*=\s*".*"$',
        f'APP_VERSION = "{version}"',
        text,
        flags=re.MULTILINE,
    )

    config_file.write_text(text, encoding="utf-8")


def main() -> None:

    backend_repo = Path(__file__).resolve().parent

    workspace = backend_repo.parent.parent

    addon_repo = (
        workspace
        / "internet-monitor-addon"
        / "internet-monitor-addon"
    )

    config_file = (
        addon_repo
        / "internet_monitor"
        / "config.yaml"
    )
    
    backend_config_file = (
        backend_repo
        / "app"
        / "config.py"
    )

    if not config_file.exists():
        print()
        print("ERROR")
        print(f"Add-on config.yaml not found:")
        print(config_file)
        sys.exit(1)

    if not backend_config_file.exists():
        print()
        print("ERROR")
        print(f"Backend config.py not found:")
        print(backend_config_file)
        sys.exit(1)

    print()
    print("====================================")
    print(" Internet Monitor Release Tool")
    print("====================================")
    print()

    version = input("Version (e.g. 0.2.0): ").strip()

    if not version:
        print("No version entered.")
        sys.exit(1)

    print()
    print(f"Updating version to {version}...")
    
    changes = input("Enter Changes: ").strip()
    
    if not changes:
        print("No changes entered.")
        sys.exit(1)

    update_addon_version(config_file, version)
    update_backend_version(backend_config_file, version)

    print("✓ Add-on config.yaml updated")
    print("✓ Backend config.py updated")
    print()

    answer = input("Continue? (y/n): ").strip().lower()

    if answer != "y":
        print("Cancelled.")
        return

    #
    # Backend
    #

    print()
    print("Publishing backend...")
    print()

    run(["git", "add", "."], backend_repo)
    run(["git", "commit", "-m", f"Changes: {changes}"], backend_repo)
    run(["git", "tag", f"v{version}"], backend_repo)
    run(["git", "push", "origin", "main"], backend_repo)
    run(["git", "push", "origin", f"v{version}"], backend_repo)

    #
    # Add-on
    #

    print()
    print("Publishing add-on...")
    print()

    run(["git", "add", "."], addon_repo)
    run(["git", "commit", "-m", f"Changes: {changes}"], addon_repo)
    run(["git", "push", "origin", "main"], addon_repo)

    print()
    print("====================================")
    print(f" Release {version} completed")
    print("====================================")


if __name__ == "__main__":
    main()