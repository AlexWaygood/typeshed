"""
Misc utility functions and constants
"""

from collections.abc import Callable, Iterable, Mapping
from typing import Any, NoReturn, TypedDict, TypeVar
from typing_extensions import NotRequired

class _DeprecateProperty(TypedDict):
    to_be_removed_in_version: str
    client_property: str
    new_property: NotRequired[str]

_T = TypeVar("_T")
_K = TypeVar("_K")
_V = TypeVar("_V")

def raise_for_error(
    method: str,
    url: str,
    status_code: int,
    message: str | None = None,
    errors: Iterable[str] | str | None = None,
    text: str | None = None,
    json: object | None = None,
) -> NoReturn:
    """Helper method to raise exceptions based on the status code of a response received back from Vault.

    :param method: HTTP method of a request to Vault.
    :type method: str
    :param url: URL of the endpoint requested in Vault.
    :type url: str
    :param status_code: Status code received in a response from Vault.
    :type status_code: int
    :param message: Optional message to include in a resulting exception.
    :type message: str
    :param errors: Optional errors to include in a resulting exception.
    :type errors: list | str
    :param text: Optional text of the response.
    :type text: str
    :param json: Optional deserialized version of a JSON response (object)
    :type json: object

    :raises: hvac.exceptions.InvalidRequest | hvac.exceptions.Unauthorized | hvac.exceptions.Forbidden |
        hvac.exceptions.InvalidPath | hvac.exceptions.RateLimitExceeded | hvac.exceptions.InternalServerError |
        hvac.exceptions.VaultNotInitialized | hvac.exceptions.BadGateway | hvac.exceptions.VaultDown |
        hvac.exceptions.UnexpectedError

    """

def aliased_parameter(
    name: str, *aliases: str, removed_in_version: str | None, position: int | None = None, raise_on_multiple: bool = True
) -> Callable[..., Any]:
    """A decorator that can be used to define one or more aliases for a parameter,
    and optionally display a deprecation warning when aliases are used.
    It can also optionally raise an exception if a value is supplied via multiple names.
    LIMITATIONS:
    If the canonical parameter can be specified unnamed (positionally),
    then its position must be set to correctly detect multiple use and apply precedence.
    To set multiple aliases with different values for the optional parameters, use the decorator multiple times with the same name.
    This method will only work properly when the alias parameter is set as a keyword (named) arg, therefore the function in question
    should ensure that any aliases come after \\*args or bare \\* (marking keyword-only arguments: https://peps.python.org/pep-3102/).
    Note also that aliases do not have to appear in the original function's argument list.

    :param name: The canonical name of the parameter.
    :type name: str
    :param aliases: One or more alias names for the parameter.
    :type aliases: str
    :param removed_in_version: The version in which the alias will be removed. This should typically have a value.
        In the rare case that an alias is not deprecated, set this to None.
    :type removed_in_version: str | None
    :param position: The 0-based position of the canonical argument if it could be specified positionally. Use None for a keyword-only (named) argument.
    :type position: int
    :param raise_on_multiple: When True (default), raise an exception if a value is supplied via multiple names.
    :type raise_on_multiple: bool
    """

def generate_parameter_deprecation_message(
    to_be_removed_in_version: str, old_parameter_name: str, new_parameter_name: str | None = None, extra_notes: str | None = None
) -> str:
    """Generate a message to be used when warning about the use of deprecated paramers.

    :param to_be_removed_in_version: Version of this module the deprecated parameter will be removed in.
    :type to_be_removed_in_version: str
    :param old_parameter_name: Deprecated parameter name.
    :type old_parameter_name: str
    :param new_parameter_name: Parameter intended to replace the deprecated parameter, if applicable.
    :type new_parameter_name: str | None
    :param extra_notes: Optional freeform text used to provide additional context, alternatives, or notes.
    :type extra_notes: str | None
    :return: Full deprecation warning message for the indicated parameter.
    :rtype: str
    """

def generate_method_deprecation_message(
    to_be_removed_in_version: str, old_method_name: str, method_name: str | None = None, module_name: str | None = None
) -> str:
    """Generate a message to be used when warning about the use of deprecated methods.

    :param to_be_removed_in_version: Version of this module the deprecated method will be removed in.
    :type to_be_removed_in_version: str
    :param old_method_name: Deprecated method name.
    :type old_method_name:  str
    :param method_name:  Method intended to replace the deprecated method indicated. This method's docstrings are
        included in the decorated method's docstring.
    :type method_name: str
    :param module_name: Name of the module containing the new method to use.
    :type module_name: str
    :return: Full deprecation warning message for the indicated method.
    :rtype: str
    """

def generate_property_deprecation_message(
    to_be_removed_in_version: str, old_name: str, new_name: str, new_attribute: str, module_name: str = "Client"
) -> str:
    """Generate a message to be used when warning about the use of deprecated properties.

    :param to_be_removed_in_version: Version of this module the deprecated property will be removed in.
    :type to_be_removed_in_version: str
    :param old_name: Deprecated property name.
    :type old_name: str
    :param new_name: Name of the new property name to use.
    :type new_name: str
    :param new_attribute: The new attribute where the new property can be found.
    :type new_attribute: str
    :param module_name: Name of the module containing the new method to use.
    :type module_name: str
    :return: Full deprecation warning message for the indicated property.
    :rtype: str
    """

def getattr_with_deprecated_properties(obj: object, item: str, deprecated_properties: dict[str, _DeprecateProperty]) -> Any:
    """Helper method to use in the getattr method of a class with deprecated properties.

    :param obj: Instance of the Class containing the deprecated properties in question.
    :type obj: object
    :param item: Name of the attribute being requested.
    :type item: str
    :param deprecated_properties: Dict of deprecated properties. Each key is the name of the old property.
        Each value is a dict with at least a "to_be_removed_in_version" and "client_property" key to be
        used in the displayed deprecation warning. An optional "new_property" key contains the name of
        the new property within the "client_property", otherwise the original name is used.
    :type deprecated_properties: Dict
    :return: The new property indicated where available.
    :rtype: object
    """

def deprecated_method(to_be_removed_in_version: str, new_method: Callable[..., Any] | None = None) -> Callable[..., Any]:
    """This is a decorator which can be used to mark methods as deprecated. It will result in a warning being emitted
    when the function is used.

    :param to_be_removed_in_version: Version of this module the decorated method will be removed in.
    :type to_be_removed_in_version: str
    :param new_method: Method intended to replace the decorated method. This method's docstrings are included in the
        decorated method's docstring.
    :type new_method: function
    :return: Wrapped function that includes a deprecation warning and update docstrings from the replacement method.
    :rtype: types.FunctionType
    """

def validate_list_of_strings_param(param_name: str, param_argument: Iterable[Any] | str) -> None:
    """Validate that an argument is a list of strings.
    Returns nothing if valid, raises ParamValidationException if invalid.

    :param param_name: The name of the parameter being validated. Used in any resulting exception messages.
    :type param_name: str | unicode
    :param param_argument: The argument to validate.
    :type param_argument: list
    """

def list_to_comma_delimited(list_param: Iterable[str] | None) -> str:
    """Convert a list of strings into a comma-delimited list / string.

    :param list_param: A list of strings.
    :type list_param: list
    :return: Comma-delimited string.
    :rtype: str
    """

def get_token_from_env() -> str | None:
    """Get the token from env var, VAULT_TOKEN. If not set, attempt to get the token from, ~/.vault-token

    :return: The vault token if set, else None
    :rtype: str | None
    """

def comma_delimited_to_list(list_param: Iterable[_T]) -> Iterable[_T]:
    """Convert comma-delimited list / string into a list of strings

    :param list_param: Comma-delimited string
    :type list_param: str | unicode
    :return: A list of strings
    :rtype: list
    """

# the docstring states that this function returns a bool, but the code does not return anything
def validate_pem_format(param_name: str, param_argument: str) -> None:
    """Validate that an argument is a PEM-formatted public key or certificate

    :param param_name: The name of the parameter being validate. Used in any resulting exception messages.
    :type param_name: str | unicode
    :param param_argument: The argument to validate
    :type param_argument: str | unicode
    :return: True if the argument is validate False otherwise
    :rtype: bool
    """

def remove_nones(params: Mapping[_K, _V | None]) -> Mapping[_K, _V]:
    """Removes None values from optional arguments in a parameter dictionary.

    :param params: The dictionary of parameters to be filtered.
    :type params: dict
    :return: A filtered copy of the parameter dictionary.
    :rtype: dict
    """

def format_url(
    format_str: str, *args: object, **kwargs: object
) -> str:  # values are passed to builtins.str, which takes an object type
    """Creates a URL using the specified format after escaping the provided arguments.

    :param format_str: The URL containing replacement fields.
    :type format_str: str
    :param kwargs: Positional replacement field values.
    :type kwargs: list
    :param kwargs: Named replacement field values.
    :type kwargs: dict
    :return: The formatted URL path with escaped replacement fields.
    :rtype: str
    """
