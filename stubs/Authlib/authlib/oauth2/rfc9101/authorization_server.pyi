from _typeshed import Incomplete

from ..rfc6749 import AuthorizationServer, ClientMixin
from ..rfc6749.requests import OAuth2Request

class JWTAuthenticationRequest:
    """Authorization server extension implementing the support
    for JWT secured authentication request, as defined in :rfc:`RFC9101 <9101>`.

    :param support_request: Whether to enable support for the ``request`` parameter.
    :param support_request_uri: Whether to enable support for the ``request_uri`` parameter.

    This extension is intended to be inherited and registered into the authorization server::

        class JWTAuthenticationRequest(rfc9101.JWTAuthenticationRequest):
            def resolve_client_public_key(self, client: ClientMixin):
                return get_jwks_for_client(client)

            def get_request_object(self, request_uri: str):
                try:
                    return requests.get(request_uri).text
                except requests.Exception:
                    return None

            def get_server_metadata(self):
                return {
                    "issuer": ...,
                    "authorization_endpoint": ...,
                    "require_signed_request_object": ...,
                }

            def get_client_require_signed_request_object(self, client: ClientMixin):
                return client.require_signed_request_object


        authorization_server.register_extension(JWTAuthenticationRequest())
    """

    support_request: bool
    support_request_uri: bool
    def __init__(self, support_request: bool = True, support_request_uri: bool = True) -> None: ...
    def __call__(self, authorization_server: AuthorizationServer) -> None: ...
    def parse_authorization_request(self, authorization_server: AuthorizationServer, request: OAuth2Request) -> None: ...
    def get_request_object(self, request_uri: str):
        """Download the request object at ``request_uri``.

        This method must be implemented if the ``request_uri`` parameter is supported::

            class JWTAuthenticationRequest(rfc9101.JWTAuthenticationRequest):
                def get_request_object(self, request_uri: str):
                    try:
                        return requests.get(request_uri).text
                    except requests.Exception:
                        return None
        """

    def resolve_client_public_keys(self, client: ClientMixin):
        """Resolve the client public key for verifying the JWT signature.
        A client may have many public keys, in this case, we can retrieve it
        via ``kid`` value in headers. Developers MUST implement this method::

            class JWTAuthenticationRequest(rfc9101.JWTAuthenticationRequest):
                def resolve_client_public_key(self, client):
                    if client.jwks_uri:
                        return requests.get(client.jwks_uri).json

                    return client.jwks
        """

    def get_server_metadata(self) -> dict[str, Incomplete]:
        """Return server metadata which includes supported grant types,
        response types and etc.

        When the ``require_signed_request_object`` claim is :data:`True`,
        all clients require that authorization requests
        use request objects, and an error will be returned when the authorization
        request payload is passed in the request body or query string::

            class JWTAuthenticationRequest(rfc9101.JWTAuthenticationRequest):
                def get_server_metadata(self):
                    return {
                        "issuer": ...,
                        "authorization_endpoint": ...,
                        "require_signed_request_object": ...,
                    }

        """

    def get_client_require_signed_request_object(self, client: ClientMixin) -> bool:
        """Return the 'require_signed_request_object' client metadata.

        When :data:`True`, the client requires that authorization requests
        use request objects, and an error will be returned when the authorization
        request payload is passed in the request body or query string::

           class JWTAuthenticationRequest(rfc9101.JWTAuthenticationRequest):
               def get_client_require_signed_request_object(self, client):
                   return client.require_signed_request_object

        If not implemented, the value is considered as :data:`False`.
        """
