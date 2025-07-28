from _typeshed import Incomplete

from authlib.jose import JWTClaims

__all__ = ["IDToken", "CodeIDToken", "ImplicitIDToken", "HybridIDToken", "UserInfo", "get_claim_cls_by_response_type"]

class IDToken(JWTClaims):
    ESSENTIAL_CLAIMS: Incomplete
    def validate(self, now=None, leeway: int = 0) -> None: ...
    def validate_auth_time(self) -> None:
        """Time when the End-User authentication occurred. Its value is a JSON
        number representing the number of seconds from 1970-01-01T0:0:0Z as
        measured in UTC until the date/time. When a max_age request is made or
        when auth_time is requested as an Essential Claim, then this Claim is
        REQUIRED; otherwise, its inclusion is OPTIONAL.
        """

    def validate_nonce(self) -> None:
        """String value used to associate a Client session with an ID Token,
        and to mitigate replay attacks. The value is passed through unmodified
        from the Authentication Request to the ID Token. If present in the ID
        Token, Clients MUST verify that the nonce Claim Value is equal to the
        value of the nonce parameter sent in the Authentication Request. If
        present in the Authentication Request, Authorization Servers MUST
        include a nonce Claim in the ID Token with the Claim Value being the
        nonce value sent in the Authentication Request. Authorization Servers
        SHOULD perform no other processing on nonce values used. The nonce
        value is a case sensitive string.
        """

    def validate_acr(self):
        """OPTIONAL. Authentication Context Class Reference. String specifying
        an Authentication Context Class Reference value that identifies the
        Authentication Context Class that the authentication performed
        satisfied. The value "0" indicates the End-User authentication did not
        meet the requirements of `ISO/IEC 29115`_ level 1. Authentication
        using a long-lived browser cookie, for instance, is one example where
        the use of "level 0" is appropriate. Authentications with level 0
        SHOULD NOT be used to authorize access to any resource of any monetary
        value. An absolute URI or an `RFC 6711`_ registered name SHOULD be
        used as the acr value; registered names MUST NOT be used with a
        different meaning than that which is registered. Parties using this
        claim will need to agree upon the meanings of the values used, which
        may be context-specific. The acr value is a case sensitive string.

        .. _`ISO/IEC 29115`: https://www.iso.org/standard/45138.html
        .. _`RFC 6711`: https://tools.ietf.org/html/rfc6711
        """

    def validate_amr(self) -> None:
        """OPTIONAL. Authentication Methods References. JSON array of strings
        that are identifiers for authentication methods used in the
        authentication. For instance, values might indicate that both password
        and OTP authentication methods were used. The definition of particular
        values to be used in the amr Claim is beyond the scope of this
        specification. Parties using this claim will need to agree upon the
        meanings of the values used, which may be context-specific. The amr
        value is an array of case sensitive strings.
        """

    def validate_azp(self) -> None:
        """OPTIONAL. Authorized party - the party to which the ID Token was
        issued. If present, it MUST contain the OAuth 2.0 Client ID of this
        party. This Claim is only needed when the ID Token has a single
        audience value and that audience is different than the authorized
        party. It MAY be included even when the authorized party is the same
        as the sole audience. The azp value is a case sensitive string
        containing a StringOrURI value.
        """

    def validate_at_hash(self) -> None:
        """OPTIONAL. Access Token hash value. Its value is the base64url
        encoding of the left-most half of the hash of the octets of the ASCII
        representation of the access_token value, where the hash algorithm
        used is the hash algorithm used in the alg Header Parameter of the
        ID Token's JOSE Header. For instance, if the alg is RS256, hash the
        access_token value with SHA-256, then take the left-most 128 bits and
        base64url encode them. The at_hash value is a case sensitive string.
        """

class CodeIDToken(IDToken):
    RESPONSE_TYPES: Incomplete

class ImplicitIDToken(IDToken):
    RESPONSE_TYPES: Incomplete
    ESSENTIAL_CLAIMS: Incomplete
    def validate_at_hash(self) -> None:
        """If the ID Token is issued from the Authorization Endpoint with an
        access_token value, which is the case for the response_type value
        id_token token, this is REQUIRED; it MAY NOT be used when no Access
        Token is issued, which is the case for the response_type value
        id_token.
        """

class HybridIDToken(ImplicitIDToken):
    RESPONSE_TYPES: Incomplete
    def validate(self, now=None, leeway: int = 0) -> None: ...
    def validate_c_hash(self) -> None:
        """Code hash value. Its value is the base64url encoding of the
        left-most half of the hash of the octets of the ASCII representation
        of the code value, where the hash algorithm used is the hash algorithm
        used in the alg Header Parameter of the ID Token's JOSE Header. For
        instance, if the alg is HS512, hash the code value with SHA-512, then
        take the left-most 256 bits and base64url encode them. The c_hash
        value is a case sensitive string.
        If the ID Token is issued from the Authorization Endpoint with a code,
        which is the case for the response_type values code id_token and code
        id_token token, this is REQUIRED; otherwise, its inclusion is OPTIONAL.
        """

class UserInfo(dict[str, object]):
    """The standard claims of a UserInfo object. Defined per `Section 5.1`_.

    .. _`Section 5.1`: http://openid.net/specs/openid-connect-core-1_0.html#StandardClaims
    """

    REGISTERED_CLAIMS: list[str]
    SCOPES_CLAIMS_MAPPING: dict[str, list[str]]
    def filter(self, scope: str) -> UserInfo:
        """Return a new UserInfo object containing only the claims matching the scope passed in parameter."""

    def __getattr__(self, key): ...

def get_claim_cls_by_response_type(response_type): ...
