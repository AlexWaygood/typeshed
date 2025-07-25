from collections.abc import Callable
from hashlib import _Hash
from typing import Any
from typing_extensions import Self

from .base import Key

# Enable when we can use stubs from installed dependencies:
# from ecdsa.curves import Curve
class ECDSAECKey(Key):
    """
    Performs signing and verification operations using
    ECDSA and the specified hash function

    This class requires the ecdsa package to be installed.

    This is based off of the implementation in PyJWT 0.3.2
    """

    SHA256: Callable[[bytes], _Hash]
    SHA384: Callable[[bytes], _Hash]
    SHA512: Callable[[bytes], _Hash]
    CURVE_MAP: Any
    CURVE_NAMES: Any
    hash_alg: Any
    curve: Any
    prepared_key: Any
    def __init__(self, key, algorithm) -> None: ...
    def sign(self, msg): ...
    def verify(self, msg, sig): ...
    def is_public(self) -> bool: ...
    def public_key(self) -> Self: ...
    def to_pem(self): ...
    def to_dict(self) -> dict[str, Any]: ...
