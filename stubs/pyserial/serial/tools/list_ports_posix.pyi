"""The ``comports`` function is expected to return an iterable that yields tuples
of 3 strings: port name, human readable description and a hardware ID.

As currently no method is known to get the second two strings easily, they are
currently just identical to the port name.
"""

import sys

from serial.tools.list_ports_common import ListPortInfo

if sys.platform != "win32":
    if sys.platform == "linux":
        from serial.tools.list_ports_linux import comports as comports
    elif sys.platform == "darwin":
        from serial.tools.list_ports_osx import comports as comports
    else:
        def comports(include_links: bool = ...) -> list[ListPortInfo]: ...
