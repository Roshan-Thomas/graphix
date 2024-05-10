"""Detect updates to the pyproject.toml file."""

# TODO: Move this file to the proper location.

import tomllib
from pathlib import Path
from typing import TypeGuard


def validate(arr: object) -> TypeGuard[list[str]]:
    """Validate the loaded attributes."""
    if not isinstance(arr, list):
        return False
    if any(not isinstance(x, str) for x in arr):
        return False
    return True


PROJECT_ROOT = Path(__file__).parents[1]
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
REQUIREMENTS_PATH = PROJECT_ROOT / "requirements.txt"
REQUIREMENTS_DEV_PATH = PROJECT_ROOT / "requirements-dev.txt"

with (
    PYPROJECT_PATH.open("rb") as f,
    REQUIREMENTS_PATH.open("w") as o,
    REQUIREMENTS_DEV_PATH.open("w") as odev,
):
    pp = tomllib.load(f)
    try:
        deps = pp["project"]["dependencies"]
        devdeps = pp["project"]["optional-dependencies"]["dev"]
        assert validate(deps)
        assert validate(devdeps)
    except KeyError as e:
        msg = "Failed parse pyproject.toml."
        raise ValueError(msg) from e
    except AssertionError as e:
        msg = "Invalid data."
        raise ValueError(msg) from e

    for entry in deps:
        print(entry, file=o)

    for entry in devdeps:
        print(entry, file=odev)
