from _typeshed.wsgi import StartResponse, WSGIEnvironment
from collections.abc import Iterable
from http.client import HTTPConnection, HTTPMessage, HTTPSConnection
from typing import ClassVar

__all__ = ["send_request_app", "SendRequest"]

class SendRequest:
    """
    Sends the request, as described by the environ, over actual HTTP.
    All controls about how it is sent are contained in the request
    environ itself.

    This connects to the server given in SERVER_NAME:SERVER_PORT, and
    sends the Host header in HTTP_HOST -- they do not have to match.
    You can send requests to servers despite what DNS says.

    Set ``environ['webob.client.timeout'] = 10`` to set the timeout on
    the request (to, for example, 10 seconds).

    Does not add X-Forwarded-For or other standard headers

    If you use ``send_request_app`` then simple ``httplib``
    connections will be used.
    """

    def __init__(self, HTTPConnection: type[HTTPConnection] = ..., HTTPSConnection: type[HTTPSConnection] = ...) -> None: ...
    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]: ...
    filtered_headers: ClassVar[tuple[str, ...]]
    def parse_headers(self, message: HTTPMessage) -> list[tuple[str, str]]:
        """
        Turn a Message object into a list of WSGI-style headers.
        """

send_request_app: SendRequest
