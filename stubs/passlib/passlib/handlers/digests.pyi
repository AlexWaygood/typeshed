"""passlib.handlers.digests - plain hash digests"""

from _typeshed import Incomplete
from typing import ClassVar
from typing_extensions import deprecated

import passlib.utils.handlers as uh

class HexDigestHash(uh.StaticHandler):
    """this provides a template for supporting passwords stored as plain hexadecimal hashes"""

    checksum_chars: ClassVar[str]
    supported: ClassVar[bool]

def create_hex_hash(digest, module="passlib.handlers.digests", django_name=None, required: bool = True):
    """
    create hex-encoded unsalted hasher for specified digest algorithm.

    .. versionchanged:: 1.7.3
        If called with unknown/supported digest, won't throw error immediately,
        but instead return a dummy hasher that will throw error when called.

        set ``required=True`` to restore old behavior.
    """

hex_md4: Incomplete
hex_md5: Incomplete
hex_sha1: Incomplete
hex_sha256: Incomplete
hex_sha512: Incomplete

class htdigest(uh.MinimalHandler):
    """htdigest hash function.

    .. todo::
        document this hash
    """

    name: ClassVar[str]
    default_encoding: ClassVar[str]
    setting_kwds: ClassVar[tuple[str, ...]]
    context_kwds: ClassVar[tuple[str, ...]]
    @classmethod
    def hash(cls, secret, user, realm, encoding=None): ...  # type: ignore[override]
    @classmethod
    def verify(cls, secret, hash, user, realm, encoding: str = "utf-8"): ...  # type: ignore[override]
    @classmethod
    def identify(cls, hash): ...
    @deprecated("Deprecated since Passlib 1.7, will be removed in 2.0")
    @classmethod
    def genconfig(cls): ...  # type: ignore[override]
    @deprecated("Deprecated since Passlib 1.7, will be removed in 2.0")
    @classmethod
    def genhash(cls, secret, config, user, realm, encoding=None): ...  # type: ignore[override]

__all__ = ["create_hex_hash", "hex_md4", "hex_md5", "hex_sha1", "hex_sha256", "hex_sha512"]
