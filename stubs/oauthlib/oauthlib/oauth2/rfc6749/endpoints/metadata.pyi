"""
oauthlib.oauth2.rfc6749.endpoint.metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An implementation of the `OAuth 2.0 Authorization Server Metadata`.

.. _`OAuth 2.0 Authorization Server Metadata`: https://tools.ietf.org/html/rfc8414
"""

from _typeshed import Incomplete
from collections.abc import Iterable
from logging import Logger

from .base import BaseEndpoint

log: Logger

class MetadataEndpoint(BaseEndpoint):
    """OAuth2.0 Authorization Server Metadata endpoint.

    This specification generalizes the metadata format defined by
    `OpenID Connect Discovery 1.0` in a way that is compatible
    with OpenID Connect Discovery while being applicable to a wider set
    of OAuth 2.0 use cases.  This is intentionally parallel to the way
    that OAuth 2.0 Dynamic Client Registration Protocol [`RFC7591`_]
    generalized the dynamic client registration mechanisms defined by
    OpenID Connect Dynamic Client Registration 1.0
    in a way that is compatible with it.

    .. _`OpenID Connect Discovery 1.0`: https://openid.net/specs/openid-connect-discovery-1_0.html
    .. _`RFC7591`: https://tools.ietf.org/html/rfc7591
    """

    raise_errors: bool
    endpoints: Iterable[BaseEndpoint]
    initial_claims: dict[str, Incomplete]
    claims: dict[str, Incomplete]
    def __init__(
        self, endpoints: Iterable[BaseEndpoint], claims: dict[str, Incomplete] = {}, raise_errors: bool = True
    ) -> None: ...
    def create_metadata_response(
        self, uri: str, http_method: str = "GET", body: str | None = None, headers: dict[str, str] | None = None
    ) -> tuple[dict[str, str], str, int]:
        """Create metadata response"""

    def validate_metadata(
        self, array, key, is_required: bool = False, is_list: bool = False, is_url: bool = False, is_issuer: bool = False
    ) -> None: ...
    def validate_metadata_token(self, claims, endpoint: BaseEndpoint) -> None:
        """
        If the token endpoint is used in the grant type, the value of this
        parameter MUST be the same as the value of the "grant_type"
        parameter passed to the token endpoint defined in the grant type
        definition.
        """

    def validate_metadata_authorization(self, claims, endpoint: BaseEndpoint): ...
    def validate_metadata_revocation(self, claims, endpoint: BaseEndpoint) -> None: ...
    def validate_metadata_introspection(self, claims, endpoint: BaseEndpoint) -> None: ...
    def validate_metadata_server(self) -> dict[str, Incomplete]:
        """
         Authorization servers can have metadata describing their
         configuration.  The following authorization server metadata values
         are used by this specification. More details can be found in
         `RFC8414 section 2`_ :

        issuer
           REQUIRED

        authorization_endpoint
           URL of the authorization server's authorization endpoint
           [`RFC6749#Authorization`_].  This is REQUIRED unless no grant types are supported
           that use the authorization endpoint.

        token_endpoint
           URL of the authorization server's token endpoint [`RFC6749#Token`_].  This
           is REQUIRED unless only the implicit grant type is supported.

        scopes_supported
           RECOMMENDED.

        response_types_supported
           REQUIRED.

        Other OPTIONAL fields:
           jwks_uri,
           registration_endpoint,
           response_modes_supported

        grant_types_supported
           OPTIONAL.  JSON array containing a list of the OAuth 2.0 grant
           type values that this authorization server supports.  The array
           values used are the same as those used with the "grant_types"
           parameter defined by "OAuth 2.0 Dynamic Client Registration
           Protocol" [`RFC7591`_].  If omitted, the default value is
           "["authorization_code", "implicit"]".

        token_endpoint_auth_methods_supported

        token_endpoint_auth_signing_alg_values_supported

        service_documentation

        ui_locales_supported

        op_policy_uri

        op_tos_uri

        revocation_endpoint

        revocation_endpoint_auth_methods_supported

        revocation_endpoint_auth_signing_alg_values_supported

        introspection_endpoint

        introspection_endpoint_auth_methods_supported

        introspection_endpoint_auth_signing_alg_values_supported

        code_challenge_methods_supported

        Additional authorization server metadata parameters MAY also be used.
        Some are defined by other specifications, such as OpenID Connect
        Discovery 1.0 [`OpenID.Discovery`_].

         .. _`RFC8414 section 2`: https://tools.ietf.org/html/rfc8414#section-2
         .. _`RFC6749#Authorization`: https://tools.ietf.org/html/rfc6749#section-3.1
         .. _`RFC6749#Token`: https://tools.ietf.org/html/rfc6749#section-3.2
         .. _`RFC7591`: https://tools.ietf.org/html/rfc7591
         .. _`OpenID.Discovery`: https://openid.net/specs/openid-connect-discovery-1_0.html
        """
