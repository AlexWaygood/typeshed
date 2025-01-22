from _typeshed.wsgi import ErrorStream, StartResponse, WSGIApplication, WSGIEnvironment
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import TypeVar, overload

from .handlers import SimpleHandler

__all__ = ["WSGIServer", "WSGIRequestHandler", "demo_app", "make_server"]

server_version: str  # undocumented
sys_version: str  # undocumented
software_version: str  # undocumented

class ServerHandler(SimpleHandler):  # undocumented
    server_software: str

class WSGIServer(HTTPServer):
    application: WSGIApplication | None
    base_environ: WSGIEnvironment  # only available after call to setup_environ()
    def setup_environ(self) -> None: ...
    def get_app(self) -> WSGIApplication | None: ...
    def set_app(self, application: WSGIApplication | None) -> None: ...

class WSGIRequestHandler(BaseHTTPRequestHandler):
    server_version: str
    def get_environ(self) -> WSGIEnvironment: ...
    def get_stderr(self) -> ErrorStream: ...

def demo_app(environ: WSGIEnvironment, start_response: StartResponse) -> list[bytes]: ...

_S = TypeVar("_S", bound=WSGIServer)

@overload
def make_server(host: str, port: int, app: WSGIApplication, *, handler_class: type[WSGIRequestHandler] = ...) -> WSGIServer: ...
@overload
def make_server[_S: WSGIServer](
    host: str, port: int, app: WSGIApplication, server_class: type[_S], handler_class: type[WSGIRequestHandler] = ...
) -> _S: ...
