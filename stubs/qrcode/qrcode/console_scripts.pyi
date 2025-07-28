"""
qr - Convert stdin (or the first argument) to a QR Code.

When stdout is a tty the QR Code is printed to the terminal and when stdout is
a pipe to a file an image is written. The default image format is PNG.
"""

from collections.abc import Iterable, Sequence

from ._types import ErrorCorrect
from .image.base import BaseImage, DrawerAliases as DrawerAliases

default_factories: dict[str, str]
error_correction: dict[str, ErrorCorrect]

def main(args: Sequence[str] | None = None) -> None: ...
def get_factory(module: str) -> type[BaseImage]: ...
def get_drawer_help() -> str: ...
def commas(items: Iterable[str], joiner: str = "or") -> str: ...
