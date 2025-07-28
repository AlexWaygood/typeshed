from _typeshed import Incomplete
from typing import ClassVar

from authlib.jose.rfc7517 import Key

class AsymmetricKey(Key):
    """This is the base class for a JSON Web Key."""

    PUBLIC_KEY_FIELDS: ClassVar[list[str]]
    PRIVATE_KEY_FIELDS: ClassVar[list[str]]
    PRIVATE_KEY_CLS: ClassVar[type | tuple[type, ...]]
    PUBLIC_KEY_CLS: ClassVar[type | tuple[type, ...]]
    SSH_PUBLIC_PREFIX: ClassVar[bytes]
    private_key: Incomplete
    public_key: Incomplete
    def __init__(self, private_key=None, public_key=None, options=None) -> None: ...
    @property
    def public_only(self): ...
    def get_op_key(self, operation):
        """Get the raw key for the given key_op. This method will also
        check if the given key_op is supported by this key.

        :param operation: key operation value, such as "sign", "encrypt".
        :return: raw key
        """

    def get_public_key(self): ...
    def get_private_key(self): ...
    def load_raw_key(self) -> None: ...
    def load_dict_key(self) -> None: ...
    def dumps_private_key(self): ...
    def dumps_public_key(self): ...
    def load_private_key(self): ...
    def load_public_key(self): ...
    def as_dict(self, is_private: bool = False, **params):
        """Represent this key as a dict of the JSON Web Key."""

    def as_key(self, is_private: bool = False):
        """Represent this key as raw key."""

    def as_bytes(self, encoding=None, is_private: bool = False, password=None):
        """Export key into PEM/DER format bytes.

        :param encoding: "PEM" or "DER"
        :param is_private: export private key or public key
        :param password: encrypt private key with password
        :return: bytes
        """

    def as_pem(self, is_private: bool = False, password=None): ...
    def as_der(self, is_private: bool = False, password=None): ...
    @classmethod
    def import_dict_key(cls, raw, options=None): ...
    @classmethod
    def import_key(cls, raw, options=None): ...
    @classmethod
    def validate_raw_key(cls, key): ...
    @classmethod
    def generate_key(cls, crv_or_size, options=None, is_private: bool = False) -> AsymmetricKey: ...
