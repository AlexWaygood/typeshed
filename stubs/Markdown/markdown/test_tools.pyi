"""A collection of tools for testing the Markdown code base and extensions."""

import unittest
from _typeshed import Unused
from typing import Any

__all__ = ["TestCase", "LegacyTestCase", "Kwargs"]

class TestCase(unittest.TestCase):
    """
    A [`unittest.TestCase`][] subclass with helpers for testing Markdown output.

    Define `default_kwargs` as a `dict` of keywords to pass to Markdown for each
    test. The defaults can be overridden on individual tests.

    The `assertMarkdownRenders` method accepts the source text, the expected
    output, and any keywords to pass to Markdown. The `default_kwargs` are used
    except where overridden by `kwargs`. The output and expected output are passed
    to `TestCase.assertMultiLineEqual`. An `AssertionError` is raised with a diff
    if the actual output does not equal the expected output.

    The `dedent` method is available to dedent triple-quoted strings if
    necessary.

    In all other respects, behaves as `unittest.TestCase`.
    """

    default_kwargs: dict[str, Any]  # taken from source code
    def assertMarkdownRenders(
        self,
        source: str,
        expected: str,
        expected_attrs: dict[str, Any] | None = None,  # values passing to self.assertEqual()
        **kwargs,
    ) -> None:
        """
        Test that source Markdown text renders to expected output with given keywords.

        `expected_attrs` accepts a `dict`. Each key should be the name of an attribute
        on the `Markdown` instance and the value should be the expected value after
        the source text is parsed by Markdown. After the expected output is tested,
        the expected value for each attribute is compared against the actual
        attribute of the `Markdown` instance using `TestCase.assertEqual`.
        """

    def dedent(self, text: str) -> str:
        """
        Dedent text.
        """

class recursionlimit:
    """
    A context manager which temporarily modifies the Python recursion limit.

    The testing framework, coverage, etc. may add an arbitrary number of levels to the depth. To maintain consistency
    in the tests, the current stack depth is determined when called, then added to the provided limit.

    Example usage:

    ``` python
    with recursionlimit(20):
        # test code here
    ```

    See <https://stackoverflow.com/a/50120316/866026>.
    """

    limit: int
    old_limit: int
    def __init__(self, limit: int) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, type: Unused, value: Unused, tb: Unused) -> None: ...

class Kwargs(dict[str, Any]):
    """A `dict` like class for holding keyword arguments."""

class LegacyTestMeta(type):
    def __new__(cls, name: str, bases: tuple[type, ...], dct: dict[str, Any]): ...  # dct is namespace argument for type.__new__()

class LegacyTestCase(unittest.TestCase, metaclass=LegacyTestMeta):
    """
    A [`unittest.TestCase`][] subclass for running Markdown's legacy file-based tests.

    A subclass should define various properties which point to a directory of
    text-based test files and define various behaviors/defaults for those tests.
    The following properties are supported:

    Attributes:
        location (str): A path to the directory of test files. An absolute path is preferred.
        exclude (list[str]): A list of tests to exclude. Each test name should comprise the filename
            without an extension.
        normalize (bool): A boolean value indicating if the HTML should be normalized. Default: `False`.
        input_ext (str): A string containing the file extension of input files. Default: `.txt`.
        output_ext (str): A string containing the file extension of expected output files. Default: `html`.
        default_kwargs (Kwargs[str, Any]): The default set of keyword arguments for all test files in the directory.

    In addition, properties can be defined for each individual set of test files within
    the directory. The property should be given the name of the file without the file
    extension. Any spaces and dashes in the filename should be replaced with
    underscores. The value of the property should be a `Kwargs` instance which
    contains the keyword arguments that should be passed to `Markdown` for that
    test file. The keyword arguments will "update" the `default_kwargs`.

    When the class instance is created, it will walk the given directory and create
    a separate `Unitttest` for each set of test files using the naming scheme:
    `test_filename`. One `Unittest` will be run for each set of input and output files.
    """
