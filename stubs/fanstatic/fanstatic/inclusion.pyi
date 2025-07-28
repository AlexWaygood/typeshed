from collections.abc import Iterable

from fanstatic.core import Bundle, NeededResources, Resource

def bundle_resources(resources: Iterable[Resource]) -> list[Resource | Bundle]:
    """Bundle sorted resources together.

    resources is expected to be a list previously sorted by sorted_resources.

    Returns a list of renderable resources, which can include several
    resources bundled together into Bundles.
    """

def rollup_resources(resources: Iterable[Resource]) -> set[Resource]:
    """Rollup resources together: if a resource include multiple
    separate ones (i.e. is a rollup) and all the separate ones are
    included the rollup will be used instead.
    """

def sort_resources(resources: Iterable[Resource]) -> list[Resource]:
    """Sort resources for inclusion on web page.

    A number of rules are followed:

    * resources are always grouped per renderer (.js, .css, etc)
    * resources that depend on other resources are sorted later
    * resources are grouped by library, if the dependencies allow it
    * libraries are sorted by name, if dependencies allow it
    * resources are sorted by resource path if they both would be
      sorted the same otherwise.

    The only purpose of sorting on library is so we can
    group resources per library, so that bundles can later be created
    of them if bundling support is enabled.

    Note this sorting algorithm guarantees a consistent ordering, no
    matter in what order resources were needed.
    """

class Inclusion:
    """
    An Inclusion is a container/group for a set of Resources that are needed.
    The Inclusion controls various aspects of these Resources:

    :param mode: If set to ``MINIFIED``, Fanstatic will include all
      resources in ``minified`` form. If a Resource instance does not
      provide a ``minified`` mode, the "main" (non-named) mode is used.

      If set to ``DEBUG``, Fanstatic will include all
      resources in ``debug`` form. If a Resource instance does not
      provide a ``debug`` mode, the "main" (non-named) mode is used.
      An exception is raised when both the ``debug`` and ``minified``
      parameters are ``True``.

    :param rollup: If set to True (default is False) rolled up
      combined resources will be served if they exist and supersede
      existing resources that are needed.

    :param bundle: If set to True, Fanstatic will attempt to bundle
      resources that fit together into larger Bundle objects. These
      can then be rendered as single URLs to these bundles.

    :param compile: If set to True, Fanstatic will compile resources
      for every time the Inclusion is created. You'll probably want to set
      this to False in a production environment.
    """

    needed: NeededResources
    resources: list[Resource | Bundle]
    def __init__(
        self,
        needed: NeededResources,
        resources: Iterable[Resource] | None = None,
        compile: bool = False,
        bundle: bool = False,
        mode: str | None = None,
        rollup: bool = False,
    ) -> None: ...
    def __len__(self) -> int: ...
    def render(self) -> str: ...
