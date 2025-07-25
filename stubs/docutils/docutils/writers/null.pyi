"""
A do-nothing Writer.

`self.output` will change from ``None`` to the empty string
in Docutils 0.22.
"""

from typing import ClassVar

from docutils import writers

class Writer(writers.UnfilteredWriter[str]):
    supported: ClassVar[tuple[str, ...]]
    config_section: ClassVar[str]
    config_section_dependencies: ClassVar[tuple[str]]
    def translate(self) -> None: ...
