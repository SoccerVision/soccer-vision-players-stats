"""Single source for the version shown in the API and its docs."""

import tomllib
from pathlib import Path

_PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"


def code_version() -> str:
    with _PYPROJECT.open("rb") as f:
        return tomllib.load(f)["project"]["version"]


VERSION = code_version()


def doc_tag(name: str) -> str:
    """Swagger tag labeled with the version of this code."""
    return f"{VERSION} · {name}"


OPTIONS_TAG = doc_tag("options")
TEAMS_TAG = doc_tag("teams")
PLAYERS_TAG = doc_tag("players")
V1_TAG = doc_tag("v1 (legacy)")
