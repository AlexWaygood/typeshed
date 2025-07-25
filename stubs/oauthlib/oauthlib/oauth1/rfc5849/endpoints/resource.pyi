"""
oauthlib.oauth1.rfc5849.endpoints.resource
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of the resource protection provider logic of
OAuth 1.0 RFC 5849.
"""

from logging import Logger

from .base import BaseEndpoint as BaseEndpoint

log: Logger

class ResourceEndpoint(BaseEndpoint):
    """An endpoint responsible for protecting resources.

    Typical use is to instantiate with a request validator and invoke the
    ``validate_protected_resource_request`` in a decorator around a view
    function. If the request is valid, invoke and return the response of the
    view. If invalid create and return an error response directly from the
    decorator.

    See :doc:`/oauth1/validator` for details on which validator methods to implement
    for this endpoint.

    An example decorator::

        from functools import wraps
        from your_validator import your_validator
        from oauthlib.oauth1 import ResourceEndpoint
        endpoint = ResourceEndpoint(your_validator)

        def require_oauth(realms=None):
            def decorator(f):
                @wraps(f)
                def wrapper(request, *args, **kwargs):
                    v, r = provider.validate_protected_resource_request(
                            request.url,
                            http_method=request.method,
                            body=request.data,
                            headers=request.headers,
                            realms=realms or [])
                    if v:
                        return f(*args, **kwargs)
                    else:
                        return abort(403)
    """

    def validate_protected_resource_request(self, uri, http_method: str = "GET", body=None, headers=None, realms=None):
        """Create a request token response, with a new request token if valid.

        :param uri: The full URI of the token request.
        :param http_method: A valid HTTP verb, i.e. GET, POST, PUT, HEAD, etc.
        :param body: The request body as a string.
        :param headers: The request headers as a dict.
        :param realms: A list of realms the resource is protected under.
                       This will be supplied to the ``validate_realms``
                       method of the request validator.
        :returns: A tuple of 2 elements.
                  1. True if valid, False otherwise.
                  2. An oauthlib.common.Request object.
        """
