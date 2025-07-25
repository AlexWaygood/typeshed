from collections.abc import Hashable, Iterable

def eval(a: Iterable[Hashable], b: Iterable[Hashable]) -> int: ...
def distance(a: Iterable[Hashable], b: Iterable[Hashable]) -> int:
    """ "An alias to eval"""

def eval_criterion(a: Iterable[Hashable], b: Iterable[Hashable], thr: int) -> bool: ...
def distance_le_than(a: Iterable[Hashable], b: Iterable[Hashable], thr: int) -> bool:
    """ "An alias to eval"""

__all__ = ("eval", "distance", "eval_criterion", "distance_le_than")
