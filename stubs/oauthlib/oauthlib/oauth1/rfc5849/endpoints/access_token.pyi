"""
oauthlib.oauth1.rfc5849.endpoints.access_token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of the access token provider logic of
OAuth 1.0 RFC 5849. It validates the correctness of access token requests,
creates and persists tokens as well as create the proper response to be
returned to the client.
"""

from logging import Logger

from .base import BaseEndpoint as BaseEndpoint

log: Logger

class AccessTokenEndpoint(BaseEndpoint):
    """An endpoint responsible for providing OAuth 1 access tokens.

    Typical use is to instantiate with a request validator and invoke the
    ``create_access_token_response`` from a view function. The tuple returned
    has all information necessary (body, status, headers) to quickly form
    and return a proper response. See :doc:`/oauth1/validator` for details on which
    validator methods to implement for this endpoint.
    """

    def create_access_token(self, request, credentials):
        """Create and save a new access token.

        Similar to OAuth 2, indication of granted scopes will be included as a
        space separated list in ``oauth_authorized_realms``.

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :returns: The token as an urlencoded string.
        """

    def create_access_token_response(self, uri, http_method: str = "GET", body=None, headers=None, credentials=None):
        """Create an access token response, with a new request token if valid.

        :param uri: The full URI of the token request.
        :param http_method: A valid HTTP verb, i.e. GET, POST, PUT, HEAD, etc.
        :param body: The request body as a string.
        :param headers: The request headers as a dict.
        :param credentials: A list of extra credentials to include in the token.
        :returns: A tuple of 3 elements.
                  1. A dict of headers to set on the response.
                  2. The response body as a string.
                  3. The response status code as an integer.

        An example of a valid request::

            >>> from your_validator import your_validator
            >>> from oauthlib.oauth1 import AccessTokenEndpoint
            >>> endpoint = AccessTokenEndpoint(your_validator)
            >>> h, b, s = endpoint.create_access_token_response(
            ...     'https://your.provider/access_token?foo=bar',
            ...     headers={
            ...         'Authorization': 'OAuth oauth_token=234lsdkf....'
            ...     },
            ...     credentials={
            ...         'my_specific': 'argument',
            ...     })
            >>> h
            {'Content-Type': 'application/x-www-form-urlencoded'}
            >>> b
            'oauth_token=lsdkfol23w54jlksdef&oauth_token_secret=qwe089234lkjsdf&oauth_authorized_realms=movies+pics&my_specific=argument'
            >>> s
            200

        An response to invalid request would have a different body and status::

            >>> b
            'error=invalid_request&description=missing+resource+owner+key'
            >>> s
            400

        The same goes for an an unauthorized request:

            >>> b
            ''
            >>> s
            401
        """

    def validate_access_token_request(self, request):
        """Validate an access token request.

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :raises: OAuth1Error if the request is invalid.
        :returns: A tuple of 2 elements.
                  1. The validation result (True or False).
                  2. The request object.
        """
