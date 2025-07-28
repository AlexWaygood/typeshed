"""Plugin built-in to Flake8 to treat pyflakes as a plugin."""

from argparse import Namespace
from ast import AST
from collections.abc import Generator
from logging import Logger
from typing import Any

from pyflakes.checker import Checker

from ..options.manager import OptionManager

LOG: Logger
FLAKE8_PYFLAKES_CODES: dict[str, str]

class FlakesChecker(Checker):
    """Subclass the Pyflakes checker to conform with the flake8 API."""

    with_doctest: bool
    def __init__(self, tree: AST, filename: str) -> None:
        """Initialize the PyFlakes plugin with an AST tree and filename."""

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        """Register options for PyFlakes on the Flake8 OptionManager."""

    @classmethod
    def parse_options(cls, options: Namespace) -> None:
        """Parse option values from Flake8's OptionManager."""

    def run(self) -> Generator[tuple[int, int, str, type[Any]], None, None]:
        """Run the plugin."""
