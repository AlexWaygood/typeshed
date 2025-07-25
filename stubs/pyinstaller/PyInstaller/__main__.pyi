"""
Main command-line interface to PyInstaller.
"""

from _typeshed import SupportsKeysAndGetItem
from collections.abc import Iterable
from typing_extensions import TypeAlias

# Used to update PyInstaller.config.CONF
_PyIConfig: TypeAlias = (
    SupportsKeysAndGetItem[str, bool | str | list[str] | None] | Iterable[tuple[str, bool | str | list[str] | None]]
)

# https://pyinstaller.org/en/stable/usage.html#running-pyinstaller-from-python-code
def run(pyi_args: Iterable[str] | None = None, pyi_config: _PyIConfig | None = None) -> None:
    """
    pyi_args     allows running PyInstaller programmatically without a subprocess
    pyi_config   allows checking configuration once when running multiple tests
    """

def check_unsafe_privileges() -> None:
    """
    Forbid dangerous usage of PyInstaller with escalated privileges
    """
