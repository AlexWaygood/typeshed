from abc import abstractmethod
from collections.abc import Callable, Iterable
from threading import local
from types import ModuleType
from typing import Literal, NewType
from typing_extensions import TypeAlias

from fanstatic.compiler import Compiler, Minifier

_Renderer: TypeAlias = Callable[[str], str]

DEFAULT_SIGNATURE: str
VERSION_PREFIX: str
BUNDLE_PREFIX: str
NEEDED: str
DEBUG: str
MINIFIED: str

def set_resource_file_existence_checking(v: bool) -> None:
    """Set resource file existence checking to True or False.

    By default, this is set to True, so that resources that point to
    non-existent files will result in an error. We recommend you keep
    it at this value when using Fanstatic. An
    :py:class:`UnknownResourceError` will then be raised if you
    accidentally refer to a non-existent resource.

    When running tests it's often useful to make fake resources that
    don't really have a filesystem representation, so this is set to
    False temporarily; for the Fanstatic tests this is done. Inside
    a test for this particular feature, this can temporarily be set
    to True.
    """

def set_auto_register_library(v: bool) -> None:
    """
    Global to say whether the Library instances should auto-register
    themselves to the Library registry. Defaults to False, is useful in tests.
    """

class UnknownResourceExtensionError(Exception):
    """A resource has an unrecognized extension."""

class ModeResourceDependencyError(Exception):
    """A Mode Resource does not have the same dependencies as the
    resource it replaces.
    """

UnknownResourceExtension = UnknownResourceExtensionError

class UnknownResourceError(Exception):
    """Resource refers to non-existent resource file."""

class ConfigurationError(Exception):
    """Impossible or illegal configuration."""

class LibraryDependencyCycleError(Exception):
    """Dependency cycles between libraries aren't allowed.

    A dependency cycle between libraries occurs when the file in one
    library depends on a file in another library, while that library
    depends on a file in the first library.
    """

class SlotError(Exception):
    """A slot was filled in incorrectly.

    If a slot is required, it must be filled in by passing an extra
    dictionary parameter to the ``.need`` method, containing a mapping
    from the required :py:class:`Slot` to :py:class:`Resource`.

    When a slot is filled, the resource filled in should have
    the same dependencies as the slot, or a subset of the dependencies
    of the slot. It should also have the same extension as the slot.
    If this is not the case, it is an error.
    """

class Library:
    """The resource library.

    This object defines which directory is published and can be
    referred to by :py:class:`Resource` objects to describe
    these resources.

    :param name: A string that uniquely identifies this library.

    :param rootpath: An absolute or relative path to the directory
      that contains the static resources this library publishes. If
      relative, it will be relative to the directory of the module
      that initializes the library.

    :param ignores: A list of globs used to determine which files
      and directories not to publish.
    """

    path: str
    name: str
    rootpath: str
    ignores: list[str]
    version: str | None
    known_resources: dict[str, Resource]
    known_assets: dict[str, Asset]
    module: ModuleType
    compilers: dict[str, Compiler]
    minifiers: dict[str, Minifier]
    def __init__(
        self,
        name: str,
        rootpath: str,
        ignores: list[str] | None = None,
        version: str | None = None,
        compilers: dict[str, Compiler] | None = None,
        minifiers: dict[str, Minifier] | None = None,
    ) -> None: ...
    def check_dependency_cycle(self, resource: Resource) -> None: ...
    def register(self, resource: Resource) -> None:
        """Register a Resource with this Library.

        A Resource knows about its Library. After a Resource has registered
        itself with its Library, the Library knows about the Resources
        associated to it.
        """

    def signature(self, recompute_hashes: bool = False, version_method: Callable[[str], str] | None = None) -> str:
        """Get a unique signature for this Library.

        If a version has been defined, we return the version.

        If no version is defined, a hash of the contents of the directory
        indicated by ``path`` is calculated.
        If ``recompute_hashes`` is set to ``True``, the signature will be
        recalculated each time, which is useful during development when
        changing Javascript/css code and images.
        """

def caller_dir() -> str: ...

class InclusionRenderers(dict[str, tuple[int, _Renderer]]):
    def register(self, extension: str, renderer: _Renderer, order: int | None = None) -> None:
        """Register a renderer function for a given filename extension.

        :param extension: the filename extension to register the
          renderer for.

        :param renderer: a callable that should accept a URL argument
          and return a rendered HTML snippet for this resource.

        :param order: optionally, to control the order in which the
          snippets are included in the HTML document. If no order is
          given, the resource will be included after all other resource
          inclusions. The lower the order number, the earlier in the
          rendering the inclusion will appear.
        """

inclusion_renderers: InclusionRenderers

def register_inclusion_renderer(extension: str, renderer: _Renderer, order: int | None = None) -> None:
    """Register a renderer function for a given filename extension.

    :param extension: the filename extension to register the
      renderer for.

    :param renderer: a callable that should accept a URL argument
      and return a rendered HTML snippet for this resource.

    :param order: optionally, to control the order in which the
      snippets are included in the HTML document. If no order is
      given, the resource will be included after all other resource
      inclusions. The lower the order number, the earlier in the
      rendering the inclusion will appear.
    """

def render_ico(url: str) -> str: ...
def render_css(url: str) -> str: ...
def render_js(url: str) -> str: ...
def render_print_css(url: str) -> str: ...
def render_screen_css(url: str) -> str: ...

class Renderable:
    """A renderable.

    A renderable must have a library attribute and a dependency_nr.
    """

    @abstractmethod
    def render(self, library_url: str) -> str:
        """Render this renderable as something to insert in HTML.

        This returns a snippet.
        """

class Dependable:
    """Dependables have a dependencies and an a resources attributes."""

    @property
    @abstractmethod
    def resources(self) -> set[Dependable]:
        """The type of the None singleton."""

    @property
    @abstractmethod
    def depends(self) -> set[Dependable]:
        """The type of the None singleton."""

    @property
    @abstractmethod
    def supports(self) -> set[Dependable]:
        """The type of the None singleton."""

    def add_dependency(self, dependency: Dependable) -> None: ...
    @abstractmethod
    def set_dependencies(self, dependencies: Iterable[Dependable] | None) -> None: ...
    @abstractmethod
    def list_assets(self) -> set[Asset]: ...
    def list_supporting(self) -> set[Dependable]: ...

class Asset(Dependable):
    """An asset can either a resource or a slot."""

    resources: set[Dependable]
    depends: set[Dependable]
    supports: set[Dependable]
    library: Library
    def __init__(self, library: Library, depends: Iterable[Dependable] | None = None) -> None: ...
    def set_dependencies(self, depends: Iterable[Dependable] | None) -> None: ...
    def list_assets(self) -> set[Asset]: ...

_NothingType = NewType("_NothingType", object)
NOTHING: _NothingType

class Resource(Renderable, Asset):
    """A resource.

    A resource specifies a single resource in a library so that it can
    be included in a web page. This is useful for Javascript and CSS
    resources in particular. Some static resources such as images are
    not included in this way and therefore do not have to be defined
    this way.

    :param library: the :py:class:`Library` this resource is in.

    :param relpath: the relative path (from the root of the library
      path) that indicates the actual resource file.

    :param depends: optionally, a list of resources that this resource
      depends on. Entries in the list are :py:class:`Resource`
      instances.

    :param supersedes: optionally, a list of :py:class:`Resource`
      instances that this resource supersedes as a rollup
      resource. If all these resources are required for render a page,
      the superseding resource will be included instead.

    :param bottom: indicate that this resource is "bottom safe": it
      can be safely included on the bottom of the page (just before
      ``</body>``). This can be used to improve the performance of
      page loads when Javascript resources are in use. Not all
      Javascript-based resources can however be safely included that
      way, so you have to set this explicitly (or use the
      ``force_bottom`` option on :py:class:`NeededResources`).

    :param renderer: optionally, a callable that accepts an URL
      argument and returns a rendered HTML snippet for this
      resource. If no renderer is provided, a renderer is looked up
      based on the resource's filename extension.

    :param dont_bundle: Don't bundle this resource in any bundles
      (if bundling is enabled).

    """

    relpath: str
    ext: str
    mode_parent: str | None
    compiler: Compiler
    source: str | None
    minifier: Minifier
    minified: Resource | None
    bottom: bool
    dont_bundle: bool
    renderer: _Renderer
    modes: dict[str, Resource]
    supersedes: list[Resource]
    rollups: list[Resource]
    def __init__(
        self,
        library: Library,
        relpath: str,
        depends: Iterable[Dependable] | None = None,
        supersedes: list[Resource] | None = None,
        bottom: bool = False,
        renderer: _Renderer | None = None,
        debug: str | Resource | None = None,
        dont_bundle: bool = False,
        minified: str | Resource | None = None,
        minifier: Minifier | _NothingType = ...,
        compiler: Compiler | _NothingType = ...,
        source: str | None = None,
        mode_parent: str | None = None,
    ) -> None: ...
    def fullpath(self, path: str | None = None) -> str: ...
    def compile(self, force: bool = False) -> None: ...
    def render(self, library_url: str) -> str: ...
    def mode(self, mode: str | None) -> Resource:
        """Get Resource in another mode.

        If the mode is ``None`` or if the mode cannot be found, this
        ``Resource`` instance is returned instead.

        :param mode: a string indicating the mode, or ``None``.
        """

    def need(self, slots: dict[Slot, Resource] | None = None) -> None:
        """Declare that the application needs this resource.

        If you call ``.need()`` on ``Resource`` sometime during the
        rendering process of your web page, this resource and all its
        dependencies will be inserted as inclusions into the web page.

        :param slots: an optional dictionary mapping from
          :py:class:`Slot` instances to :py:class:`Resource`
          instances. This dictionary describes how to fill in the
          slots that this resource might depend on (directly or
          indirectly). If a slot is required, the dictionary must
          contain an entry for it.
        """

_RequiredDefaultMarkerType = NewType("_RequiredDefaultMarkerType", object)
REQUIRED_DEFAULT_MARKER: _RequiredDefaultMarkerType

class Slot(Asset):
    """A resource slot.

    Sometimes only the application has knowledge on how to fill in a
    dependency for a resource, and this cannot be known at resource
    definition time. In this case you can define a slot, and make your
    resource depend on that. This slot can then be filled in with a
    real resource by the application when you ``.need()`` that
    resource (or when you need something that depends on the slot
    indirectly).

    :param library: the :py:class:`Library` this slot is in.

    :param ext: the extension of the slot, for instance '.js'. This
      determines what kind of resources can be slotted in here.

    :param required: a boolean indicating whether this slot is
      required to be filled in when a resource that depends on a slot
      is needed, or whether it's optional. By default filling in a
      slot is required.

    :param depends: optionally, a list of resources that this slot
      depends on. Resources that are slotted in here need to have
      the same dependencies as that of the slot, or a strict subset.
    """

    default: Resource | None
    ext: str
    required: bool
    def __init__(
        self,
        library: Library,
        extension: str,
        depends: Iterable[Dependable] | None = None,
        required: bool | _RequiredDefaultMarkerType = ...,
        default: Resource | None = None,
    ) -> None: ...

class FilledSlot(Renderable):
    filledby: Resource
    library: Library
    relpath: str
    bottom: bool
    rollups: list[Resource]
    dont_bundle: bool
    ext: str
    order: int
    renderer: _Renderer
    dependency_nr: int
    modes: dict[str, FilledSlot]
    def __init__(self, slot: Slot, resource: Resource) -> None: ...
    def render(self, library_url: str) -> str: ...
    def compile(self, force: bool = False) -> None: ...
    def mode(self, mode: str | None) -> FilledSlot: ...

class Group(Dependable):
    """A resource used to group resources together.

     It doesn't define a resource file itself, but instead depends on
     other resources. When a Group is depended on, all the resources
     grouped together will be included.

    :param depends: a list of resources that this resource depends
      on. Entries in the list can be :py:class:`Resource` instances, or
      :py:class:`Group` instances.
    """

    resources: set[Dependable]
    depends: set[Dependable]
    supports: set[Dependable]
    def __init__(self, depends: Iterable[Dependable]) -> None: ...
    def set_dependencies(self, depends: Iterable[Dependable]) -> None: ...  # type: ignore[override]
    def list_assets(self) -> set[Asset]: ...
    def need(self, slots: dict[Slot, Resource] | None = None) -> None:
        """Need this group resource.

        If you call ``.need()`` on ``Group`` sometime
        during the rendering process of your web page, all dependencies
        of this group resources will be inserted into the web page.

        :param slots: an optional dictionary mapping from
          :py:class:`Slot` instances to :py:class:`Resource`
          instances. This dictionary describes how to fill in the
          slots that this resource might depend on (directly or
          indirectly). If a slot is required, the dictionary must
          contain an entry for it.
        """

GroupResource = Group

class NeededResources:
    """The current selection of needed resources..

    The ``NeededResources`` instance maintains a set of needed
    resources for a particular web page.

    :param versioning: If ``True``, Fanstatic will automatically include
      a version identifier in all URLs pointing to resources.
      Since the version identifier will change when you update a resource,
      the URLs can both be infinitely cached and the resources will always
      be up to date. See also the ``recompute_hashes`` parameter.

    :param versioning_use_md5: If ``True``, Fanstatic will use and md5
      algorithm instead of an algorithm based on the last modification time of
      the Resource files to compute versions. Use md5 if you don't trust your
      filesystem.

    :param recompute_hashes: If ``True`` and versioning is enabled, Fanstatic
      will recalculate hash URLs on the fly whenever you make changes, even
      without restarting the server. This is useful during development,
      but slower, so should be turned off during deployment.
      If set to ``False``, the hash URLs will only be
      calculated once after server startup.

    :param base_url: This URL will be prefixed in front of all resource
      URLs. This can be useful if your web framework wants the resources
      to be published on a sub-URL. By default, there is no ``base_url``,
      and resources are served in the script root. Note that this can
      also be set with the set_base_url method on a ``NeededResources``
      instance.

    :param script_name: The script_name is a fallback for computing
      library URLs. The base_url parameter should be honoured if
      it is provided.

    :param publisher_signature: The name under which resource libraries
      should be served in the URL. By default this is ``fanstatic``, so
      URLs to resources will start with ``/fanstatic/``.

    :param resources: Optionally, a list of resources we want to
      include. Normally you specify resources to include by calling
      ``.need()`` on them, or alternatively by calling ``.need()``
      on an instance of this class.

    """

    def __init__(
        self,
        versioning: bool = False,
        versioning_use_md5: bool = False,
        recompute_hashes: bool = True,
        base_url: str | None = None,
        script_name: str | None = None,
        publisher_signature: str = ...,
        resources: Iterable[Dependable] | None = None,
    ) -> None: ...
    def has_resources(self) -> bool:
        """Returns True if any resources are needed."""

    def has_base_url(self) -> bool:
        """Returns True if base_url has been set."""

    def set_base_url(self, url: str) -> None:
        """Set the base_url. The base_url can only be set (1) if it has not
        been set in the NeededResources configuration and (2) if it has not
        been set before using this method.
        """

    def need(self, resource: Resource | Group, slots: dict[Slot, Resource] | None = None) -> None:
        """Add a particular resource to the needed resources.

        This is an alternative to calling ``.need()`` on the resource
        directly.

        :param resource: A :py:class:`Resource` instance.

        :param slots: an optional dictionary mapping from
          :py:class:`Slot` instances to :py:class:`Resource`
          instances. This dictionary describes how to fill in the
          slots that the given resource might depend on (directly or
          indirectly). If a slot is required, the dictionary must
          contain an entry for it.
        """

    def resources(self) -> set[Resource]:
        """Retrieve the list of resources needed.

        This returns the needed :py:class:`Resource`
        instances.  Resources are guaranteed to come earlier in the
        list than those resources that depend on them.

        Resources are also sorted by extension.
        """

    def clear(self) -> None: ...
    def library_url(self, library: Library) -> str:
        """Construct URL to library.

        This constructs a URL to a library, obey ``versioning`` and
        ``base_url`` configuration.

        :param library: A :py:class:`Library` instance.
        """

class DummyNeededResources:
    """A dummy implementation of the needed resources.

    This class implements the same API as the NeededResources class,
    but refuses to do anything but need() resources. Resources that are
    needed are dropped to the floor.
    """

    def need(self, resource: Resource | Group, slots: dict[Slot, Resource] | None = None) -> None: ...
    def has_resources(self) -> Literal[False]: ...

thread_local_needed_data: local

def init_needed(
    versioning: bool = False,
    versioning_use_md5: bool = False,
    recompute_hashes: bool = True,
    base_url: str | None = None,
    script_name: str | None = None,
    publisher_signature: str = ...,
    resources: Iterable[Dependable] | None = None,
) -> NeededResources:
    """Initialize a NeededResources object in the thread-local data. Arguments
    are passed verbatim to the NeededResource __init__.
    """

def del_needed() -> None:
    """Delete the NeededResources object from the thread-local data to leave a
    clean environment.

    This function will silently pass whenever there is no NeededResources
    object in the thread-local in the first place.
    """

def get_needed() -> NeededResources | DummyNeededResources: ...
def clear_needed() -> None: ...

class Bundle(Renderable):
    def __init__(self) -> None: ...
    @property
    def dirname(self) -> str: ...
    @property
    def library(self) -> Library: ...
    @property
    def renderer(self) -> _Renderer: ...
    @property
    def ext(self) -> str: ...
    @property
    def relpath(self) -> str: ...
    def resources(self) -> list[Resource]:
        """This is used to test resources, not because this is a dependable."""

    def render(self, library_url: str) -> str: ...
    def fits(self, resource: Resource) -> bool: ...
    def append(self, resource: Resource) -> None: ...
    def add_to_list(self, result: list[Renderable]) -> None:
        """Add the bundle to list, taking single-resource bundles into account."""
