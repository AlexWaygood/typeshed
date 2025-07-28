import ctypes
import sys

from serial.tools.list_ports_common import ListPortInfo

if sys.platform == "darwin":
    iokit: ctypes.CDLL
    cf: ctypes.CDLL
    kIOMasterPortDefault: int
    kCFAllocatorDefault: ctypes.c_void_p
    kCFStringEncodingMacRoman: int
    kCFStringEncodingUTF8: int
    kUSBVendorString: str
    kUSBSerialNumberString: str
    io_name_size: int
    KERN_SUCCESS: int
    kern_return_t = ctypes.c_int
    kCFNumberSInt8Type: int
    kCFNumberSInt16Type: int
    kCFNumberSInt32Type: int
    kCFNumberSInt64Type: int

    def get_string_property(device_type: ctypes._CData, property: str) -> str | None:
        """
        Search the given device for the specified string property

        @param device_type Type of Device
        @param property String to search for
        @return Python string containing the value, or None if not found.
        """

    def get_int_property(device_type: ctypes._CData, property: str, cf_number_type: int) -> int | None:
        """
        Search the given device for the specified string property

        @param device_type Device to search
        @param property String to search for
        @param cf_number_type CFType number

        @return Python string containing the value, or None if not found.
        """

    def IORegistryEntryGetName(device: ctypes._CData) -> str | None: ...
    def IOObjectGetClass(device: ctypes._CData) -> bytes: ...
    def GetParentDeviceByType(device: ctypes._CData, parent_type: str) -> ctypes._CData | None:
        """Find the first parent of a device that implements the parent_type
        @param IOService Service to inspect
        @return Pointer to the parent type, or None if it was not found.
        """

    def GetIOServicesByType(service_type: str) -> list[ctypes._CData]:
        """
        returns iterator over specified service_type
        """

    def location_to_string(locationID: int) -> str:
        """
        helper to calculate port and bus number from locationID
        """

    # `SuitableSerialInterface` has required attributes `id: int` and `name: str` but they are not defined on the class
    class SuitableSerialInterface: ...

    def scan_interfaces() -> list[SuitableSerialInterface]:
        """
        helper function to scan USB interfaces
        returns a list of SuitableSerialInterface objects with name and id attributes
        """

    def search_for_locationID_in_interfaces(serial_interfaces: list[SuitableSerialInterface], locationID: int) -> str | None: ...
    def comports(include_links: bool = ...) -> list[ListPortInfo]: ...
