from _typeshed import Incomplete
from typing import Any, ClassVar

class BaseClaims(dict[str, Any]):  # dict values are key-dependent
    """Payload claims for JWT, which contains a validate interface.

    :param payload: the payload dict of JWT
    :param header: the header dict of JWT
    :param options: validate options
    :param params: other params

    An example on ``options`` parameter, the format is inspired by
    `OpenID Connect Claims`_::

        {
            "iss": {
                "essential": True,
                "values": ["https://example.com", "https://example.org"]
            },
            "sub": {
                "essential": True
                "value": "248289761001"
            },
            "jti": {
                "validate": validate_jti
            }
        }

    .. _`OpenID Connect Claims`:
        http://openid.net/specs/openid-connect-core-1_0.html#IndividualClaimsRequests
    """

    REGISTERED_CLAIMS: ClassVar[list[str]]
    header: Incomplete
    options: Incomplete
    params: Incomplete
    def __init__(self, payload, header, options=None, params=None) -> None: ...
    # TODO: Adds an attribute for each key in REGISTERED_CLAIMS
    def __getattr__(self, key: str): ...
    def get_registered_claims(self) -> dict[str, Incomplete]: ...

class JWTClaims(BaseClaims):
    def validate(self, now=None, leeway: int = 0) -> None:
        """Validate everything in claims payload."""

    def validate_iss(self) -> None:
        """The "iss" (issuer) claim identifies the principal that issued the
        JWT.  The processing of this claim is generally application specific.
        The "iss" value is a case-sensitive string containing a StringOrURI
        value.  Use of this claim is OPTIONAL.
        """

    def validate_sub(self) -> None:
        """The "sub" (subject) claim identifies the principal that is the
        subject of the JWT.  The claims in a JWT are normally statements
        about the subject.  The subject value MUST either be scoped to be
        locally unique in the context of the issuer or be globally unique.
        The processing of this claim is generally application specific.  The
        "sub" value is a case-sensitive string containing a StringOrURI
        value.  Use of this claim is OPTIONAL.
        """

    def validate_aud(self) -> None:
        """The "aud" (audience) claim identifies the recipients that the JWT is
        intended for.  Each principal intended to process the JWT MUST
        identify itself with a value in the audience claim.  If the principal
        processing the claim does not identify itself with a value in the
        "aud" claim when this claim is present, then the JWT MUST be
        rejected.  In the general case, the "aud" value is an array of case-
        sensitive strings, each containing a StringOrURI value.  In the
        special case when the JWT has one audience, the "aud" value MAY be a
        single case-sensitive string containing a StringOrURI value.  The
        interpretation of audience values is generally application specific.
        Use of this claim is OPTIONAL.
        """

    def validate_exp(self, now, leeway) -> None:
        """The "exp" (expiration time) claim identifies the expiration time on
        or after which the JWT MUST NOT be accepted for processing.  The
        processing of the "exp" claim requires that the current date/time
        MUST be before the expiration date/time listed in the "exp" claim.
        Implementers MAY provide for some small leeway, usually no more than
        a few minutes, to account for clock skew.  Its value MUST be a number
        containing a NumericDate value.  Use of this claim is OPTIONAL.
        """

    def validate_nbf(self, now, leeway) -> None:
        """The "nbf" (not before) claim identifies the time before which the JWT
        MUST NOT be accepted for processing.  The processing of the "nbf"
        claim requires that the current date/time MUST be after or equal to
        the not-before date/time listed in the "nbf" claim.  Implementers MAY
        provide for some small leeway, usually no more than a few minutes, to
        account for clock skew.  Its value MUST be a number containing a
        NumericDate value.  Use of this claim is OPTIONAL.
        """

    def validate_iat(self, now, leeway) -> None:
        """The "iat" (issued at) claim identifies the time at which the JWT was
        issued.  This claim can be used to determine the age of the JWT.
        Implementers MAY provide for some small leeway, usually no more
        than a few minutes, to account for clock skew. Its value MUST be a
        number containing a NumericDate value.  Use of this claim is OPTIONAL.
        """

    def validate_jti(self) -> None:
        """The "jti" (JWT ID) claim provides a unique identifier for the JWT.
        The identifier value MUST be assigned in a manner that ensures that
        there is a negligible probability that the same value will be
        accidentally assigned to a different data object; if the application
        uses multiple issuers, collisions MUST be prevented among values
        produced by different issuers as well.  The "jti" claim can be used
        to prevent the JWT from being replayed.  The "jti" value is a case-
        sensitive string.  Use of this claim is OPTIONAL.
        """
