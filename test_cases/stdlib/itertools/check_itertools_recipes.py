"""Type-annotated versions of the recipes from the itertools docs.

These are all meant to be examples of idiomatic itertools usage,
so they should all type-check without error.
"""
from __future__ import annotations

import operator
from itertools import groupby
from typing import Callable, Iterable, Iterator, TypeVar

_T = TypeVar("_T")


# In the itertools recipes, this is a one-liner,
# but that's a bit too much for pyright to handle
def unique_justseen(iterable: Iterable[_T], key: Callable[[_T], bool] | None = None) -> Iterator[_T]:
    "List unique elements, preserving order. Remember only the element just seen."
    # unique_justseen('AAAABBBCCDAABBB') --> A B C D A B
    # unique_justseen('ABBcCAD', str.lower) --> A B c A D
    return map(next, map(operator.itemgetter(1), groupby(iterable, key)))
