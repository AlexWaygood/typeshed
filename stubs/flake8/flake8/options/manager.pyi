"""Option handling and Option management logic."""

import argparse
from _typeshed import Incomplete
from collections.abc import Callable, Sequence
from enum import Enum
from logging import Logger
from typing import Any

from ..plugins.finder import Plugins

LOG: Logger

class _ARG(Enum):
    NO = 1

class Option:
    """Our wrapper around an argparse argument parsers to add features."""

    short_option_name: Incomplete
    long_option_name: Incomplete
    option_args: Incomplete
    action: Incomplete
    default: Incomplete
    type: Incomplete
    dest: Incomplete
    nargs: Incomplete
    const: Incomplete
    choices: Incomplete
    help: Incomplete
    metavar: Incomplete
    required: Incomplete
    option_kwargs: Incomplete
    parse_from_config: Incomplete
    comma_separated_list: Incomplete
    normalize_paths: Incomplete
    config_name: Incomplete
    def __init__(
        self,
        short_option_name: str | _ARG = ...,
        long_option_name: str | _ARG = ...,
        action: str | type[argparse.Action] | _ARG = ...,
        default: Any | _ARG = ...,
        type: Callable[..., Any] | _ARG = ...,
        dest: str | _ARG = ...,
        nargs: int | str | _ARG = ...,
        const: Any | _ARG = ...,
        choices: Sequence[Any] | _ARG = ...,
        help: str | _ARG = ...,
        metavar: str | _ARG = ...,
        required: bool | _ARG = ...,
        parse_from_config: bool = False,
        comma_separated_list: bool = False,
        normalize_paths: bool = False,
    ) -> None:
        """Initialize an Option instance.

        The following are all passed directly through to argparse.

        :param short_option_name:
            The short name of the option (e.g., ``-x``). This will be the
            first argument passed to ``ArgumentParser.add_argument``
        :param long_option_name:
            The long name of the option (e.g., ``--xtra-long-option``). This
            will be the second argument passed to
            ``ArgumentParser.add_argument``
        :param default:
            Default value of the option.
        :param dest:
            Attribute name to store parsed option value as.
        :param nargs:
            Number of arguments to parse for this option.
        :param const:
            Constant value to store on a common destination. Usually used in
            conjunction with ``action="store_const"``.
        :param choices:
            Possible values for the option.
        :param help:
            Help text displayed in the usage information.
        :param metavar:
            Name to use instead of the long option name for help text.
        :param required:
            Whether this option is required or not.

        The following options may be passed directly through to :mod:`argparse`
        but may need some massaging.

        :param type:
            A callable to normalize the type (as is the case in
            :mod:`argparse`).
        :param action:
            Any action allowed by :mod:`argparse`.

        The following parameters are for Flake8's option handling alone.

        :param parse_from_config:
            Whether or not this option should be parsed out of config files.
        :param comma_separated_list:
            Whether the option is a comma separated list when parsing from a
            config file.
        :param normalize_paths:
            Whether the option is expecting a path or list of paths and should
            attempt to normalize the paths to absolute paths.
        """

    @property
    def filtered_option_kwargs(self) -> dict[str, Any]:
        """Return any actually-specified arguments."""

    def normalize(self, value: Any, *normalize_args: str) -> Any:
        """Normalize the value based on the option configuration."""

    def to_argparse(self) -> tuple[list[str], dict[str, Any]]:
        """Convert a Flake8 Option to argparse ``add_argument`` arguments."""

class OptionManager:
    """Manage Options and OptionParser while adding post-processing."""

    formatter_names: Incomplete
    parser: Incomplete
    config_options_dict: Incomplete
    options: Incomplete
    extended_default_ignore: Incomplete
    extended_default_select: Incomplete
    def __init__(
        self, *, version: str, plugin_versions: str, parents: list[argparse.ArgumentParser], formatter_names: list[str]
    ) -> None:
        """Initialize an instance of an OptionManager."""

    def register_plugins(self, plugins: Plugins) -> None:
        """Register the plugin options (if needed)."""

    def add_option(self, *args: Any, **kwargs: Any) -> None:
        """Create and register a new option.

        See parameters for :class:`~flake8.options.manager.Option` for
        acceptable arguments to this method.

        .. note::

            ``short_option_name`` and ``long_option_name`` may be specified
            positionally as they are with argparse normally.
        """

    def extend_default_ignore(self, error_codes: Sequence[str]) -> None:
        """Extend the default ignore list with the error codes provided.

        :param error_codes:
            List of strings that are the error/warning codes with which to
            extend the default ignore list.
        """

    def extend_default_select(self, error_codes: Sequence[str]) -> None:
        """Extend the default select list with the error codes provided.

        :param error_codes:
            List of strings that are the error/warning codes with which
            to extend the default select list.
        """

    def parse_args(self, args: Sequence[str] | None = None, values: argparse.Namespace | None = None) -> argparse.Namespace:
        """Proxy to calling the OptionParser's parse_args method."""
