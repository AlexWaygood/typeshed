from _typeshed import Incomplete

class AuthorizationServerMetadata(dict[str, object]):
    """Define Authorization Server Metadata via `Section 2`_ in RFC8414_.

    .. _RFC8414: https://tools.ietf.org/html/rfc8414
    .. _`Section 2`: https://tools.ietf.org/html/rfc8414#section-2
    """

    REGISTRY_KEYS: Incomplete
    def validate_issuer(self) -> None:
        """REQUIRED. The authorization server's issuer identifier, which is
        a URL that uses the "https" scheme and has no query or fragment
        components.
        """

    def validate_authorization_endpoint(self) -> None:
        """URL of the authorization server's authorization endpoint
        [RFC6749]. This is REQUIRED unless no grant types are supported
        that use the authorization endpoint.
        """

    def validate_token_endpoint(self) -> None:
        """URL of the authorization server's token endpoint [RFC6749]. This
        is REQUIRED unless only the implicit grant type is supported.
        """

    def validate_jwks_uri(self) -> None:
        """OPTIONAL.  URL of the authorization server's JWK Set [JWK]
        document.  The referenced document contains the signing key(s) the
        client uses to validate signatures from the authorization server.
        This URL MUST use the "https" scheme.  The JWK Set MAY also
        contain the server's encryption key or keys, which are used by
        clients to encrypt requests to the server.  When both signing and
        encryption keys are made available, a "use" (public key use)
        parameter value is REQUIRED for all keys in the referenced JWK Set
        to indicate each key's intended usage.
        """

    def validate_registration_endpoint(self) -> None:
        """OPTIONAL.  URL of the authorization server's OAuth 2.0 Dynamic
        Client Registration endpoint [RFC7591].
        """

    def validate_scopes_supported(self) -> None:
        """RECOMMENDED. JSON array containing a list of the OAuth 2.0
        [RFC6749] "scope" values that this authorization server supports.
        Servers MAY choose not to advertise some supported scope values
        even when this parameter is used.
        """

    def validate_response_types_supported(self) -> None:
        """REQUIRED.  JSON array containing a list of the OAuth 2.0
        "response_type" values that this authorization server supports.
        The array values used are the same as those used with the
        "response_types" parameter defined by "OAuth 2.0 Dynamic Client
        Registration Protocol" [RFC7591].
        """

    def validate_response_modes_supported(self) -> None:
        """OPTIONAL.  JSON array containing a list of the OAuth 2.0
        "response_mode" values that this authorization server supports, as
        specified in "OAuth 2.0 Multiple Response Type Encoding Practices"
        [OAuth.Responses].  If omitted, the default is "["query",
        "fragment"]".  The response mode value "form_post" is also defined
        in "OAuth 2.0 Form Post Response Mode" [OAuth.Post].
        """

    def validate_grant_types_supported(self) -> None:
        """OPTIONAL. JSON array containing a list of the OAuth 2.0 grant
        type values that this authorization server supports.  The array
        values used are the same as those used with the "grant_types"
        parameter defined by "OAuth 2.0 Dynamic Client Registration
        Protocol" [RFC7591].  If omitted, the default value is
        "["authorization_code", "implicit"]".
        """

    def validate_token_endpoint_auth_methods_supported(self) -> None:
        """OPTIONAL.  JSON array containing a list of client authentication
        methods supported by this token endpoint.  Client authentication
        method values are used in the "token_endpoint_auth_method"
        parameter defined in Section 2 of [RFC7591].  If omitted, the
        default is "client_secret_basic" -- the HTTP Basic Authentication
        Scheme specified in Section 2.3.1 of OAuth 2.0 [RFC6749].
        """

    def validate_token_endpoint_auth_signing_alg_values_supported(self) -> None:
        """OPTIONAL.  JSON array containing a list of the JWS signing
        algorithms ("alg" values) supported by the token endpoint for the
        signature on the JWT [JWT] used to authenticate the client at the
        token endpoint for the "private_key_jwt" and "client_secret_jwt"
        authentication methods.  This metadata entry MUST be present if
        either of these authentication methods are specified in the
        "token_endpoint_auth_methods_supported" entry.  No default
        algorithms are implied if this entry is omitted.  Servers SHOULD
        support "RS256".  The value "none" MUST NOT be used.
        """

    def validate_service_documentation(self) -> None:
        """OPTIONAL. URL of a page containing human-readable information
        that developers might want or need to know when using the
        authorization server.  In particular, if the authorization server
        does not support Dynamic Client Registration, then information on
        how to register clients needs to be provided in this
        documentation.
        """

    def validate_ui_locales_supported(self) -> None:
        """OPTIONAL.  Languages and scripts supported for the user interface,
        represented as a JSON array of language tag values from BCP 47
        [RFC5646].  If omitted, the set of supported languages and scripts
        is unspecified.
        """

    def validate_op_policy_uri(self) -> None:
        """OPTIONAL.  URL that the authorization server provides to the
        person registering the client to read about the authorization
        server's requirements on how the client can use the data provided
        by the authorization server.  The registration process SHOULD
        display this URL to the person registering the client if it is
        given.  As described in Section 5, despite the identifier
        "op_policy_uri" appearing to be OpenID-specific, its usage in this
        specification is actually referring to a general OAuth 2.0 feature
        that is not specific to OpenID Connect.
        """

    def validate_op_tos_uri(self) -> None:
        """OPTIONAL.  URL that the authorization server provides to the
        person registering the client to read about the authorization
        server's terms of service.  The registration process SHOULD
        display this URL to the person registering the client if it is
        given.  As described in Section 5, despite the identifier
        "op_tos_uri", appearing to be OpenID-specific, its usage in this
        specification is actually referring to a general OAuth 2.0 feature
        that is not specific to OpenID Connect.
        """

    def validate_revocation_endpoint(self) -> None:
        """OPTIONAL. URL of the authorization server's OAuth 2.0 revocation
        endpoint [RFC7009].
        """

    def validate_revocation_endpoint_auth_methods_supported(self) -> None:
        """OPTIONAL.  JSON array containing a list of client authentication
        methods supported by this revocation endpoint.  The valid client
        authentication method values are those registered in the IANA
        "OAuth Token Endpoint Authentication Methods" registry
        [IANA.OAuth.Parameters].  If omitted, the default is
        "client_secret_basic" -- the HTTP Basic Authentication Scheme
        specified in Section 2.3.1 of OAuth 2.0 [RFC6749].
        """

    def validate_revocation_endpoint_auth_signing_alg_values_supported(self) -> None:
        """OPTIONAL.  JSON array containing a list of the JWS signing
        algorithms ("alg" values) supported by the revocation endpoint for
        the signature on the JWT [JWT] used to authenticate the client at
        the revocation endpoint for the "private_key_jwt" and
        "client_secret_jwt" authentication methods.  This metadata entry
        MUST be present if either of these authentication methods are
        specified in the "revocation_endpoint_auth_methods_supported"
        entry.  No default algorithms are implied if this entry is
        omitted.  The value "none" MUST NOT be used.
        """

    def validate_introspection_endpoint(self) -> None:
        """OPTIONAL.  URL of the authorization server's OAuth 2.0
        introspection endpoint [RFC7662].
        """

    def validate_introspection_endpoint_auth_methods_supported(self) -> None:
        """OPTIONAL.  JSON array containing a list of client authentication
        methods supported by this introspection endpoint.  The valid
        client authentication method values are those registered in the
        IANA "OAuth Token Endpoint Authentication Methods" registry
        [IANA.OAuth.Parameters] or those registered in the IANA "OAuth
        Access Token Types" registry [IANA.OAuth.Parameters].  (These
        values are and will remain distinct, due to Section 7.2.)  If
        omitted, the set of supported authentication methods MUST be
        determined by other means.
        """

    def validate_introspection_endpoint_auth_signing_alg_values_supported(self) -> None:
        """OPTIONAL.  JSON array containing a list of the JWS signing
        algorithms ("alg" values) supported by the introspection endpoint
        for the signature on the JWT [JWT] used to authenticate the client
        at the introspection endpoint for the "private_key_jwt" and
        "client_secret_jwt" authentication methods.  This metadata entry
        MUST be present if either of these authentication methods are
        specified in the "introspection_endpoint_auth_methods_supported"
        entry.  No default algorithms are implied if this entry is
        omitted.  The value "none" MUST NOT be used.
        """

    def validate_code_challenge_methods_supported(self) -> None:
        """OPTIONAL.  JSON array containing a list of Proof Key for Code
        Exchange (PKCE) [RFC7636] code challenge methods supported by this
        authorization server.  Code challenge method values are used in
        the "code_challenge_method" parameter defined in Section 4.3 of
        [RFC7636].  The valid code challenge method values are those
        registered in the IANA "PKCE Code Challenge Methods" registry
        [IANA.OAuth.Parameters].  If omitted, the authorization server
        does not support PKCE.
        """

    @property
    def response_modes_supported(self): ...
    @property
    def grant_types_supported(self): ...
    @property
    def token_endpoint_auth_methods_supported(self): ...
    @property
    def revocation_endpoint_auth_methods_supported(self): ...
    @property
    def introspection_endpoint_auth_methods_supported(self): ...
    def validate(self) -> None:
        """Validate all server metadata value."""

    def __getattr__(self, key): ...

def validate_array_value(metadata, key) -> None: ...
