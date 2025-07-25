from _typeshed import Incomplete

from authlib.oauth1 import ClientAuth

class OAuth1Client:
    auth_class: type[ClientAuth] = ...
    session: Incomplete
    auth: Incomplete
    def __init__(
        self,
        session,
        client_id,
        client_secret=None,
        token=None,
        token_secret=None,
        redirect_uri=None,
        rsa_key=None,
        verifier=None,
        signature_method="HMAC-SHA1",
        signature_type="HEADER",
        force_include_body: bool = False,
        realm=None,
        **kwargs,
    ) -> None: ...
    @property
    def redirect_uri(self): ...
    @redirect_uri.setter
    def redirect_uri(self, uri) -> None: ...
    @property
    def token(self): ...
    @token.setter
    def token(self, token) -> None: ...
    def create_authorization_url(self, url, request_token=None, **kwargs):
        """Create an authorization URL by appending request_token and optional
        kwargs to url.

        This is the second step in the OAuth 1 workflow. The user should be
        redirected to this authorization URL, grant access to you, and then
        be redirected back to you. The redirection back can either be specified
        during client registration or by supplying a callback URI per request.

        :param url: The authorization endpoint URL.
        :param request_token: The previously obtained request token.
        :param kwargs: Optional parameters to append to the URL.
        :returns: The authorization URL with new parameters embedded.
        """

    def fetch_request_token(self, url, **kwargs):
        """Method for fetching an access token from the token endpoint.

        This is the first step in the OAuth 1 workflow. A request token is
        obtained by making a signed post request to url. The token is then
        parsed from the application/x-www-form-urlencoded response and ready
        to be used to construct an authorization url.

        :param url: Request Token endpoint.
        :param kwargs: Extra parameters to include for fetching token.
        :return: A Request Token dict.
        """

    def fetch_access_token(self, url, verifier=None, **kwargs):
        """Method for fetching an access token from the token endpoint.

        This is the final step in the OAuth 1 workflow. An access token is
        obtained using all previously obtained credentials, including the
        verifier from the authorization step.

        :param url: Access Token endpoint.
        :param verifier: A verifier string to prove authorization was granted.
        :param kwargs: Extra parameters to include for fetching access token.
        :return: A token dict.
        """

    def parse_authorization_response(self, url):
        """Extract parameters from the post authorization redirect
        response URL.

        :param url: The full URL that resulted from the user being redirected
                    back from the OAuth provider to you, the client.
        :returns: A dict of parameters extracted from the URL.
        """

    def parse_response_token(self, status_code, text): ...
    @staticmethod
    def handle_error(error_type, error_description) -> None: ...
    def __del__(self) -> None: ...
