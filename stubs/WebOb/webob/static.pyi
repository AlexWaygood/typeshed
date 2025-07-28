from _typeshed import StrPath
from _typeshed.wsgi import WSGIApplication
from collections.abc import Iterator
from typing import IO, Any

from webob.dec import wsgify
from webob.request import Request
from webob.response import Response

__all__ = ["FileApp", "DirectoryApp"]

BLOCK_SIZE: int

class FileApp:
    """An application that will send the file at the given filename.

    Adds a mime type based on `mimetypes.guess_type()`.
    """

    filename: StrPath
    kw: dict[str, Any]
    def __init__(self, filename: StrPath, **kw: Any) -> None: ...
    @wsgify
    def __call__(self, req: Request) -> WSGIApplication:
        """Turns a request-taking, response-returning function into a WSGI
        app

        You can use this like::

            @wsgify
            def myfunc(req):
                return webob.Response('hey there')

        With that ``myfunc`` will be a WSGI application, callable like
        ``app_iter = myfunc(environ, start_response)``.  You can also call
        it like normal, e.g., ``resp = myfunc(req)``.  (You can also wrap
        methods, like ``def myfunc(self, req)``.)

        If you raise exceptions from :mod:`webob.exc` they will be turned
        into WSGI responses.

        There are also several parameters you can use to customize the
        decorator.  Most notably, you can use a :class:`webob.Request`
        subclass, like::

            class MyRequest(webob.Request):
                @property
                def is_local(self):
                    return self.remote_addr == '127.0.0.1'
            @wsgify(RequestClass=MyRequest)
            def myfunc(req):
                if req.is_local:
                    return Response('hi!')
                else:
                    raise webob.exc.HTTPForbidden

        Another customization you can add is to add `args` (positional
        arguments) or `kwargs` (of course, keyword arguments).  While
        generally not that useful, you can use this to create multiple
        WSGI apps from one function, like::

            import simplejson
            def serve_json(req, json_obj):
                return Response(json.dumps(json_obj),
                                content_type='application/json')

            serve_ob1 = wsgify(serve_json, args=(ob1,))
            serve_ob2 = wsgify(serve_json, args=(ob2,))

        You can return several things from a function:

        * A :class:`webob.Response` object (or subclass)
        * *Any* WSGI application
        * None, and then ``req.response`` will be used (a pre-instantiated
          Response object)
        * A string, which will be written to ``req.response`` and then that
          response will be used.
        * Raise an exception from :mod:`webob.exc`

        Also see :func:`wsgify.middleware` for a way to make middleware.

        You can also subclass this decorator; the most useful things to do
        in a subclass would be to change `RequestClass` or override
        `call_func` (e.g., to add ``req.urlvars`` as keyword arguments to
        the function).
        """

class FileIter:
    file: IO[bytes]
    def __init__(self, file: IO[bytes]) -> None: ...
    def app_iter_range(self, seek: int | None = None, limit: int | None = None, block_size: int | None = None) -> Iterator[bytes]:
        """Iter over the content of the file.

        You can set the `seek` parameter to read the file starting from a
        specific position.

        You can set the `limit` parameter to read the file up to specific
        position.

        Finally, you can change the number of bytes read at once by setting the
        `block_size` parameter.
        """
    __iter__ = app_iter_range

class DirectoryApp:
    """An application that serves up the files in a given directory.

    This will serve index files (by default ``index.html``), or set
    ``index_page=None`` to disable this.  If you set
    ``hide_index_with_redirect=True`` (it defaults to False) then
    requests to, e.g., ``/index.html`` will be redirected to ``/``.

    To customize `FileApp` instances creation (which is what actually
    serves the responses), override the `make_fileapp` method.
    """

    path: StrPath
    index_page: str
    hide_index_with_redirect: bool
    fileapp_kw: dict[str, Any]
    def __init__(
        self, path: StrPath, index_page: str = "index.html", hide_index_with_redirect: bool = False, **kw: Any
    ) -> None: ...
    def make_fileapp(self, path: StrPath) -> FileApp: ...
    @wsgify
    def __call__(self, req: Request) -> Response | FileApp:
        """Turns a request-taking, response-returning function into a WSGI
        app

        You can use this like::

            @wsgify
            def myfunc(req):
                return webob.Response('hey there')

        With that ``myfunc`` will be a WSGI application, callable like
        ``app_iter = myfunc(environ, start_response)``.  You can also call
        it like normal, e.g., ``resp = myfunc(req)``.  (You can also wrap
        methods, like ``def myfunc(self, req)``.)

        If you raise exceptions from :mod:`webob.exc` they will be turned
        into WSGI responses.

        There are also several parameters you can use to customize the
        decorator.  Most notably, you can use a :class:`webob.Request`
        subclass, like::

            class MyRequest(webob.Request):
                @property
                def is_local(self):
                    return self.remote_addr == '127.0.0.1'
            @wsgify(RequestClass=MyRequest)
            def myfunc(req):
                if req.is_local:
                    return Response('hi!')
                else:
                    raise webob.exc.HTTPForbidden

        Another customization you can add is to add `args` (positional
        arguments) or `kwargs` (of course, keyword arguments).  While
        generally not that useful, you can use this to create multiple
        WSGI apps from one function, like::

            import simplejson
            def serve_json(req, json_obj):
                return Response(json.dumps(json_obj),
                                content_type='application/json')

            serve_ob1 = wsgify(serve_json, args=(ob1,))
            serve_ob2 = wsgify(serve_json, args=(ob2,))

        You can return several things from a function:

        * A :class:`webob.Response` object (or subclass)
        * *Any* WSGI application
        * None, and then ``req.response`` will be used (a pre-instantiated
          Response object)
        * A string, which will be written to ``req.response`` and then that
          response will be used.
        * Raise an exception from :mod:`webob.exc`

        Also see :func:`wsgify.middleware` for a way to make middleware.

        You can also subclass this decorator; the most useful things to do
        in a subclass would be to change `RequestClass` or override
        `call_func` (e.g., to add ``req.urlvars`` as keyword arguments to
        the function).
        """

    def index(self, req: Request, path: StrPath) -> Response | FileApp: ...
