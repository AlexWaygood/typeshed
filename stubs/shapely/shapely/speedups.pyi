"""Speedups for Shapely geometry operations.

.. deprecated:: 2.0
        Deprecated in Shapely 2.0, and will be removed in a future version.

"""

from typing import Final
from typing_extensions import deprecated

__all__ = ["available", "enable", "disable", "enabled"]

available: Final = True
enabled: Final = True

@deprecated("Function `enable` is deprecated and no longer has any effect. Speedups are always available.")
def enable() -> None:
    """Will be removed in a future release and has no longer any effect.

    Previously, this function enabled cython-based speedups. Starting with
    Shapely 2.0, equivalent speedups are available in every installation.
    """

@deprecated("Function `disable` is deprecated and no longer has any effect. Speedups are always available.")
def disable() -> None:
    """Will be removed in a future release and has no longer any effect.

    Previously, this function enabled cython-based speedups. Starting with
    Shapely 2.0, equivalent speedups are available in every installation.
    """
