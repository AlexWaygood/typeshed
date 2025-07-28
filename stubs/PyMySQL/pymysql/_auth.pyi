"""
Implements auth methods
"""

from _typeshed import Incomplete, ReadableBuffer
from typing import Final

DEBUG: Final[bool]
SCRAMBLE_LENGTH: Final[int]
sha1_new: Incomplete

def scramble_native_password(password: ReadableBuffer | None, message: ReadableBuffer | None) -> bytes:
    """Scramble used for mysql_native_password"""

def ed25519_password(password: ReadableBuffer, scramble: ReadableBuffer) -> bytes:
    """Sign a random scramble with elliptic curve Ed25519.

    Secret and public key are derived from password.
    """

def sha2_rsa_encrypt(password: bytes, salt: bytes, public_key: bytes) -> bytes:
    """Encrypt password with salt and public_key.

    Used for sha256_password and caching_sha2_password.
    """

def sha256_password_auth(conn, pkt): ...
def scramble_caching_sha2(password: ReadableBuffer, nonce: ReadableBuffer) -> bytes:
    """Scramble algorithm used in cached_sha2_password fast path.

    XOR(SHA256(password), SHA256(SHA256(SHA256(password)), nonce))
    """

def caching_sha2_password_auth(conn, pkt) -> Incomplete | None: ...
