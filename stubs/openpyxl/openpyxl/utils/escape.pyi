"""
OOXML has non-standard escaping for characters < \x19
"""

def escape(value: str) -> str:
    """
    Convert ASCII < 31 to OOXML: \\n == _x + hex(ord(\\n)) + _
    """

def unescape(value: str) -> str:
    """
    Convert escaped strings to ASCIII: _x000a_ == \\n
    """
