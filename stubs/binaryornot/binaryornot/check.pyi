"""
binaryornot.check
-----------------

Main code for checking if a file is binary or text.
"""

from _typeshed import StrOrBytesPath

def is_binary(filename: StrOrBytesPath) -> bool:
    """
    :param filename: File to check.
    :returns: True if it's a binary file, otherwise False.
    """
