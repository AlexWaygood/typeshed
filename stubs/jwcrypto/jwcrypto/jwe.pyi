from _typeshed import Incomplete
from collections.abc import Mapping, Sequence
from typing import Any
from typing_extensions import Self

from jwcrypto import common
from jwcrypto.common import JWException, JWSEHeaderParameter, JWSEHeaderRegistry
from jwcrypto.jwk import JWK, JWKSet

default_max_compressed_size: int
JWEHeaderRegistry: Mapping[str, JWSEHeaderParameter]
default_allowed_algs: Sequence[str]

class InvalidJWEData(JWException):
    """Invalid JWE Object.

    This exception is raised when the JWE Object is invalid and/or
    improperly formatted.
    """

    def __init__(self, message: str | None = None, exception: BaseException | None = None) -> None: ...

InvalidCEKeyLength = common.InvalidCEKeyLength
InvalidJWEKeyLength = common.InvalidJWEKeyLength
InvalidJWEKeyType = common.InvalidJWEKeyType
InvalidJWEOperation = common.InvalidJWEOperation

class JWE:
    """JSON Web Encryption object

    This object represent a JWE token.
    """

    objects: dict[str, Any]
    plaintext: bytes | None
    header_registry: JWSEHeaderRegistry
    cek: Incomplete
    decryptlog: list[str] | None
    def __init__(
        self,
        plaintext: str | bytes | None = None,
        protected: str | None = None,
        unprotected: str | None = None,
        aad: bytes | None = None,
        algs: list[str] | None = None,
        recipient: str | None = None,
        header: str | None = None,
        header_registry: Mapping[str, JWSEHeaderParameter] | None = None,
    ) -> None:
        """Creates a JWE token.

        :param plaintext(bytes): An arbitrary plaintext to be encrypted.
        :param protected: A JSON string with the protected header.
        :param unprotected: A JSON string with the shared unprotected header.
        :param aad(bytes): Arbitrary additional authenticated data
        :param algs: An optional list of allowed algorithms
        :param recipient: An optional, default recipient key
        :param header: An optional header for the default recipient
        :param header_registry: Optional additions to the header registry
        """

    @property
    def allowed_algs(self) -> list[str]:
        """Allowed algorithms.

        The list of allowed algorithms.
        Can be changed by setting a list of algorithm names.
        """

    @allowed_algs.setter
    def allowed_algs(self, algs: list[str]) -> None: ...
    def add_recipient(self, key: JWK, header: dict[str, Any] | str | None = None) -> None:
        """Encrypt the plaintext with the given key.

        :param key: A JWK key or password of appropriate type for the 'alg'
         provided in the JOSE Headers.
        :param header: A JSON string representing the per-recipient header.

        :raises ValueError: if the plaintext is missing or not of type bytes.
        :raises ValueError: if the compression type is unknown.
        :raises InvalidJWAAlgorithm: if the 'alg' provided in the JOSE
         headers is missing or unknown, or otherwise not implemented.
        """

    def serialize(self, compact: bool = False) -> str:
        """Serializes the object into a JWE token.

        :param compact(boolean): if True generates the compact
         representation, otherwise generates a standard JSON format.

        :raises InvalidJWEOperation: if the object cannot be serialized
         with the compact representation and `compact` is True.
        :raises InvalidJWEOperation: if no recipients have been added
         to the object.

        :return: A json formatted string or a compact representation string
        :rtype: `str`
        """

    def decrypt(self, key: JWK | JWKSet) -> None:
        """Decrypt a JWE token.

        :param key: The (:class:`jwcrypto.jwk.JWK`) decryption key.
        :param key: A (:class:`jwcrypto.jwk.JWK`) decryption key,
         or a (:class:`jwcrypto.jwk.JWKSet`) that contains a key indexed
         by the 'kid' header or (deprecated) a string containing a password.

        :raises InvalidJWEOperation: if the key is not a JWK object.
        :raises InvalidJWEData: if the ciphertext can't be decrypted or
         the object is otherwise malformed.
        :raises JWKeyNotFound: if key is a JWKSet and the key is not found.
        """

    def deserialize(self, raw_jwe: str | bytes, key: JWK | JWKSet | None = None) -> None:
        """Deserialize a JWE token.

        NOTE: Destroys any current status and tries to import the raw
        JWE provided.

        If a key is provided a decryption step will be attempted after
        the object is successfully deserialized.

        :param raw_jwe: a 'raw' JWE token (JSON Encoded or Compact
         notation) string.
        :param key: A (:class:`jwcrypto.jwk.JWK`) decryption key,
         or a (:class:`jwcrypto.jwk.JWKSet`) that contains a key indexed
         by the 'kid' header or (deprecated) a string containing a password
         (optional).

        :raises InvalidJWEData: if the raw object is an invalid JWE token.
        :raises InvalidJWEOperation: if the decryption fails.
        """

    @property
    def payload(self) -> bytes: ...
    @property
    def jose_header(self) -> dict[Incomplete, Incomplete]: ...
    @classmethod
    def from_jose_token(cls, token: str | bytes) -> Self:
        """Creates a JWE object from a serialized JWE token.

        :param token: A string with the json or compat representation
         of the token.

        :raises InvalidJWEData: if the raw object is an invalid JWE token.

        :return: A JWE token
        :rtype: JWE
        """

    def __eq__(self, other: object) -> bool: ...
