from _typeshed import Incomplete
from typing import ClassVar

class Key:
    """This is the base class for a JSON Web Key."""

    kty: str
    ALLOWED_PARAMS: ClassVar[list[str]]
    PRIVATE_KEY_OPS: ClassVar[list[str]]
    PUBLIC_KEY_OPS: ClassVar[list[str]]
    REQUIRED_JSON_FIELDS: ClassVar[list[str]]
    options: Incomplete
    def __init__(self, options=None) -> None: ...
    @property
    def tokens(self): ...
    @property
    def kid(self): ...
    def keys(self): ...
    def __getitem__(self, item): ...
    @property
    def public_only(self) -> None: ...
    def load_raw_key(self) -> None: ...
    def load_dict_key(self) -> None: ...
    def check_key_op(self, operation) -> None:
        """Check if the given key_op is supported by this key.

        :param operation: key operation value, such as "sign", "encrypt".
        :raise: ValueError
        """

    def as_dict(self, is_private: bool = False, **params) -> None: ...
    def as_json(self, is_private: bool = False, **params):
        """Represent this key as a JSON string."""

    def thumbprint(self):
        """Implementation of RFC7638 JSON Web Key (JWK) Thumbprint."""

    @classmethod
    def check_required_fields(cls, data) -> None: ...
    @classmethod
    def validate_raw_key(cls, key) -> None: ...
