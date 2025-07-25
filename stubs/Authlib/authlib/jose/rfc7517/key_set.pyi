from collections.abc import Collection

from authlib.jose.rfc7517 import Key

class KeySet:
    """This class represents a JSON Web Key Set."""

    keys: Collection[Key]
    def __init__(self, keys) -> None: ...
    def as_dict(self, is_private: bool = False, **params):
        """Represent this key as a dict of the JSON Web Key Set."""

    def as_json(self, is_private: bool = False, **params):
        """Represent this key set as a JSON string."""

    def find_by_kid(self, kid):
        """Find the key matches the given kid value.

        :param kid: A string of kid
        :return: Key instance
        :raise: ValueError
        """
