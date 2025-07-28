"""
Adapt a word-processor-generated styles.odt for odtwriter use:

Drop page size specifications from styles.xml in STYLE_FILE.odt.
See https://docutils.sourceforge.io/docs/user/odt.html#page-size
"""

from _typeshed import StrPath
from typing import IO

NAMESPACES: dict[str, str]

def prepstyle(filename: StrPath | IO[bytes]) -> None: ...
def main() -> None: ...
