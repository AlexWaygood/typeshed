"""Implementation of pydocstyle integration with Flake8.

pydocstyle docstrings convention needs error code and class parser for be
included as module into flake8
"""

import argparse
import ast
from collections.abc import Generator, Iterable
from typing import Any, ClassVar, Final, Literal
from typing_extensions import Self

from flake8.options.manager import OptionManager

__version__: Final[str]
__all__ = ("pep257Checker",)

class pep257Checker:
    """Flake8 needs a class to check python file."""

    name: ClassVar[str]
    version: ClassVar[str]
    tree: ast.AST
    filename: str
    checker: Any  # actual type: pep257.ConventionChecker
    source: str
    def __init__(self, tree: ast.AST, filename: str, lines: Iterable[str]) -> None:
        """Initialize the checker."""

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        """Add plugin configuration option to flake8."""

    @classmethod
    def parse_options(cls, options: argparse.Namespace) -> None:
        """Parse the configuration options given to flake8."""

    def run(self) -> Generator[tuple[int, Literal[0], str, type[Self]]]:
        """Use directly check() api from pydocstyle."""
