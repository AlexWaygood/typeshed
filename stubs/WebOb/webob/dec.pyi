"""
Decorators to wrap functions to make them WSGI applications.

The main decorator :class:`wsgify` turns a function into a WSGI
application (while also allowing normal calling of the method with an
instantiated request).
"""

from _typeshed.wsgi import StartResponse, WSGIApplication, WSGIEnvironment
from collections.abc import Callable, Iterable, Mapping
from typing import Any, Generic, overload
from typing_extensions import Concatenate, Never, ParamSpec, Self, TypeAlias, TypeVar

from webob.request import BaseRequest, Request
from webob.response import Response

__all__ = ["wsgify"]

_AnyResponse: TypeAlias = Response | WSGIApplication | str | None
_S = TypeVar("_S")
_AppT = TypeVar("_AppT", bound=WSGIApplication)
_AppT_contra = TypeVar("_AppT_contra", bound=WSGIApplication, contravariant=True)
_RequestT = TypeVar("_RequestT", bound=BaseRequest)
_RequestT_contra = TypeVar("_RequestT_contra", bound=BaseRequest, default=Request, contravariant=True)
_P = ParamSpec("_P")
_P2 = ParamSpec("_P2")

_RequestHandlerCallable: TypeAlias = Callable[Concatenate[_RequestT, _P], _AnyResponse]
_RequestHandlerMethod: TypeAlias = Callable[Concatenate[Any, _RequestT, _P], _AnyResponse]
_MiddlewareCallable: TypeAlias = Callable[Concatenate[_RequestT, _AppT, _P], _AnyResponse]
_MiddlewareMethod: TypeAlias = Callable[Concatenate[Any, _RequestT, _AppT, _P], _AnyResponse]
_RequestHandler: TypeAlias = _RequestHandlerCallable[_RequestT, _P] | _RequestHandlerMethod[_RequestT, _P]
_Middleware: TypeAlias = _MiddlewareCallable[_RequestT, _AppT, _P] | _MiddlewareMethod[_RequestT, _AppT, _P]

class wsgify(Generic[_P, _RequestT_contra]):
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

    RequestClass: type[_RequestT_contra]
    func: _RequestHandler[_RequestT_contra, _P] | None
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    middleware_wraps: WSGIApplication | None
    # NOTE: We disallow passing args/kwargs using this direct API, because
    #       we can't really make it work as a decorator this way, these
    #       arguments should only really be used indirectly through the
    #       middleware decorator, where we can be more type safe
    @overload
    def __init__(
        self: wsgify[[], Request],
        func: _RequestHandler[Request, []] | None = None,
        RequestClass: None = None,
        args: tuple[()] = (),
        kwargs: None = None,
        middleware_wraps: None = None,
    ) -> None: ...
    @overload
    def __init__(
        self: wsgify[[], _RequestT_contra],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        func: _RequestHandler[_RequestT_contra, []] | None,
        RequestClass: type[_RequestT_contra],
        args: tuple[()] = (),
        kwargs: None = None,
        middleware_wraps: None = None,
    ) -> None: ...
    @overload
    def __init__(
        self: wsgify[[], _RequestT_contra],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        func: _RequestHandler[_RequestT_contra, []] | None = None,
        *,
        RequestClass: type[_RequestT_contra],
        args: tuple[()] = (),
        kwargs: None = None,
        middleware_wraps: None = None,
    ) -> None: ...
    @overload
    def __init__(
        self: wsgify[[_AppT_contra], Request],
        func: _Middleware[Request, _AppT_contra, []] | None = None,
        RequestClass: None = None,
        args: tuple[()] = (),
        kwargs: None = None,
        *,
        middleware_wraps: _AppT_contra,
    ) -> None: ...
    @overload
    def __init__(
        self: wsgify[[_AppT_contra], _RequestT_contra],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        func: _Middleware[_RequestT_contra, _AppT_contra, []] | None,
        RequestClass: type[_RequestT_contra],
        args: tuple[()] = (),
        kwargs: None = None,
        *,
        middleware_wraps: _AppT_contra,
    ) -> None: ...
    @overload
    def __init__(
        self: wsgify[[_AppT_contra], _RequestT_contra],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        func: _Middleware[_RequestT_contra, _AppT_contra, []] | None = None,
        *,
        RequestClass: type[_RequestT_contra],
        args: tuple[()] = (),
        kwargs: None = None,
        middleware_wraps: _AppT_contra,
    ) -> None: ...
    @overload
    def __get__(self, obj: None, type: type[_S]) -> _unbound_wsgify[_P, _S, _RequestT_contra]: ...
    @overload
    def __get__(self, obj: object, type: type | None = None) -> Self: ...
    @overload
    def __call__(self, env: WSGIEnvironment, /, start_response: StartResponse) -> Iterable[bytes]:
        """Call this as a WSGI application or with a request"""

    @overload
    def __call__(self, func: _RequestHandler[_RequestT_contra, _P], /) -> Self: ...
    @overload
    def __call__(self, req: _RequestT_contra) -> _AnyResponse: ...
    @overload
    def __call__(self, req: _RequestT_contra, *args: _P.args, **kw: _P.kwargs) -> _AnyResponse: ...
    def get(self, url: str, **kw: Any) -> _AnyResponse:
        """Run a GET request on this application, returning a Response.

        This creates a request object using the given URL, and any
        other keyword arguments are set on the request object (e.g.,
        ``last_modified=datetime.now()``).

        ::

            resp = myapp.get('/article?id=10')
        """

    def post(
        self, url: str, POST: str | bytes | Mapping[Any, Any] | Mapping[Any, list[Any] | tuple[Any, ...]] | None = None, **kw: Any
    ) -> _AnyResponse:
        """Run a POST request on this application, returning a Response.

        The second argument (`POST`) can be the request body (a
        string), or a dictionary or list of two-tuples, that give the
        POST body.

        ::

            resp = myapp.post('/article/new',
                              dict(title='My Day',
                                   content='I ate a sandwich'))
        """

    def request(self, url: str, **kw: Any) -> _AnyResponse:
        """Run a request on this application, returning a Response.

        This can be used for DELETE, PUT, etc requests.  E.g.::

            resp = myapp.request('/article/1', method='PUT', body='New article')
        """

    def call_func(self, req: _RequestT_contra, *args: _P.args, **kwargs: _P.kwargs) -> _AnyResponse:
        """Call the wrapped function; override this in a subclass to
        change how the function is called.
        """
    # technically this could bind different type vars, but we disallow it for safety
    def clone(self, func: _RequestHandler[_RequestT_contra, _P] | None = None, **kw: Never) -> Self:
        """Creates a copy/clone of this object, but with some
        parameters rebound
        """

    @property
    def undecorated(self) -> _RequestHandler[_RequestT_contra, _P] | None: ...
    @overload
    @classmethod
    def middleware(
        cls, middle_func: None = None, app: None | _AppT = None, *_: _P.args, **kw: _P.kwargs
    ) -> _UnboundMiddleware[_P, _AppT, Any]:
        """Creates middleware

        Use this like::

            @wsgify.middleware
            def restrict_ip(req, app, ips):
                if req.remote_addr not in ips:
                    raise webob.exc.HTTPForbidden('Bad IP: %s' % req.remote_addr)
                return app

            @wsgify
            def app(req):
                return 'hi'

            wrapped = restrict_ip(app, ips=['127.0.0.1'])

        Or as a decorator::

            @restrict_ip(ips=['127.0.0.1'])
            @wsgify
            def wrapped_app(req):
                return 'hi'

        Or if you want to write output-rewriting middleware::

            @wsgify.middleware
            def all_caps(req, app):
                resp = req.get_response(app)
                resp.body = resp.body.upper()
                return resp

            wrapped = all_caps(app)

        Note that you must call ``req.get_response(app)`` to get a WebOb
        response object.  If you are not modifying the output, you can just
        return the app.

        As you can see, this method doesn't actually create an application, but
        creates "middleware" that can be bound to an application, along with
        "configuration" (that is, any other keyword arguments you pass when
        binding the application).

        """

    @overload
    @classmethod
    def middleware(
        cls, middle_func: _MiddlewareCallable[_RequestT, _AppT, _P2], app: None = None
    ) -> _MiddlewareFactory[_P2, _AppT, _RequestT]: ...
    @overload
    @classmethod
    def middleware(
        cls, middle_func: _MiddlewareMethod[_RequestT, _AppT, _P2], app: None = None
    ) -> _MiddlewareFactory[_P2, _AppT, _RequestT]: ...
    @overload
    @classmethod
    def middleware(
        cls, middle_func: _MiddlewareMethod[_RequestT, _AppT, _P2], app: None = None, *_: _P2.args, **kw: _P2.kwargs
    ) -> _MiddlewareFactory[_P2, _AppT, _RequestT]: ...
    @overload
    @classmethod
    def middleware(
        cls, middle_func: _MiddlewareMethod[_RequestT, _AppT, _P2], app: _AppT
    ) -> type[wsgify[Concatenate[_AppT, _P2], _RequestT]]: ...
    @overload
    @classmethod
    def middleware(
        cls, middle_func: _MiddlewareMethod[_RequestT, _AppT, _P2], app: _AppT, *_: _P2.args, **kw: _P2.kwargs
    ) -> type[wsgify[Concatenate[_AppT, _P2], _RequestT]]: ...

class _unbound_wsgify(wsgify[_P, _RequestT_contra], Generic[_P, _S, _RequestT_contra]):
    @overload  # type: ignore[override]
    def __call__(self, __self: _S, env: WSGIEnvironment, /, start_response: StartResponse) -> Iterable[bytes]: ...
    @overload
    def __call__(self, __self: _S, func: _RequestHandler[_RequestT_contra, _P], /) -> Self: ...
    @overload
    def __call__(self, __self: _S, /, req: _RequestT_contra) -> _AnyResponse: ...
    @overload
    def __call__(self, __self: _S, /, req: _RequestT_contra, *args: _P.args, **kw: _P.kwargs) -> _AnyResponse: ...

class _UnboundMiddleware(Generic[_P, _AppT_contra, _RequestT_contra]):
    """A `wsgify.middleware` invocation that has not yet wrapped a
    middleware function; the intermediate object when you do
    something like ``@wsgify.middleware(RequestClass=Foo)``
    """

    wrapper_class: type[wsgify[Concatenate[_AppT_contra, _P], _RequestT_contra]]
    app: _AppT_contra | None
    kw: dict[str, Any]
    def __init__(
        self,
        wrapper_class: type[wsgify[Concatenate[_AppT_contra, _P], _RequestT_contra]],
        app: _AppT_contra | None,
        kw: dict[str, Any],
    ) -> None: ...
    @overload
    def __call__(self, func: None, app: _AppT_contra | None = None) -> Self: ...
    @overload
    def __call__(
        self, func: _Middleware[_RequestT_contra, _AppT_contra, _P], app: None = None
    ) -> wsgify[Concatenate[_AppT_contra, _P], _RequestT_contra]: ...
    @overload
    def __call__(
        self, func: _Middleware[_RequestT_contra, _AppT_contra, _P], app: _AppT_contra
    ) -> wsgify[Concatenate[_AppT_contra, _P], _RequestT_contra]: ...

class _MiddlewareFactory(Generic[_P, _AppT_contra, _RequestT_contra]):
    """A middleware that has not yet been bound to an application or
    configured.
    """

    wrapper_class: type[wsgify[Concatenate[_AppT_contra, _P], _RequestT_contra]]
    middleware: _Middleware[_RequestT_contra, _AppT_contra, _P]
    kw: dict[str, Any]
    def __init__(
        self,
        wrapper_class: type[wsgify[Concatenate[_AppT_contra, _P], _RequestT_contra]],
        middleware: _Middleware[_RequestT_contra, _AppT_contra, _P],
        kw: dict[str, Any],
    ) -> None: ...
    # NOTE: Technically you are not allowed to pass args, but we give up all kinds
    #       of other safety if we don't use ParamSpec
    @overload
    def __call__(
        self, app: None = None, *_: _P.args, **config: _P.kwargs
    ) -> _MiddlewareFactory[[], _AppT_contra, _RequestT_contra]: ...
    @overload
    def __call__(self, app: _AppT_contra, *_: _P.args, **config: _P.kwargs) -> wsgify[[_AppT_contra], _RequestT_contra]: ...
