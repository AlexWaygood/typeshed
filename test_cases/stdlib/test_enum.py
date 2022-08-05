import sys
from typing_extensions import assert_type
from enum import Enum, auto

if sys.version_info >= (3, 11):
    from enum import StrEnum

class Bar(Enum):
    X = auto()

assert_type(Bar.X, Bar)
assert_type(Bar.X.value, int)

if sys.version_info >= (3, 11):
    class Foo(StrEnum):
        X = auto()

    assert_type(Foo.X, Foo)
    assert_type(Foo.X.value, str)
