"""
This module defines standard interpreted text role functions, a registry for
interpreted text roles, and an API for adding to and retrieving from the
registry. See also `Creating reStructuredText Interpreted Text Roles`__.

__ https://docutils.sourceforge.io/docs/ref/rst/roles.html


The interface for interpreted role functions is as follows::

    def role_fn(name, rawtext, text, lineno, inliner,
                options=None, content=None):
        code...

    # Set function attributes for customization:
    role_fn.options = ...
    role_fn.content = ...

Parameters:

- ``name`` is the local name of the interpreted text role, the role name
  actually used in the document.

- ``rawtext`` is a string containing the entire interpreted text construct.
  Return it as a ``problematic`` node linked to a system message if there is a
  problem.

- ``text`` is the interpreted text content, with backslash escapes converted
  to nulls (``\x00``).

- ``lineno`` is the line number where the text block containing the
  interpreted text begins.

- ``inliner`` is the Inliner object that called the role function.
  It defines the following useful attributes: ``reporter``,
  ``problematic``, ``memo``, ``parent``, ``document``.

- ``options``: A dictionary of directive options for customization, to be
  interpreted by the role function.  Used for additional attributes for the
  generated elements and other functionality.

- ``content``: A list of strings, the directive content for customization
  ("role" directive).  To be interpreted by the role function.

Function attributes for customization, interpreted by the "role" directive:

- ``options``: A dictionary, mapping known option names to conversion
  functions such as `int` or `float`.  ``None`` or an empty dict implies no
  options to parse.  Several directive option conversion functions are defined
  in the `directives` module.

  All role functions implicitly support the "class" option, unless disabled
  with an explicit ``{'class': None}``.

- ``content``: A boolean; true if content is allowed.  Client code must handle
  the case where content is required but not supplied (an empty content list
  will be supplied).

Note that unlike directives, the "arguments" function attribute is not
supported for role customization.  Directive arguments are handled by the
"role" directive itself.

Interpreted role functions return a tuple of two values:

- A list of nodes which will be inserted into the document tree at the
  point where the interpreted role was encountered (can be an empty
  list).

- A list of system messages, which will be inserted into the document tree
  immediately after the end of the current inline block (can also be empty).
"""

from collections.abc import Callable, Mapping, Sequence
from typing import Any, Final
from typing_extensions import TypeAlias

import docutils.parsers.rst.states
from docutils import nodes
from docutils.languages import _LanguageModule
from docutils.nodes import Node, system_message
from docutils.parsers.rst.states import Inliner
from docutils.utils import Reporter

__docformat__: Final = "reStructuredText"
DEFAULT_INTERPRETED_ROLE: Final = "title-reference"

_RoleFn: TypeAlias = Callable[
    [str, str, str, int, docutils.parsers.rst.states.Inliner, Mapping[str, Any], Sequence[str]],
    tuple[Sequence[nodes.reference], Sequence[nodes.reference]],
]

def register_canonical_role(name: str, role_fn: _RoleFn) -> None:
    """
    Register an interpreted text role by its canonical name.

    :Parameters:
      - `name`: The canonical name of the interpreted role.
      - `role_fn`: The role function.  See the module docstring.
    """

def register_local_role(name: str, role_fn: _RoleFn) -> None:
    """
    Register an interpreted text role by its local or language-dependent name.

    :Parameters:
      - `name`: The local or language-dependent name of the interpreted role.
      - `role_fn`: The role function.  See the module docstring.
    """

def role(
    role_name: str, language_module: _LanguageModule, lineno: int, reporter: Reporter
) -> tuple[_RoleFn | None, list[system_message]]:
    """
    Locate and return a role function from its language-dependent name, along
    with a list of system messages.

    If the role is not found in the current language, check English. Return a
    2-tuple: role function (``None`` if the named role cannot be found) and a
    list of system messages.
    """

def set_implicit_options(role_fn: _RoleFn) -> None:
    """
    Add customization options to role functions, unless explicitly set or
    disabled.
    """

def register_generic_role(canonical_name: str, node_class: type[Node]) -> None:
    """For roles which simply wrap a given `node_class` around the text."""

class GenericRole:
    """
    Generic interpreted text role.

    The interpreted text is simply wrapped with the provided node class.
    """

    name: str
    node_class: type[Node]
    def __init__(self, role_name: str, node_class: type[Node]) -> None: ...
    def __call__(
        self,
        role: str,
        rawtext: str,
        text: str,
        lineno: int,
        inliner: Inliner,
        options: Mapping[str, Any] | None = None,
        content: Sequence[str] | None = None,
    ) -> tuple[list[Node], list[system_message]]: ...

class CustomRole:
    """Wrapper for custom interpreted text roles."""

    name: str
    base_role: _RoleFn | CustomRole
    options: Mapping[str, Any]
    content: Sequence[str]
    supplied_options: Mapping[str, Any]
    supplied_content: Sequence[str]
    def __init__(
        self,
        role_name: str,
        base_role: _RoleFn | CustomRole,
        options: Mapping[str, Any] | None = None,
        content: Sequence[str] | None = None,
    ) -> None: ...
    def __call__(
        self,
        role: str,
        rawtext: str,
        text: str,
        lineno: int,
        inliner: Inliner,
        options: Mapping[str, Any] | None = None,
        content: Sequence[str] | None = None,
    ) -> tuple[list[Node], list[system_message]]: ...

def generic_custom_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Mapping[str, Any] | None = None,
    content: Sequence[str] | None = None,
) -> tuple[list[Node], list[system_message]]:
    """Base for custom roles if no other base role is specified."""

def pep_reference_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Mapping[str, Any] | None = None,
    content: Sequence[str] | None = None,
) -> tuple[list[Node], list[system_message]]: ...
def rfc_reference_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Mapping[str, Any] | None = None,
    content: Sequence[str] | None = None,
) -> tuple[list[Node], list[system_message]]: ...
def raw_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Mapping[str, Any] | None = None,
    content: Sequence[str] | None = None,
) -> tuple[list[Node], list[system_message]]: ...
def code_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Mapping[str, Any] | None = None,
    content: Sequence[str] | None = None,
) -> tuple[list[Node], list[system_message]]: ...
def math_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Mapping[str, Any] | None = None,
    content: Sequence[str] | None = None,
) -> tuple[list[Node], list[system_message]]: ...
def unimplemented_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: Mapping[str, Any] | None = None,
    content: Sequence[str] | None = None,
) -> tuple[list[Node], list[system_message]]: ...
def set_classes(options: dict[str, str]) -> None:
    """Deprecated. Obsoleted by ``normalized_role_options()``."""

def normalized_role_options(options: Mapping[str, Any] | None) -> dict[str, Any]:
    """
    Return normalized dictionary of role options.

    * ``None`` is replaced by an empty dictionary.
    * The key 'class' is renamed to 'classes'.
    """
