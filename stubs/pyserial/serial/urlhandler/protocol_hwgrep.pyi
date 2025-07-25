import serial

class Serial(serial.Serial):
    """Just inherit the native Serial port implementation and patch the port property."""

    def from_url(self, url: str) -> str:
        """extract host and port from an URL string"""
