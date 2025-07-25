from _typeshed import Incomplete
from collections.abc import Collection, Mapping

from authlib.jose.rfc7517 import Key, KeySet

class JsonWebKey:
    JWK_KEY_CLS: Incomplete
    @classmethod
    def generate_key(cls, kty, crv_or_size, options=None, is_private: bool = False):
        """Generate a Key with the given key type, curve name or bit size.

        :param kty: string of ``oct``, ``RSA``, ``EC``, ``OKP``
        :param crv_or_size: curve name or bit size
        :param options: a dict of other options for Key
        :param is_private: create a private key or public key
        :return: Key instance
        """

    @classmethod
    def import_key(cls, raw: Mapping[str, object], options: Mapping[str, object] | None = None) -> Key:
        """Import a Key from bytes, string, PEM or dict.

        :return: Key instance
        """

    @classmethod
    def import_key_set(cls, raw: str | Collection[str] | dict[str, object]) -> KeySet:
        """Import KeySet from string, dict or a list of keys.

        :return: KeySet instance
        """
