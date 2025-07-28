from collections.abc import Mapping
from typing import Any, SupportsInt
from typing_extensions import deprecated

from jwcrypto.common import JWException, JWKeyNotFound
from jwcrypto.jwk import JWK, JWKSet

JWTClaimsRegistry: Mapping[str, str]
JWT_expect_type: bool

class JWTExpired(JWException):
    """JSON Web Token is expired.

    This exception is raised when a token is expired according to its claims.
    """

    def __init__(self, message: str | None = None, exception: BaseException | None = None) -> None: ...

class JWTNotYetValid(JWException):
    """JSON Web Token is not yet valid.

    This exception is raised when a token is not valid yet according to its
    claims.
    """

    def __init__(self, message: str | None = None, exception: BaseException | None = None) -> None: ...

class JWTMissingClaim(JWException):
    """JSON Web Token claim is invalid.

    This exception is raised when a claim does not match the expected value.
    """

    def __init__(self, message: str | None = None, exception: BaseException | None = None) -> None: ...

class JWTInvalidClaimValue(JWException):
    """JSON Web Token claim is invalid.

    This exception is raised when a claim does not match the expected value.
    """

    def __init__(self, message: str | None = None, exception: BaseException | None = None) -> None: ...

class JWTInvalidClaimFormat(JWException):
    """JSON Web Token claim format is invalid.

    This exception is raised when a claim is not in a valid format.
    """

    def __init__(self, message: str | None = None, exception: BaseException | None = None) -> None: ...

@deprecated("")
class JWTMissingKeyID(JWException):
    """JSON Web Token is missing key id.

    This exception is raised when trying to decode a JWT with a key set
    that does not have a kid value in its header.
    """

    def __init__(self, message: str | None = None, exception: BaseException | None = None) -> None: ...

class JWTMissingKey(JWKeyNotFound):
    """JSON Web Token is using a key not in the key set.

    This exception is raised if the key that was used is not available
    in the passed key set.
    """

    def __init__(self, message: str | None = None, exception: BaseException | None = None) -> None: ...

class JWT:
    """JSON Web token object

    This object represent a generic token.
    """

    deserializelog: list[str] | None
    def __init__(
        self,
        header: dict[str, Any] | str | None = None,
        claims: dict[str, Any] | str | None = None,
        jwt=None,
        key: JWK | JWKSet | None = None,
        algs=None,
        default_claims=None,
        check_claims=None,
        expected_type=None,
    ) -> None:
        """Creates a JWT object.

        :param header: A dict or a JSON string with the JWT Header data.
        :param claims: A dict or a string with the JWT Claims data.
        :param jwt: a 'raw' JWT token
        :param key: A (:class:`jwcrypto.jwk.JWK`) key to deserialize
         the token. A (:class:`jwcrypto.jwk.JWKSet`) can also be used.
        :param algs: An optional list of allowed algorithms
        :param default_claims: An optional dict with default values for
         registered claims. A None value for NumericDate type claims
         will cause generation according to system time. Only the values
         from RFC 7519 - 4.1 are evaluated.
        :param check_claims: An optional dict of claims that must be
         present in the token, if the value is not None the claim must
         match exactly.
        :param expected_type: An optional string that defines what kind
         of token to expect when validating a deserialized token.
         Supported values: "JWS" or "JWE"
         If left to None the code will try to detect what the expected
         type is based on other parameters like 'algs' and will default
         to JWS if no hints are found. It has no effect on token creation.

        Note: either the header,claims or jwt,key parameters should be
        provided as a deserialization operation (which occurs if the jwt
        is provided) will wipe any header or claim provided by setting
        those obtained from the deserialization of the jwt token.

        Note: if check_claims is not provided the 'exp' and 'nbf' claims
        are checked if they are set on the token but not enforced if not
        set. Any other RFC 7519 registered claims are checked only for
        format conformance.
        """

    @property
    def header(self) -> str: ...
    @header.setter
    def header(self, h: dict[str, Any] | str) -> None: ...
    @property
    def claims(self) -> str: ...
    @claims.setter
    def claims(self, data: str) -> None: ...
    @property
    def token(self): ...
    @token.setter
    def token(self, t) -> None: ...
    @property
    def leeway(self) -> int: ...
    @leeway.setter
    def leeway(self, lwy: SupportsInt) -> None: ...
    @property
    def validity(self) -> int: ...
    @validity.setter
    def validity(self, v: SupportsInt) -> None: ...
    @property
    def expected_type(self): ...
    @expected_type.setter
    def expected_type(self, v) -> None: ...
    def norm_typ(self, val): ...
    def make_signed_token(self, key: JWK) -> None:
        """Signs the payload.

        Creates a JWS token with the header as the JWS protected header and
        the claims as the payload. See (:class:`jwcrypto.jws.JWS`) for
        details on the exceptions that may be raised.

        :param key: A (:class:`jwcrypto.jwk.JWK`) key.
        """

    def make_encrypted_token(self, key: JWK) -> None:
        """Encrypts the payload.

        Creates a JWE token with the header as the JWE protected header and
        the claims as the plaintext. See (:class:`jwcrypto.jwe.JWE`) for
        details on the exceptions that may be raised.

        :param key: A (:class:`jwcrypto.jwk.JWK`) key.
        """

    def validate(self, key: JWK | JWKSet) -> None:
        """Validate a JWT token that was deserialized w/o providing a key

        :param key: A (:class:`jwcrypto.jwk.JWK`) verification or
         decryption key, or a (:class:`jwcrypto.jwk.JWKSet`) that
         contains a key indexed by the 'kid' header.
        """

    def deserialize(self, jwt, key=None) -> None:
        """Deserialize a JWT token.

        NOTE: Destroys any current status and tries to import the raw
        token provided.

        :param jwt: a 'raw' JWT token.
        :param key: A (:class:`jwcrypto.jwk.JWK`) verification or
         decryption key, or a (:class:`jwcrypto.jwk.JWKSet`) that
         contains a key indexed by the 'kid' header.
        """

    def serialize(self, compact: bool = True) -> str:
        """Serializes the object into a JWS token.

        :param compact(boolean): must be True.

        Note: the compact parameter is provided for general compatibility
        with the serialize() functions of :class:`jwcrypto.jws.JWS` and
        :class:`jwcrypto.jwe.JWE` so that these objects can all be used
        interchangeably. However the only valid JWT representation is the
        compact representation.

        :return: A json formatted string or a compact representation string
        :rtype: `str`
        """

    @classmethod
    def from_jose_token(cls, token):
        """Creates a JWT object from a serialized JWT token.

        :param token: A string with the json or compat representation
         of the token.

        :raises InvalidJWEData or InvalidJWSObject: if the raw object is an
         invalid JWT token.

        :return: A JWT token
        :rtype: JWT
        """

    def __eq__(self, other: object) -> bool: ...
