"""Module containing the logic for our debugging logic."""

from typing import Any

from ..plugins.finder import Plugins

def information(version: str, plugins: Plugins) -> dict[str, Any]:
    """Generate the information to be printed for the bug report."""
