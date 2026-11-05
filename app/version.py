"""Single source for the version shown at the top of the API docs."""

import tomllib
from pathlib import Path

_PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"


def code_version() -> str:
    with _PYPROJECT.open("rb") as f:
        return tomllib.load(f)["project"]["version"]


VERSION = code_version()

OPTIONS_TAG = "options"
TEAMS_TAG = "teams"
PLAYERS_TAG = "players"
