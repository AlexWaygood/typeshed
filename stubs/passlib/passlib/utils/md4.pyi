"""
passlib.utils.md4 - DEPRECATED MODULE, WILL BE REMOVED IN 2.0

MD4 should now be looked up through ``passlib.crypto.digest.lookup_hash("md4").const``,
which provides unified handling stdlib implementation (if present).
"""

from typing import Any

md4: Any

__all__ = ["md4"]
