"""
Markdown accepts an [`Extension`][markdown.extensions.Extension] instance for each extension. Therefore, each extension
must to define a class that extends [`Extension`][markdown.extensions.Extension] and over-rides the
[`extendMarkdown`][markdown.extensions.Extension.extendMarkdown] method. Within this class one can manage configuration
options for their extension and attach the various processors and patterns which make up an extension to the
[`Markdown`][markdown.Markdown] instance.
"""

from collections.abc import Iterable, Mapping
from typing import Any

from markdown.core import Markdown

class Extension:
    """Base class for extensions to subclass."""

    config: Mapping[str, list[Any]]
    def __init__(self, **kwargs: Any) -> None:
        """Initiate Extension and set up configs."""

    def getConfig(self, key: str, default: Any = "") -> Any:
        """
        Return a single configuration option value.

        Arguments:
            key: The configuration option name.
            default: Default value to return if key is not set.

        Returns:
            Value of stored configuration option.
        """

    def getConfigs(self) -> dict[str, Any]:
        """
        Return all configuration options.

        Returns:
            All configuration options.
        """

    def getConfigInfo(self) -> list[tuple[str, str]]:
        """
        Return descriptions of all configuration options.

        Returns:
            All descriptions of configuration options.
        """

    def setConfig(self, key: str, value: Any) -> None:
        """
        Set a configuration option.

        If the corresponding default value set in [`config`][markdown.extensions.Extension.config]
        is a `bool` value or `None`, then `value` is passed through
        [`parseBoolValue`][markdown.util.parseBoolValue] before being stored.

        Arguments:
            key: Name of configuration option to set.
            value: Value to assign to option.

        Raises:
            KeyError: If `key` is not known.
        """

    def setConfigs(self, items: Mapping[str, Any] | Iterable[tuple[str, Any]]) -> None:
        """
        Loop through a collection of configuration options, passing each to
        [`setConfig`][markdown.extensions.Extension.setConfig].

        Arguments:
            items: Collection of configuration options.

        Raises:
            KeyError: for any unknown key.
        """

    def extendMarkdown(self, md: Markdown) -> None:
        """
        Add the various processors and patterns to the Markdown Instance.

        This method must be overridden by every extension.

        Arguments:
            md: The Markdown instance.

        """
