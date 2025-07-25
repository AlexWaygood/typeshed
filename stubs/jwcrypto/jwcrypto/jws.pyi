from _typeshed import Incomplete
from collections.abc import Mapping
from typing import Any, Literal
from typing_extensions import Self

from jwcrypto.common import JWException, JWSEHeaderParameter
from jwcrypto.jwa import JWAAlgorithm
from jwcrypto.jwk import JWK, JWKSet

JWSHeaderRegistry: Mapping[str, JWSEHeaderParameter]
default_allowed_algs: list[str]

class InvalidJWSSignature(JWException):
    """Invalid JWS Signature.

    This exception is raised when a signature cannot be validated.
    """

    def __init__(self, message: str | None = None, exception: BaseException | None = None) -> None: ...

class InvalidJWSObject(JWException):
    """Invalid JWS Object.

    This exception is raised when the JWS Object is invalid and/or
    improperly formatted.
    """

    def __init__(self, message: str | None = None, exception: BaseException | None = None) -> None: ...

class InvalidJWSOperation(JWException):
    """Invalid JWS Object.

    This exception is raised when a requested operation cannot
    be execute due to unsatisfied conditions.
    """

    def __init__(self, message: str | None = None, exception: BaseException | None = None) -> None: ...

class JWSCore:
    """The inner JWS Core object.

    This object SHOULD NOT be used directly, the JWS object should be
    used instead as JWS perform necessary checks on the validity of
    the object and requested operations.

    """

    alg: str
    engine: JWAAlgorithm
    key: JWK | JWKSet
    header: dict[str, Any]
    protected: str
    payload: bytes
    def __init__(
        self,
        alg: str,
        key: JWK | JWKSet,
        header: dict[str, Any] | str | None,
        payload: str | bytes,
        algs: list[str] | None = None,
    ) -> None:
        """Core JWS token handling.

        :param alg: The algorithm used to produce the signature.
            See RFC 7518
        :param key: A (:class:`jwcrypto.jwk.JWK`) verification or
         a (:class:`jwcrypto.jwk.JWKSet`) that contains a key indexed by the
         'kid' header. A JWKSet is allowed only for verification operations.
        :param header: A JSON string representing the protected header.
        :param payload(bytes): An arbitrary value
        :param algs: An optional list of allowed algorithms

        :raises ValueError: if the key is not a (:class:`jwcrypto.jwk.JWK`)
        :raises InvalidJWAAlgorithm: if the algorithm is not valid, is
            unknown or otherwise not yet implemented.
        :raises InvalidJWSOperation: if the algorithm is not allowed.
        """

    def sign(self) -> dict[str, str | bytes]:
        """Generates a signature"""

    def verify(self, signature: bytes) -> Literal[True]:
        """Verifies a signature

        :raises InvalidJWSSignature: if the verification fails.

        :return: Returns True or an Exception
        :rtype: `bool`
        """

class JWS:
    """JSON Web Signature object

    This object represent a JWS token.
    """

    objects: Incomplete
    verifylog: list[str] | None
    header_registry: Incomplete
    def __init__(self, payload=None, header_registry=None) -> None:
        """Creates a JWS object.

        :param payload(bytes): An arbitrary value (optional).
        :param header_registry: Optional additions to the header registry
        """

    @property
    def allowed_algs(self):
        """Allowed algorithms.

        The list of allowed algorithms.
        Can be changed by setting a list of algorithm names.
        """

    @allowed_algs.setter
    def allowed_algs(self, algs) -> None: ...
    @property
    def is_valid(self): ...
    def verify(self, key, alg=None, detached_payload=None) -> None:
        """Verifies a JWS token.

        :param key: A (:class:`jwcrypto.jwk.JWK`) verification or
         a (:class:`jwcrypto.jwk.JWKSet`) that contains a key indexed by the
         'kid' header.
        :param alg: The signing algorithm (optional). Usually the algorithm
            is known as it is provided with the JOSE Headers of the token.
        :param detached_payload: A detached payload to verify the signature
            against. Only valid for tokens that are not carrying a payload.

        :raises InvalidJWSSignature: if the verification fails.
        :raises InvalidJWSOperation: if a detached_payload is provided but
                                     an object payload exists
        :raises JWKeyNotFound: if key is a JWKSet and the key is not found.
        """

    def deserialize(self, raw_jws, key=None, alg=None) -> None:
        """Deserialize a JWS token.

        NOTE: Destroys any current status and tries to import the raw
        JWS provided.

        If a key is provided a verification step will be attempted after
        the object is successfully deserialized.

        :param raw_jws: a 'raw' JWS token (JSON Encoded or Compact
         notation) string.
        :param key: A (:class:`jwcrypto.jwk.JWK`) verification or
         a (:class:`jwcrypto.jwk.JWKSet`) that contains a key indexed by the
         'kid' header (optional).
        :param alg: The signing algorithm (optional). Usually the algorithm
         is known as it is provided with the JOSE Headers of the token.

        :raises InvalidJWSObject: if the raw object is an invalid JWS token.
        :raises InvalidJWSSignature: if the verification fails.
        :raises JWKeyNotFound: if key is a JWKSet and the key is not found.
        """

    def add_signature(self, key, alg=None, protected=None, header=None) -> None:
        """Adds a new signature to the object.

        :param key: A (:class:`jwcrypto.jwk.JWK`) key of appropriate for
         the "alg" provided.
        :param alg: An optional algorithm name. If already provided as an
         element of the protected or unprotected header it can be safely
         omitted.
        :param protected: The Protected Header (optional)
        :param header: The Unprotected Header (optional)

        :raises InvalidJWSObject: if invalid headers are provided.
        :raises ValueError: if the key is not a (:class:`jwcrypto.jwk.JWK`)
        :raises ValueError: if the algorithm is missing or is not provided
         by one of the headers.
        :raises InvalidJWAAlgorithm: if the algorithm is not valid, is
         unknown or otherwise not yet implemented.
        """

    def serialize(self, compact: bool = False) -> str:
        """Serializes the object into a JWS token.

        :param compact(boolean): if True generates the compact
         representation, otherwise generates a standard JSON format.

        :raises InvalidJWSOperation: if the object cannot serialized
         with the compact representation and `compact` is True.
        :raises InvalidJWSSignature: if no signature has been added
         to the object, or no valid signature can be found.

        :return: A json formatted string or a compact representation string
        :rtype: `str`
        """

    @property
    def payload(self): ...
    def detach_payload(self) -> None: ...
    @property
    def jose_header(self): ...
    @classmethod
    def from_jose_token(cls, token: str | bytes) -> Self:
        """Creates a JWS object from a serialized JWS token.

        :param token: A string with the json or compat representation
         of the token.

        :raises InvalidJWSObject: if the raw object is an invalid JWS token.

        :return: A JWS token
        :rtype: JWS
        """

    def __eq__(self, other: object) -> bool: ...
