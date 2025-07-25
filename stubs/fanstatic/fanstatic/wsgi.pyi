from _typeshed.wsgi import WSGIApplication
from typing import Any

from fanstatic.core import Resource
from fanstatic.injector import InjectorPlugin
from fanstatic.publisher import Delegator
from webob import Request, Response
from webob.dec import wsgify

def Fanstatic(
    app: WSGIApplication, publisher_signature: str = ..., injector: InjectorPlugin | None = None, **config: Any
) -> Delegator:
    """Fanstatic WSGI framework component.

    :param app: The WSGI app to wrap with Fanstatic.

    :param publisher_signature: Optional argument to define the
      signature of the publisher in a URL. The default is ``fanstatic``.

    :param injector: A injector callable.

    :param ``**config``: Optional keyword arguments. These are
      passed to :py:class:`NeededInclusions` when it is constructed.
    """

def make_fanstatic(app: WSGIApplication, global_config: Any, **local_config: Any) -> Delegator: ...

class Serf:
    """Serf WSGI application.

    Serve a very simple HTML page while needing a resource. Can be
    configured behind the :py:func:`Fanstatic` WSGI framework
    component to let the resource be included.

    :param resource: The :py:class:`Resource` to include.
    """

    resource: Resource
    def __init__(self, resource: Resource) -> None: ...
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

def make_serf(global_config: Any, **local_config: Any) -> Serf: ...
def resolve(name: str, module: str | None = None) -> Any: ...
