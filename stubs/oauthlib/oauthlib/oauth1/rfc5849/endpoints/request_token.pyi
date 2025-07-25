"""
oauthlib.oauth1.rfc5849.endpoints.request_token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of the request token provider logic of
OAuth 1.0 RFC 5849. It validates the correctness of request token requests,
creates and persists tokens as well as create the proper response to be
returned to the client.
"""

from logging import Logger

from .base import BaseEndpoint as BaseEndpoint

log: Logger

class RequestTokenEndpoint(BaseEndpoint):
    """An endpoint responsible for providing OAuth 1 request tokens.

    Typical use is to instantiate with a request validator and invoke the
    ``create_request_token_response`` from a view function. The tuple returned
    has all information necessary (body, status, headers) to quickly form
    and return a proper response. See :doc:`/oauth1/validator` for details on which
    validator methods to implement for this endpoint.
    """

    def create_request_token(self, request, credentials):
        """Create and save a new request token.

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :param credentials: A dict of extra token credentials.
        :returns: The token as an urlencoded string.
        """

    def create_request_token_response(self, uri, http_method: str = "GET", body=None, headers=None, credentials=None):
        """Create a request token response, with a new request token if valid.

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
            >>> from oauthlib.oauth1 import RequestTokenEndpoint
            >>> endpoint = RequestTokenEndpoint(your_validator)
            >>> h, b, s = endpoint.create_request_token_response(
            ...     'https://your.provider/request_token?foo=bar',
            ...     headers={
            ...         'Authorization': 'OAuth realm=movies user, oauth_....'
            ...     },
            ...     credentials={
            ...         'my_specific': 'argument',
            ...     })
            >>> h
            {'Content-Type': 'application/x-www-form-urlencoded'}
            >>> b
            'oauth_token=lsdkfol23w54jlksdef&oauth_token_secret=qwe089234lkjsdf&oauth_callback_confirmed=true&my_specific=argument'
            >>> s
            200

        An response to invalid request would have a different body and status::

            >>> b
            'error=invalid_request&description=missing+callback+uri'
            >>> s
            400

        The same goes for an an unauthorized request:

            >>> b
            ''
            >>> s
            401
        """

    def validate_request_token_request(self, request):
        """Validate a request token request.

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :raises: OAuth1Error if the request is invalid.
        :returns: A tuple of 2 elements.
                  1. The validation result (True or False).
                  2. The request object.
        """
