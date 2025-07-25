from _typeshed import Incomplete
from typing import Final

class ClientConfigurationEndpoint:
    ENDPOINT_NAME: Final = "client_configuration"
    server: Incomplete
    claims_classes: list[type[Incomplete]]
    def __init__(self, server=None, claims_classes: list[type[Incomplete]] | None = None) -> None: ...
    def __call__(self, request): ...
    def create_configuration_response(self, request): ...
    def create_endpoint_request(self, request): ...
    def create_read_client_response(self, client, request): ...
    def create_delete_client_response(self, client, request): ...
    def create_update_client_response(self, client, request): ...
    def extract_client_metadata(self, request): ...
    def introspect_client(self, client): ...
    def generate_client_registration_info(self, client, request) -> None:
        """Generate ```registration_client_uri`` and ``registration_access_token``
        for RFC7592. By default this method returns the values sent in the current
        request. Developers MUST rewrite this method to return different registration
        information.::

            def generate_client_registration_info(self, client, request):{
                access_token = request.headers['Authorization'].split(' ')[1]
                return {
                    'registration_client_uri': request.uri,
                    'registration_access_token': access_token,
                }

        :param client: the instance of OAuth client
        :param request: formatted request instance
        """

    def authenticate_token(self, request) -> None:
        """Authenticate current credential who is requesting to register a client.
        Developers MUST implement this method in subclass::

            def authenticate_token(self, request):
                auth = request.headers.get("Authorization")
                return get_token_by_auth(auth)

        :return: token instance
        """

    def authenticate_client(self, request) -> None:
        """Read a client from the request payload.
        Developers MUST implement this method in subclass::

            def authenticate_client(self, request):
                client_id = request.payload.data.get("client_id")
                return Client.get(client_id=client_id)

        :return: client instance
        """

    def revoke_access_token(self, token, request) -> None:
        """Revoke a token access in case an invalid client has been requested.
        Developers MUST implement this method in subclass::

            def revoke_access_token(self, token, request):
                token.revoked = True
                token.save()

        """

    def check_permission(self, client, request) -> None:
        """Checks whether the current client is allowed to be accessed, edited
        or deleted. Developers MUST implement it in subclass, e.g.::

            def check_permission(self, client, request):
                return client.editable

        :return: boolean
        """

    def delete_client(self, client, request) -> None:
        """Delete authorization code from database or cache. Developers MUST
        implement it in subclass, e.g.::

            def delete_client(self, client, request):
                client.delete()

        :param client: the instance of OAuth client
        :param request: formatted request instance
        """

    def update_client(self, client, client_metadata, request) -> None:
        """Update the client in the database. Developers MUST implement this method
        in subclass::

            def update_client(self, client, client_metadata, request):
                client.set_client_metadata(
                    {**client.client_metadata, **client_metadata}
                )
                client.save()
                return client

        :param client: the instance of OAuth client
        :param client_metadata: a dict of the client claims to update
        :param request: formatted request instance
        :return: client instance
        """

    def get_server_metadata(self) -> None:
        """Return server metadata which includes supported grant types,
        response types and etc.
        """
