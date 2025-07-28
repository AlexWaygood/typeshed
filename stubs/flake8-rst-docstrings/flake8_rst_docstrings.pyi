"""Check Python docstrings validate as reStructuredText (RST).

This is a plugin for the tool flake8 tool for checking Python
source code.
"""

import ast
from argparse import Namespace
from collections.abc import Container, Generator
from typing import Any

rst_prefix: str
rst_fail_load: int
rst_fail_lint: int
code_mapping_info: dict[str, int]
code_mapping_warning: dict[str, int]
code_mapping_error: dict[str, int]
code_mapping_severe: dict[str, int]
code_mappings_by_level: dict[int, dict[str, int]]

def code_mapping(
    level: int,
    msg: str,
    extra_directives: Container[str],
    extra_roles: Container[str],
    extra_substitutions: Container[str],
    default: int = ...,
) -> int:
    """Return an error code between 0 and 99."""

class reStructuredTextChecker:
    """Checker of Python docstrings as reStructuredText."""

    name: str
    version: str
    tree: ast.AST
    filename: str
    def __init__(self, tree: ast.AST, filename: str = ...) -> None:
        """Initialise."""

    @classmethod
    def add_options(cls, parser: Any) -> None:
        """Add RST directives, roles and substitutions options."""

    @classmethod
    def parse_options(cls, options: Namespace) -> None:
        """Adding black-config option."""

    def run(self) -> Generator[tuple[int, int, str, type[reStructuredTextChecker]], None, None]:
        """Use docutils to check docstrings are valid RST."""
