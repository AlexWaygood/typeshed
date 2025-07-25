from _typeshed import Incomplete
from typing import Final

class ClientRegistrationEndpoint:
    """The client registration endpoint is an OAuth 2.0 endpoint designed to
    allow a client to be registered with the authorization server.
    """

    ENDPOINT_NAME: Final = "client_registration"
    software_statement_alg_values_supported: Incomplete
    server: Incomplete
    claims_classes: list[type[Incomplete]]
    def __init__(self, server=None, claims_classes: list[type[Incomplete]] | None = None) -> None: ...
    def __call__(self, request) -> dict[Incomplete, Incomplete]: ...
    def create_registration_response(self, request): ...
    def extract_client_metadata(self, request): ...
    def extract_software_statement(self, software_statement, request): ...
    def generate_client_info(self): ...
    def generate_client_registration_info(self, client, request) -> None:
        """Generate ```registration_client_uri`` and ``registration_access_token``
        for RFC7592. This method returns ``None`` by default. Developers MAY rewrite
        this method to return registration information.
        """

    def create_endpoint_request(self, request): ...
    def generate_client_id(self):
        """Generate ``client_id`` value. Developers MAY rewrite this method
        to use their own way to generate ``client_id``.
        """

    def generate_client_secret(self):
        """Generate ``client_secret`` value. Developers MAY rewrite this method
        to use their own way to generate ``client_secret``.
        """

    def get_server_metadata(self) -> None:
        """Return server metadata which includes supported grant types,
        response types and etc.
        """

    def authenticate_token(self, request) -> None:
        """Authenticate current credential who is requesting to register a client.
        Developers MUST implement this method in subclass::

            def authenticate_token(self, request):
                auth = request.headers.get("Authorization")
                return get_token_by_auth(auth)

        :return: token instance
        """

    def resolve_public_key(self, request) -> None:
        """Resolve a public key for decoding ``software_statement``. If
        ``enable_software_statement=True``, developers MUST implement this
        method in subclass::

            def resolve_public_key(self, request):
                return get_public_key_from_user(request.credential)

        :return: JWK or Key string
        """

    def save_client(self, client_info, client_metadata, request) -> None:
        """Save client into database. Developers MUST implement this method
        in subclass::

            def save_client(self, client_info, client_metadata, request):
                client = OAuthClient(
                    client_id=client_info['client_id'],
                    client_secret=client_info['client_secret'],
                    ...
                )
                client.save()
                return client
        """
