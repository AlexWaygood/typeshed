from _typeshed import Incomplete
from typing import ClassVar, Final

from authlib.jose.rfc7517 import Key

POSSIBLE_UNSAFE_KEYS: Final[tuple[bytes, ...]]

class OctKey(Key):
    """Key class of the ``oct`` key type."""

    kty: str
    REQUIRED_JSON_FIELDS: ClassVar[list[str]]
    raw_key: Incomplete
    def __init__(self, raw_key=None, options=None) -> None: ...
    @property
    def public_only(self): ...
    def get_op_key(self, operation):
        """Get the raw key for the given key_op. This method will also
        check if the given key_op is supported by this key.

        :param operation: key operation value, such as "sign", "encrypt".
        :return: raw key
        """

    def load_raw_key(self) -> None: ...
    def load_dict_key(self) -> None: ...
    def as_dict(self, is_private: bool = False, **params): ...
    @classmethod
    def validate_raw_key(cls, key): ...
    @classmethod
    def import_key(cls, raw, options=None):
        """Import a key from bytes, string, or dict data."""

    @classmethod
    def generate_key(cls, key_size: int = 256, options=None, is_private: bool = True):
        """Generate a ``OctKey`` with the given bit size."""
