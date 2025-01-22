import unittest.result
from collections.abc import Callable
from typing import TypeVar, overload
from typing_extensions import ParamSpec

_P = ParamSpec("_P")
_T = TypeVar("_T")

def installHandler() -> None: ...
def registerResult(result: unittest.result.TestResult) -> None: ...
def removeResult(result: unittest.result.TestResult) -> bool: ...
@overload
def removeHandler(method: None = None) -> None: ...
@overload
def removeHandler[**_P, _T](method: Callable[_P, _T]) -> Callable[_P, _T]: ...
