"""
Decorator module, see http://pypi.python.org/pypi/decorator
for the documentation.
"""

import re
from _typeshed import Incomplete
from collections.abc import Callable
from inspect import getfullargspec as getfullargspec
from typing import Final

__version__: Final[str]
__all__ = ["decorator", "FunctionMaker", "contextmanager"]

def get_init(cls: object) -> Callable[..., None]: ...

DEF: re.Pattern[str]

class FunctionMaker:
    """
    An object with the ability to create functions with a given signature.
    It has attributes name, doc, module, signature, defaults, dict and
    methods update and make.
    """

    shortsignature: Incomplete
    name: Incomplete
    doc: Incomplete
    module: Incomplete
    annotations: Incomplete
    signature: Incomplete
    dict: Incomplete
    defaults: Incomplete
    def __init__(self, func=None, name=None, signature=None, defaults=None, doc=None, module=None, funcdict=None) -> None: ...
    def update(self, func, **kw) -> None:
        """Update the signature of func with the data in self"""

    def make(self, src_templ, evaldict=None, addsource: bool = False, **attrs):
        """Make a new function from a given template and update the signature"""

    @classmethod
    def create(cls, obj, body, evaldict, defaults=None, doc=None, module=None, addsource: bool = True, **attrs):
        """
        Create a function from the strings name, signature and body.
        evaldict is the evaluation dictionary. If addsource is true an attribute
        __source__ is added to the result. The attributes attrs are added,
        if any.
        """

def decorator(caller, func=None):
    """
    decorator(caller) converts a caller function into a decorator;
    decorator(caller, func) decorates a function using a caller.
    """

contextmanager: Incomplete
