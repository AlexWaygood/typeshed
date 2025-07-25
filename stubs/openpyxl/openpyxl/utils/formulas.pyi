"""
List of builtin formulae
"""

from typing import Final

FORMULAE: Final[frozenset[str]]

def validate(formula: str) -> None:
    """
    Utility function for checking whether a formula is syntactically correct
    """
