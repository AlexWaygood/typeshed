from collections.abc import Callable, Collection, Iterable
from decimal import Decimal
from re import Match, Pattern
from typing import Any, TypeVar, overload

from wtforms.fields import Field, StringField
from wtforms.form import BaseForm

__all__ = (
    "DataRequired",
    "data_required",
    "Email",
    "email",
    "EqualTo",
    "equal_to",
    "IPAddress",
    "ip_address",
    "InputRequired",
    "input_required",
    "Length",
    "length",
    "NumberRange",
    "number_range",
    "Optional",
    "optional",
    "Regexp",
    "regexp",
    "URL",
    "url",
    "AnyOf",
    "any_of",
    "NoneOf",
    "none_of",
    "MacAddress",
    "mac_address",
    "UUID",
    "ValidationError",
    "StopValidation",
    "readonly",
    "ReadOnly",
    "disabled",
    "Disabled",
)

_ValuesT_contra = TypeVar("_ValuesT_contra", bound=Collection[Any], contravariant=True)

class ValidationError(ValueError):
    """
    Raised when a validator fails to validate its input.
    """

    def __init__(self, message: str = "", *args: object) -> None: ...

class StopValidation(Exception):
    """
    Causes the validation chain to stop.

    If StopValidation is raised, no more validators in the validation chain are
    called. If raised with a message, the message will be added to the errors
    list.
    """

    def __init__(self, message: str = "", *args: object) -> None: ...

class EqualTo:
    """
    Compares the values of two fields.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """

    fieldname: str
    message: str | None
    def __init__(self, fieldname: str, message: str | None = None) -> None: ...
    def __call__(self, form: BaseForm, field: Field) -> None: ...

class Length:
    """
    Validates the length of a string.

    :param min:
        The minimum required length of the string. If not provided, minimum
        length will not be checked.
    :param max:
        The maximum length of the string. If not provided, maximum length
        will not be checked.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `%(min)d` and `%(max)d` if desired. Useful defaults
        are provided depending on the existence of min and max.

    When supported, sets the `minlength` and `maxlength` attributes on widgets.
    """

    min: int
    max: int
    message: str | None
    field_flags: dict[str, Any]
    def __init__(self, min: int = -1, max: int = -1, message: str | None = None) -> None: ...
    def __call__(self, form: BaseForm, field: StringField) -> None: ...

class NumberRange:
    """
    Validates that a number is of a minimum and/or maximum value, inclusive.
    This will work with any comparable number type, such as floats and
    decimals, not just integers.

    :param min:
        The minimum required value of the number. If not provided, minimum
        value will not be checked.
    :param max:
        The maximum value of the number. If not provided, maximum value
        will not be checked.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `%(min)s` and `%(max)s` if desired. Useful defaults
        are provided depending on the existence of min and max.

    When supported, sets the `min` and `max` attributes on widgets.
    """

    min: float | Decimal | None
    max: float | Decimal | None
    message: str | None
    field_flags: dict[str, Any]
    def __init__(
        self, min: float | Decimal | None = None, max: float | Decimal | None = None, message: str | None = None
    ) -> None: ...
    # any numeric field will work, for now we don't try to use a union
    # to restrict to the defined numeric fields, since user-defined fields
    # will likely not use a common base class, just like the existing
    # numeric fields
    def __call__(self, form: BaseForm, field: Field) -> None: ...

class Optional:
    """
    Allows empty input and stops the validation chain from continuing.

    If input is empty, also removes prior errors (such as processing errors)
    from the field.

    :param strip_whitespace:
        If True (the default) also stop the validation chain on input which
        consists of only whitespace.

    Sets the `optional` attribute on widgets.
    """

    string_check: Callable[[str], bool]
    field_flags: dict[str, Any]
    def __init__(self, strip_whitespace: bool = True) -> None: ...
    def __call__(self, form: BaseForm, field: Field) -> None: ...

class DataRequired:
    """
    Checks the field's data is 'truthy' otherwise stops the validation chain.

    This validator checks that the ``data`` attribute on the field is a 'true'
    value (effectively, it does ``if field.data``.) Furthermore, if the data
    is a string type, a string containing only whitespace characters is
    considered false.

    If the data is empty, also removes prior errors (such as processing errors)
    from the field.

    **NOTE** this validator used to be called `Required` but the way it behaved
    (requiring coerced data, not input data) meant it functioned in a way
    which was not symmetric to the `Optional` validator and furthermore caused
    confusion with certain fields which coerced data to 'falsey' values like
    ``0``, ``Decimal(0)``, ``time(0)`` etc. Unless a very specific reason
    exists, we recommend using the :class:`InputRequired` instead.

    :param message:
        Error message to raise in case of a validation error.

    Sets the `required` attribute on widgets.
    """

    message: str | None
    field_flags: dict[str, Any]
    def __init__(self, message: str | None = None) -> None: ...
    def __call__(self, form: BaseForm, field: Field) -> None: ...

class InputRequired:
    """
    Validates that input was provided for this field.

    Note there is a distinction between this and DataRequired in that
    InputRequired looks that form-input data was provided, and DataRequired
    looks at the post-coercion data. This means that this validator only checks
    whether non-empty data was sent, not whether non-empty data was coerced
    from that data. Initially populated data is not considered sent.

    Sets the `required` attribute on widgets.
    """

    message: str | None
    field_flags: dict[str, Any]
    def __init__(self, message: str | None = None) -> None: ...
    def __call__(self, form: BaseForm, field: Field) -> None: ...

class Regexp:
    """
    Validates the field against a user provided regexp.

    :param regex:
        The regular expression string to use. Can also be a compiled regular
        expression pattern.
    :param flags:
        The regexp flags to use, for example re.IGNORECASE. Ignored if
        `regex` is not a string.
    :param message:
        Error message to raise in case of a validation error.
    """

    regex: Pattern[str]
    message: str | None
    def __init__(self, regex: str | Pattern[str], flags: int = 0, message: str | None = None) -> None: ...
    def __call__(self, form: BaseForm, field: StringField, message: str | None = None) -> Match[str]: ...

class Email:
    """
    Validates an email address. Requires email_validator package to be
    installed. For ex: pip install wtforms[email].

    :param message:
        Error message to raise in case of a validation error.
    :param granular_message:
        Use validation failed message from email_validator library
        (Default False).
    :param check_deliverability:
        Perform domain name resolution check (Default False).
    :param allow_smtputf8:
        Fail validation for addresses that would require SMTPUTF8
        (Default True).
    :param allow_empty_local:
        Allow an empty local part (i.e. @example.com), e.g. for validating
        Postfix aliases (Default False).
    """

    message: str | None
    granular_message: bool
    check_deliverability: bool
    allow_smtputf8: bool
    allow_empty_local: bool
    def __init__(
        self,
        message: str | None = None,
        granular_message: bool = False,
        check_deliverability: bool = False,
        allow_smtputf8: bool = True,
        allow_empty_local: bool = False,
    ) -> None: ...
    def __call__(self, form: BaseForm, field: StringField) -> None: ...

class IPAddress:
    """
    Validates an IP address.

    :param ipv4:
        If True, accept IPv4 addresses as valid (default True)
    :param ipv6:
        If True, accept IPv6 addresses as valid (default False)
    :param message:
        Error message to raise in case of a validation error.
    """

    ipv4: bool
    ipv6: bool
    message: str | None
    def __init__(self, ipv4: bool = True, ipv6: bool = False, message: str | None = None) -> None: ...
    def __call__(self, form: BaseForm, field: StringField) -> None: ...
    @classmethod
    def check_ipv4(cls, value: str | None) -> bool: ...
    @classmethod
    def check_ipv6(cls, value: str | None) -> bool: ...

class MacAddress(Regexp):
    """
    Validates a MAC address.

    :param message:
        Error message to raise in case of a validation error.
    """

    def __init__(self, message: str | None = None) -> None: ...
    def __call__(self, form: BaseForm, field: StringField) -> None: ...  # type: ignore[override]

class URL(Regexp):
    """
    Simple regexp based url validation. Much like the email validator, you
    probably want to validate the url later by other means if the url must
    resolve.

    :param require_tld:
        If true, then the domain-name portion of the URL must contain a .tld
        suffix.  Set this to false if you want to allow domains like
        `localhost`.
    :param allow_ip:
        If false, then give ip as host will fail validation
    :param message:
        Error message to raise in case of a validation error.
    """

    validate_hostname: HostnameValidation
    def __init__(self, require_tld: bool = True, allow_ip: bool = True, message: str | None = None) -> None: ...
    def __call__(self, form: BaseForm, field: StringField) -> None: ...  # type: ignore[override]

class UUID:
    """
    Validates a UUID.

    :param message:
        Error message to raise in case of a validation error.
    """

    message: str | None
    def __init__(self, message: str | None = None) -> None: ...
    def __call__(self, form: BaseForm, field: StringField) -> None: ...

class AnyOf:
    """
    Compares the incoming data to a sequence of valid inputs.

    :param values:
        A sequence of valid inputs.
    :param message:
        Error message to raise in case of a validation error. `%(values)s`
        contains the list of values.
    :param values_formatter:
        Function used to format the list of values in the error message.
    """

    values: Collection[Any]
    message: str | None
    values_formatter: Callable[[Any], str]
    @overload
    def __init__(self, values: Collection[Any], message: str | None = None, values_formatter: None = None) -> None: ...
    @overload
    def __init__(
        self, values: _ValuesT_contra, message: str | None, values_formatter: Callable[[_ValuesT_contra], str]
    ) -> None: ...
    @overload
    def __init__(
        self, values: _ValuesT_contra, message: str | None = None, *, values_formatter: Callable[[_ValuesT_contra], str]
    ) -> None: ...
    def __call__(self, form: BaseForm, field: Field) -> None: ...
    @staticmethod
    def default_values_formatter(values: Iterable[object]) -> str: ...

class NoneOf:
    """
    Compares the incoming data to a sequence of invalid inputs.

    :param values:
        A sequence of invalid inputs.
    :param message:
        Error message to raise in case of a validation error. `%(values)s`
        contains the list of values.
    :param values_formatter:
        Function used to format the list of values in the error message.
    """

    values: Collection[Any]
    message: str | None
    values_formatter: Callable[[Any], str]
    @overload
    def __init__(self, values: Collection[Any], message: str | None = None, values_formatter: None = None) -> None: ...
    @overload
    def __init__(
        self, values: _ValuesT_contra, message: str | None, values_formatter: Callable[[_ValuesT_contra], str]
    ) -> None: ...
    @overload
    def __init__(
        self, values: _ValuesT_contra, message: str | None = None, *, values_formatter: Callable[[_ValuesT_contra], str]
    ) -> None: ...
    def __call__(self, form: BaseForm, field: Field) -> None: ...
    @staticmethod
    def default_values_formatter(v: Iterable[object]) -> str: ...

class HostnameValidation:
    """
    Helper class for checking hostnames for validation.

    This is not a validator in and of itself, and as such is not exported.
    """

    hostname_part: Pattern[str]
    tld_part: Pattern[str]
    require_tld: bool
    allow_ip: bool
    def __init__(self, require_tld: bool = True, allow_ip: bool = False) -> None: ...
    def __call__(self, hostname: str) -> bool: ...

class ReadOnly:
    """
    Set a field readonly.

    Validation fails if the form data is different than the
    field object data, or if unset, from the field default data.
    """

    def __call__(self, form: BaseForm, field: Field) -> None: ...

class Disabled:
    """
    Set a field disabled.

    Validation fails if the form data has any value.
    """

    def __call__(self, form: BaseForm, field: Field) -> None: ...

email = Email
equal_to = EqualTo
ip_address = IPAddress
mac_address = MacAddress
length = Length
number_range = NumberRange
optional = Optional
input_required = InputRequired
data_required = DataRequired
regexp = Regexp
url = URL
any_of = AnyOf
none_of = NoneOf
readonly = ReadOnly
disabled = Disabled
