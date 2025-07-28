from collections.abc import Collection
from typing import Any

def numsplit(text: str) -> list[str | int]:
    """Convert string into a list of texts and numbers in order to support a
    natural sorting.
    """

class ListPortInfo:
    """Info collection base class for serial ports"""

    device: str
    name: str
    description: str
    hwid: str
    # USB specific data: the vid and pid attributes below are specific to USB devices only and
    # should be marked as Optional. Since the majority of the serial devices nowadays are USB
    # devices, typing them as Optional will be unnecessarily annoying. We type them with as
    # `int | Any` so that obvious typing errors like ListPortInfo.pid + "str" are flagged.
    # As desired, this will cause a false negative if the value is ever None, but may also cause
    # other false negatives from the Any proliferating. The other USB attributes are correctly
    # typed as Optional because they may be `None` even for USB devices
    # Original discussion at https://github.com/python/typeshed/pull/9347#issuecomment-1358245865.
    vid: int | Any
    pid: int | Any
    serial_number: str | None
    location: str | None
    manufacturer: str | None
    product: str | None
    interface: str | None
    def __init__(self, device: str, skip_link_detection: bool = False) -> None: ...
    def usb_description(self) -> str:
        """return a short string to name the port based on USB info"""

    def usb_info(self) -> str:
        """return a string with USB related information about device"""

    def apply_usb_info(self) -> None:
        """update description and hwid from USB data"""

    def __lt__(self, other: ListPortInfo) -> bool: ...
    def __getitem__(self, index: int) -> str:
        """Item access: backwards compatible -> (port, desc, hwid)"""

def list_links(devices: Collection[str]) -> list[str]:
    """search all /dev devices and look for symlinks to known ports already
    listed in devices.
    """
