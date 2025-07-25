from _typeshed import Incomplete
from logging import Logger
from typing import TypedDict
from typing_extensions import TypeAlias

import requests
from oauthlib.oauth1 import Client

from . import OAuth1

# should be dict[str, str] but could look different
_ParsedToken: TypeAlias = dict[str, Incomplete]

class _TokenDict(TypedDict, total=False):
    oauth_token: Incomplete  # oauthlib.oauth1.Client.resource_owner_key
    oauth_token_secret: Incomplete  # oauthlib.oauth1.Client.resource_token_secret
    oauth_verifier: Incomplete  # oauthlib.oauth1.Client.oauth_verifier

log: Logger

def urldecode(body):
    """Parse query or json to python dictionary"""

class TokenRequestDenied(ValueError):
    response: requests.Response
    def __init__(self, message: str, response: requests.Response) -> None: ...
    @property
    def status_code(self) -> int:
        """For backwards-compatibility purposes"""

class TokenMissing(ValueError):
    response: requests.Response
    def __init__(self, message: str, response: requests.Response) -> None: ...

class VerifierMissing(ValueError): ...

class OAuth1Session(requests.Session):
    """Request signing and convenience methods for the oauth dance.

    What is the difference between OAuth1Session and OAuth1?

    OAuth1Session actually uses OAuth1 internally and its purpose is to assist
    in the OAuth workflow through convenience methods to prepare authorization
    URLs and parse the various token and redirection responses. It also provide
    rudimentary validation of responses.

    An example of the OAuth workflow using a basic CLI app and Twitter.

    >>> # Credentials obtained during the registration.
    >>> client_key = 'client key'
    >>> client_secret = 'secret'
    >>> callback_uri = 'https://127.0.0.1/callback'
    >>>
    >>> # Endpoints found in the OAuth provider API documentation
    >>> request_token_url = 'https://api.twitter.com/oauth/request_token'
    >>> authorization_url = 'https://api.twitter.com/oauth/authorize'
    >>> access_token_url = 'https://api.twitter.com/oauth/access_token'
    >>>
    >>> oauth_session = OAuth1Session(client_key,client_secret=client_secret, callback_uri=callback_uri)
    >>>
    >>> # First step, fetch the request token.
    >>> oauth_session.fetch_request_token(request_token_url)
    {
        'oauth_token': 'kjerht2309u',
        'oauth_token_secret': 'lsdajfh923874',
    }
    >>>
    >>> # Second step. Follow this link and authorize
    >>> oauth_session.authorization_url(authorization_url)
    'https://api.twitter.com/oauth/authorize?oauth_token=sdf0o9823sjdfsdf&oauth_callback=https%3A%2F%2F127.0.0.1%2Fcallback'
    >>>
    >>> # Third step. Fetch the access token
    >>> redirect_response = input('Paste the full redirect URL here.')
    >>> oauth_session.parse_authorization_response(redirect_response)
    {
        'oauth_token: 'kjerht2309u',
        'oauth_token_secret: 'lsdajfh923874',
        'oauth_verifier: 'w34o8967345',
    }
    >>> oauth_session.fetch_access_token(access_token_url)
    {
        'oauth_token': 'sdf0o9823sjdfsdf',
        'oauth_token_secret': '2kjshdfp92i34asdasd',
    }
    >>> # Done. You can now make OAuth requests.
    >>> status_url = 'http://api.twitter.com/1/statuses/update.json'
    >>> new_status = {'status':  'hello world!'}
    >>> oauth_session.post(status_url, data=new_status)
    <Response [200]>
    """

    auth: OAuth1
    def __init__(
        self,
        client_key,
        client_secret=None,
        resource_owner_key=None,
        resource_owner_secret=None,
        callback_uri=None,
        signature_method="HMAC-SHA1",
        signature_type="AUTH_HEADER",
        rsa_key=None,
        verifier=None,
        client_class: type[Client] | None = None,
        force_include_body: bool = False,
        *,
        encoding: str = "utf-8",
        nonce=None,
        timestamp=None,
    ) -> None:
        """Construct the OAuth 1 session.

        :param client_key: A client specific identifier.
        :param client_secret: A client specific secret used to create HMAC and
                              plaintext signatures.
        :param resource_owner_key: A resource owner key, also referred to as
                                   request token or access token depending on
                                   when in the workflow it is used.
        :param resource_owner_secret: A resource owner secret obtained with
                                      either a request or access token. Often
                                      referred to as token secret.
        :param callback_uri: The URL the user is redirect back to after
                             authorization.
        :param signature_method: Signature methods determine how the OAuth
                                 signature is created. The three options are
                                 oauthlib.oauth1.SIGNATURE_HMAC (default),
                                 oauthlib.oauth1.SIGNATURE_RSA and
                                 oauthlib.oauth1.SIGNATURE_PLAIN.
        :param signature_type: Signature type decides where the OAuth
                               parameters are added. Either in the
                               Authorization header (default) or to the URL
                               query parameters or the request body. Defined as
                               oauthlib.oauth1.SIGNATURE_TYPE_AUTH_HEADER,
                               oauthlib.oauth1.SIGNATURE_TYPE_QUERY and
                               oauthlib.oauth1.SIGNATURE_TYPE_BODY
                               respectively.
        :param rsa_key: The private RSA key as a string. Can only be used with
                        signature_method=oauthlib.oauth1.SIGNATURE_RSA.
        :param verifier: A verifier string to prove authorization was granted.
        :param client_class: A subclass of `oauthlib.oauth1.Client` to use with
                             `requests_oauthlib.OAuth1` instead of the default
        :param force_include_body: Always include the request body in the
                                   signature creation.
        :param **kwargs: Additional keyword arguments passed to `OAuth1`
        """

    @property
    def token(self) -> _TokenDict: ...
    @token.setter
    def token(self, value: _TokenDict) -> None: ...
    @property
    def authorized(self) -> bool:
        """Boolean that indicates whether this session has an OAuth token
        or not. If `self.authorized` is True, you can reasonably expect
        OAuth-protected requests to the resource to succeed. If
        `self.authorized` is False, you need the user to go through the OAuth
        authentication dance before OAuth-protected requests to the resource
        will succeed.
        """

    def authorization_url(self, url: str, request_token=None, **kwargs) -> str:
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

        An example using a registered default callback URI.

        >>> request_token_url = 'https://api.twitter.com/oauth/request_token'
        >>> authorization_url = 'https://api.twitter.com/oauth/authorize'
        >>> oauth_session = OAuth1Session('client-key', client_secret='secret')
        >>> oauth_session.fetch_request_token(request_token_url)
        {
            'oauth_token': 'sdf0o9823sjdfsdf',
            'oauth_token_secret': '2kjshdfp92i34asdasd',
        }
        >>> oauth_session.authorization_url(authorization_url)
        'https://api.twitter.com/oauth/authorize?oauth_token=sdf0o9823sjdfsdf'
        >>> oauth_session.authorization_url(authorization_url, foo='bar')
        'https://api.twitter.com/oauth/authorize?oauth_token=sdf0o9823sjdfsdf&foo=bar'

        An example using an explicit callback URI.

        >>> request_token_url = 'https://api.twitter.com/oauth/request_token'
        >>> authorization_url = 'https://api.twitter.com/oauth/authorize'
        >>> oauth_session = OAuth1Session('client-key', client_secret='secret', callback_uri='https://127.0.0.1/callback')
        >>> oauth_session.fetch_request_token(request_token_url)
        {
            'oauth_token': 'sdf0o9823sjdfsdf',
            'oauth_token_secret': '2kjshdfp92i34asdasd',
        }
        >>> oauth_session.authorization_url(authorization_url)
        'https://api.twitter.com/oauth/authorize?oauth_token=sdf0o9823sjdfsdf&oauth_callback=https%3A%2F%2F127.0.0.1%2Fcallback'
        """

    def fetch_request_token(self, url: str, realm=None, **request_kwargs) -> _ParsedToken:
        """Fetch a request token.

        This is the first step in the OAuth 1 workflow. A request token is
        obtained by making a signed post request to url. The token is then
        parsed from the application/x-www-form-urlencoded response and ready
        to be used to construct an authorization url.

        :param url: The request token endpoint URL.
        :param realm: A list of realms to request access to.
        :param request_kwargs: Optional arguments passed to ''post''
            function in ''requests.Session''
        :returns: The response in dict format.

        Note that a previously set callback_uri will be reset for your
        convenience, or else signature creation will be incorrect on
        consecutive requests.

        >>> request_token_url = 'https://api.twitter.com/oauth/request_token'
        >>> oauth_session = OAuth1Session('client-key', client_secret='secret')
        >>> oauth_session.fetch_request_token(request_token_url)
        {
            'oauth_token': 'sdf0o9823sjdfsdf',
            'oauth_token_secret': '2kjshdfp92i34asdasd',
        }
        """

    def fetch_access_token(self, url: str, verifier=None, **request_kwargs) -> _ParsedToken:
        """Fetch an access token.

        This is the final step in the OAuth 1 workflow. An access token is
        obtained using all previously obtained credentials, including the
        verifier from the authorization step.

        Note that a previously set verifier will be reset for your
        convenience, or else signature creation will be incorrect on
        consecutive requests.

        >>> access_token_url = 'https://api.twitter.com/oauth/access_token'
        >>> redirect_response = 'https://127.0.0.1/callback?oauth_token=kjerht2309uf&oauth_token_secret=lsdajfh923874&oauth_verifier=w34o8967345'
        >>> oauth_session = OAuth1Session('client-key', client_secret='secret')
        >>> oauth_session.parse_authorization_response(redirect_response)
        {
            'oauth_token: 'kjerht2309u',
            'oauth_token_secret: 'lsdajfh923874',
            'oauth_verifier: 'w34o8967345',
        }
        >>> oauth_session.fetch_access_token(access_token_url)
        {
            'oauth_token': 'sdf0o9823sjdfsdf',
            'oauth_token_secret': '2kjshdfp92i34asdasd',
        }
        """

    def parse_authorization_response(self, url: str) -> _ParsedToken:
        """Extract parameters from the post authorization redirect response URL.

        :param url: The full URL that resulted from the user being redirected
                    back from the OAuth provider to you, the client.
        :returns: A dict of parameters extracted from the URL.

        >>> redirect_response = 'https://127.0.0.1/callback?oauth_token=kjerht2309uf&oauth_token_secret=lsdajfh923874&oauth_verifier=w34o8967345'
        >>> oauth_session = OAuth1Session('client-key', client_secret='secret')
        >>> oauth_session.parse_authorization_response(redirect_response)
        {
            'oauth_token: 'kjerht2309u',
            'oauth_token_secret: 'lsdajfh923874',
            'oauth_verifier: 'w34o8967345',
        }
        """

    def rebuild_auth(self, prepared_request: requests.PreparedRequest, response: requests.Response) -> None:
        """
        When being redirected we should always strip Authorization
        header, since nonce may not be reused as per OAuth spec.
        """
