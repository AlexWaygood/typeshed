from _typeshed.wsgi import StartResponse, WSGIApplication, WSGIEnvironment
from abc import abstractmethod
from collections.abc import Iterable
from typing import Any, Literal, TypedDict
from typing_extensions import Unpack

from fanstatic.core import Dependable, NeededResources, Resource
from fanstatic.inclusion import Inclusion
from webob import Request, Response

class _NeededResourcesConfig(TypedDict, total=False):
    versioning: bool
    versioning_use_md5: bool
    recompute_hashes: bool
    base_url: str | None
    script_name: str | None
    publisher_signature: str
    resources: Iterable[Dependable] | None

class _InjectorPluginOptions(TypedDict, total=False):
    compile: bool
    bundle: bool
    rollup: bool
    debug: bool
    minified: bool

class _TopBottomInjectorPluginOptions(_InjectorPluginOptions, total=False):
    bottom: bool
    force_bottom: bool

CONTENT_TYPES: list[str]

class Injector:
    """Fanstatic injector WSGI framework component.

    This WSGI component takes care of injecting the proper resource
    inclusions into HTML when needed.

    This WSGI component is used automatically by the
    :py:func:`Fanstatic` WSGI framework component, but can also be
    used independently if you need more control.

    :param app: The WSGI app to wrap with the injector.

    :param ``**config``: Optional keyword arguments. These are passed
      to :py:class:`NeededResources` when it is constructed. It also
      makes sure that when initialized, it isn't given any
      configuration parameters that cannot be passed to
      ``NeededResources``.
    """

    app: WSGIApplication
    config: _NeededResourcesConfig
    injector: InjectorPlugin
    def __init__(
        self, app: WSGIApplication, injector: InjectorPlugin | None = None, **config: Unpack[_NeededResourcesConfig]
    ) -> None: ...
    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]: ...

class InjectorPlugin:
    """Base class that can be use to write an injector plugin. It will
    take out from the configuration the common options that can be
    used in conjunction with an Inclusion.
    """

    @property
    @abstractmethod
    def name(self) -> str: ...
    def __init__(self, options: _InjectorPluginOptions) -> None: ...
    def make_inclusion(self, needed: NeededResources, resources: set[Resource] | None = None) -> Inclusion:
        """Helper to create an Inclusion passing all the options
        configured in the configuration file.
        """

    def __call__(
        self, html: bytes, needed: NeededResources, request: Request | None = None, response: Response | None = None
    ) -> None:
        """Render the needed resources into the html.
        The request and response arguments are
        webob Request and Response objects.
        """

class TopBottomInjector(InjectorPlugin):
    name: Literal["topbottom"]
    def __init__(self, options: _TopBottomInjectorPluginOptions) -> None:
        """
        :param bottom: If set to ``True``, Fanstatic will include any
          resource that has been marked as "bottom safe" at the bottom of
          the web page, at the end of ``<body>``, as opposed to in the
          ``<head>`` section. This is useful for optimizing the load-time
          of Javascript resources.

        :param force_bottom: If set to ``True`` and ``bottom`` is set to
          ``True`` as well, all Javascript resources will be included at
          the bottom of a web page, even if they aren't marked bottom
          safe.

        """

    def group(self, needed: NeededResources) -> tuple[Inclusion, Inclusion]:
        """Return the top and bottom resources."""

def make_injector(app: WSGIApplication, global_config: Any, **local_config: Any) -> Injector: ...
