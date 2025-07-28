from serial.tools.list_ports_common import ListPortInfo

class SysFS(ListPortInfo):
    """Wrapper for easy sysfs access and device info"""

    usb_device_path: str | None
    device_path: str | None
    subsystem: str | None
    usb_interface_path: str | None
    def __init__(self, device: str) -> None: ...
    def read_line(self, *args: str) -> str | None:
        """Helper function to read a single line from a file.
        One or more parameters are allowed, they are joined with os.path.join.
        Returns None on errors..
        """

def comports(include_links: bool = False) -> list[SysFS]: ...
