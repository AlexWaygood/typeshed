from _typeshed import Incomplete

from authlib.oauth2.rfc8414 import AuthorizationServerMetadata

class OpenIDProviderMetadata(AuthorizationServerMetadata):
    REGISTRY_KEYS: Incomplete
    def validate_jwks_uri(self): ...
    def validate_acr_values_supported(self) -> None:
        """OPTIONAL. JSON array containing a list of the Authentication
        Context Class References that this OP supports.
        """

    def validate_subject_types_supported(self) -> None:
        """REQUIRED. JSON array containing a list of the Subject Identifier
        types that this OP supports. Valid types include pairwise and public.
        """

    def validate_id_token_signing_alg_values_supported(self) -> None:
        """REQUIRED. JSON array containing a list of the JWS signing
        algorithms (alg values) supported by the OP for the ID Token to
        encode the Claims in a JWT [JWT]. The algorithm RS256 MUST be
        included. The value none MAY be supported, but MUST NOT be used
        unless the Response Type used returns no ID Token from the
        Authorization Endpoint (such as when using the Authorization
        Code Flow).
        """

    def validate_id_token_encryption_alg_values_supported(self) -> None:
        """OPTIONAL. JSON array containing a list of the JWE encryption
        algorithms (alg values) supported by the OP for the ID Token to
        encode the Claims in a JWT.
        """

    def validate_id_token_encryption_enc_values_supported(self) -> None:
        """OPTIONAL. JSON array containing a list of the JWE encryption
        algorithms (enc values) supported by the OP for the ID Token to
        encode the Claims in a JWT.
        """

    def validate_userinfo_signing_alg_values_supported(self) -> None:
        """OPTIONAL. JSON array containing a list of the JWS signing
        algorithms (alg values) [JWA] supported by the UserInfo Endpoint
        to encode the Claims in a JWT. The value none MAY be included.
        """

    def validate_userinfo_encryption_alg_values_supported(self) -> None:
        """OPTIONAL. JSON array containing a list of the JWE encryption
        algorithms (alg values) [JWA] supported by the UserInfo Endpoint
        to encode the Claims in a JWT.
        """

    def validate_userinfo_encryption_enc_values_supported(self) -> None:
        """OPTIONAL. JSON array containing a list of the JWE encryption
        algorithms (enc values) [JWA] supported by the UserInfo Endpoint
        to encode the Claims in a JWT.
        """

    def validate_request_object_signing_alg_values_supported(self) -> None:
        """OPTIONAL. JSON array containing a list of the JWS signing
        algorithms (alg values) supported by the OP for Request Objects,
        which are described in Section 6.1 of OpenID Connect Core 1.0.
        These algorithms are used both when the Request Object is passed
        by value (using the request parameter) and when it is passed by
        reference (using the request_uri parameter). Servers SHOULD support
        none and RS256.
        """

    def validate_request_object_encryption_alg_values_supported(self) -> None:
        """OPTIONAL. JSON array containing a list of the JWE encryption
        algorithms (alg values) supported by the OP for Request Objects.
        These algorithms are used both when the Request Object is passed
        by value and when it is passed by reference.
        """

    def validate_request_object_encryption_enc_values_supported(self) -> None:
        """OPTIONAL. JSON array containing a list of the JWE encryption
        algorithms (enc values) supported by the OP for Request Objects.
        These algorithms are used both when the Request Object is passed
        by value and when it is passed by reference.
        """

    def validate_display_values_supported(self) -> None:
        """OPTIONAL. JSON array containing a list of the display parameter
        values that the OpenID Provider supports. These values are described
        in Section 3.1.2.1 of OpenID Connect Core 1.0.
        """

    def validate_claim_types_supported(self) -> None:
        """OPTIONAL. JSON array containing a list of the Claim Types that
        the OpenID Provider supports. These Claim Types are described in
        Section 5.6 of OpenID Connect Core 1.0. Values defined by this
        specification are normal, aggregated, and distributed. If omitted,
        the implementation supports only normal Claims.
        """

    def validate_claims_supported(self) -> None:
        """RECOMMENDED. JSON array containing a list of the Claim Names
        of the Claims that the OpenID Provider MAY be able to supply values
        for. Note that for privacy or other reasons, this might not be an
        exhaustive list.
        """

    def validate_claims_locales_supported(self) -> None:
        """OPTIONAL. Languages and scripts supported for values in Claims
        being returned, represented as a JSON array of BCP47 [RFC5646]
        language tag values. Not all languages and scripts are necessarily
        supported for all Claim values.
        """

    def validate_claims_parameter_supported(self) -> None:
        """OPTIONAL. Boolean value specifying whether the OP supports use of
        the claims parameter, with true indicating support. If omitted, the
        default value is false.
        """

    def validate_request_parameter_supported(self) -> None:
        """OPTIONAL. Boolean value specifying whether the OP supports use of
        the request parameter, with true indicating support. If omitted, the
        default value is false.
        """

    def validate_request_uri_parameter_supported(self) -> None:
        """OPTIONAL. Boolean value specifying whether the OP supports use of
        the request_uri parameter, with true indicating support. If omitted,
        the default value is true.
        """

    def validate_require_request_uri_registration(self) -> None:
        """OPTIONAL. Boolean value specifying whether the OP requires any
        request_uri values used to be pre-registered using the request_uris
        registration parameter. Pre-registration is REQUIRED when the value
        is true. If omitted, the default value is false.
        """

    @property
    def claim_types_supported(self): ...
    @property
    def claims_parameter_supported(self): ...
    @property
    def request_parameter_supported(self): ...
    @property
    def request_uri_parameter_supported(self): ...
    @property
    def require_request_uri_registration(self): ...
