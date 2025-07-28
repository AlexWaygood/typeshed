"""
Module version for monitoring CLI pipes (`... | python -m tqdm | ...`).
"""

from collections.abc import Sequence

__all__ = ["main"]

def main(fp=..., argv: Sequence[str] | None = None) -> None:
    """
    Parameters (internal use only)
    ---------
    fp  : file-like object for tqdm
    argv  : list (default: sys.argv[1:])
    """
