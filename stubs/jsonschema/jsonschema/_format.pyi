from collections.abc import Callable, Iterable
from typing import TypeVar
from typing_extensions import TypeAlias

_FormatCheckCallable: TypeAlias = Callable[[object], bool]
_F = TypeVar("_F", bound=_FormatCheckCallable)
_RaisesType: TypeAlias = type[Exception] | tuple[type[Exception], ...]

class FormatChecker:
    """
    A ``format`` property checker.

    JSON Schema does not mandate that the ``format`` property actually do any
    validation. If validation is desired however, instances of this class can
    be hooked into validators to enable format validation.

    `FormatChecker` objects always return ``True`` when asked about
    formats that they do not know how to validate.

    To add a check for a custom format use the `FormatChecker.checks`
    decorator.

    Arguments:

        formats:

            The known formats to validate. This argument can be used to
            limit which formats will be used during validation.

    """

    checkers: dict[str, tuple[_FormatCheckCallable, _RaisesType]]

    def __init__(self, formats: Iterable[str] | None = None) -> None: ...
    def checks(self, format: str, raises: _RaisesType = ()) -> Callable[[_F], _F]:
        """
        Register a decorated function as validating a new format.

        Arguments:

            format:

                The format that the decorated function will check.

            raises:

                The exception(s) raised by the decorated function when an
                invalid instance is found.

                The exception object will be accessible as the
                `jsonschema.exceptions.ValidationError.cause` attribute of the
                resulting validation error.

        """

    @classmethod
    def cls_checks(cls, format: str, raises: _RaisesType = ()) -> Callable[[_F], _F]: ...
    def check(self, instance: object, format: str) -> None:
        """
        Check whether the instance conforms to the given format.

        Arguments:

            instance (*any primitive type*, i.e. str, number, bool):

                The instance to check

            format:

                The format that instance should conform to

        Raises:

            FormatError:

                if the instance does not conform to ``format``

        """

    def conforms(self, instance: object, format: str) -> bool:
        """
        Check whether the instance conforms to the given format.

        Arguments:

            instance (*any primitive type*, i.e. str, number, bool):

                The instance to check

            format:

                The format that instance should conform to

        Returns:

            bool: whether it conformed

        """

draft3_format_checker: FormatChecker
draft4_format_checker: FormatChecker
draft6_format_checker: FormatChecker
draft7_format_checker: FormatChecker
draft201909_format_checker: FormatChecker
draft202012_format_checker: FormatChecker

def is_email(instance: object) -> bool: ...
def is_ipv4(instance: object) -> bool: ...
def is_ipv6(instance: object) -> bool: ...

# is_host_name is only defined if fqdn is installed.
def is_host_name(instance: object) -> bool: ...
def is_idn_host_name(instance: object) -> bool: ...
def is_uri(instance: object) -> bool: ...
def is_uri_reference(instance: object) -> bool: ...
def is_iri(instance: object) -> bool: ...
def is_iri_reference(instance: object) -> bool: ...
def is_datetime(instance: object) -> bool: ...
def is_time(instance: object) -> bool: ...
def is_regex(instance: object) -> bool: ...
def is_date(instance: object) -> bool: ...
def is_draft3_time(instance: object) -> bool: ...
def is_css21_color(instance: object) -> bool: ...
def is_json_pointer(instance: object) -> bool: ...
def is_relative_json_pointer(instance: object) -> bool: ...
def is_uri_template(instance: object) -> bool: ...

# is_duration is only defined if isoduration is installed.
def is_duration(instance: object) -> bool: ...
def is_uuid(instance: object) -> bool: ...
