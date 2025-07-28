"""
#################
exceptions module
#################

All custom exceptions are defined in this module.
"""

class StoreNotInitialisedError(FileNotFoundError):
    """Raised to indicate an uninitialised password store."""

class RecursiveCopyMoveError(OSError):
    """Raised when trying to copy a directory into itself or a
    subdirectory of itself.

    """
