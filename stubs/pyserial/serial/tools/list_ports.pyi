"""This module will provide a function called comports that returns an
iterable (generator or list) that will enumerate available com ports. Note that
on some systems non-existent ports may be listed.

Additionally a grep function is supplied that can be used to search for ports
based on their descriptions or hardware ID.
"""

import re
import sys
from collections.abc import Generator

if sys.platform == "win32":
    from serial.tools.list_ports_windows import comports as comports
else:
    from serial.tools.list_ports_posix import comports as comports

def grep(regexp: str | re.Pattern[str], include_links: bool = False) -> Generator[tuple[str, str, str], None, None]:
    """Search for ports using a regular expression. Port name, description and
    hardware ID are searched. The function returns an iterable that returns the
    same tuples as comport() would do.
    """

def main() -> None: ...
