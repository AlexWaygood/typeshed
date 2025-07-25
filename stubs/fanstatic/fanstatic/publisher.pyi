from _typeshed import StrOrBytesPath
from _typeshed.wsgi import StartResponse, WSGIApplication, WSGIEnvironment
from collections.abc import Iterable
from typing import IO, Any, Literal

from fanstatic.core import Library
from fanstatic.registry import LibraryRegistry
from webob import Request, Response
from webob.dec import wsgify
from webob.static import DirectoryApp, FileApp

MINUTE_IN_SECONDS: Literal[60]
HOUR_IN_SECONDS: Literal[3600]
DAY_IN_SECONDS: Literal[86400]
YEAR_IN_SECONDS: int
FOREVER: int

class BundleApp(FileApp):
    filenames: list[str]
    def __init__(self, rootpath: str, bundle: IO[bytes], filenames: Iterable[StrOrBytesPath]) -> None: ...
    @wsgify
    def __call__(self, req: Request) -> Response:
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

class LibraryPublisher(DirectoryApp):
    """Fanstatic directory publisher WSGI application.

    This WSGI application serves a directory of static resources to
    the web.

    This WSGI component is used automatically by the
    :py:func:`Fanstatic` WSGI framework component, but can also be
    used independently if you need more control.

    :param library: The fanstatic library instance.
    """

    ignores: list[str]
    library: Library
    cached_apps: dict[str, FileApp]
    def __init__(self, library: Library) -> None: ...
    @wsgify
    def __call__(self, req: Request) -> Response:
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

class Publisher:
    """Fanstatic publisher WSGI application.

    This WSGI application serves Fanstatic :py:class:`Library`
    instances. Libraries are published as
    ``<library_name>/<optional_version>/path/to/resource.js``.

    All static resources contained in the libraries will be published
    to the web. If a step prefixed with ``:version:`` appears in the URL,
    this will be automatically skipped, and the HTTP response will
    indicate the resource can be cached forever.

    This WSGI component is used automatically by the
    :py:func:`Fanstatic` WSGI framework component, but can also be
    used independently if you need more control.

    :param registry: an instance of
      :py:class:`LibraryRegistry` with those resource libraries that
      should be published.
    """

    registry: LibraryRegistry
    directory_publishers: dict[str, LibraryPublisher]
    def __init__(self, registry: LibraryRegistry) -> None: ...
    @wsgify
    def __call__(self, request: Request) -> Response:
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

class Delegator:
    """Fanstatic delegator WSGI framework component.

    This WSGI component recognizes URLs that point to Fanstatic
    libraries, and delegates them to the :py:class:`Publisher` WSGI
    application.

    In order to recognize such URLs it looks for occurrences of the
    ``publisher_signature`` parameter as a URL step. By default
    it looks for ``/fanstatic/``.

    This WSGI component is used automatically by the
    :py:func:`Fanstatic` WSGI framework component, but can also be
    used independently if you need more control.

    :param app: The WSGI app to wrap with the delegator.

    :param publisher: An instance of the :py:class:`Publisher` component.

    :param publisher_signature: Optional argument to define the
      signature of the publisher in a URL. The default is ``fanstatic``.
    """

    app: WSGIApplication
    publisher: Publisher
    publisher_signature: str
    trigger: str
    def __init__(self, app: WSGIApplication, publisher: Publisher, publisher_signature: str = ...) -> None: ...
    def is_resource(self, request: Request) -> bool: ...
    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]: ...

def make_publisher(global_config: Any) -> Publisher: ...
