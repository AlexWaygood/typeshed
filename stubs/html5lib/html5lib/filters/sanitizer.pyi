"""Deprecated from html5lib 1.1.

See `here <https://github.com/html5lib/html5lib-python/issues/443>`_ for
information about its deprecation; `Bleach <https://github.com/mozilla/bleach>`_
is recommended as a replacement. Please let us know in the aforementioned issue
if Bleach is unsuitable for your needs.

"""

import re
from collections.abc import Iterable
from typing_extensions import deprecated

from . import base

__all__ = ["Filter"]

allowed_elements: frozenset[tuple[str, str]]
allowed_attributes: frozenset[tuple[None, str] | tuple[str, str]]
attr_val_is_uri: frozenset[tuple[None, str] | tuple[str, str]]
svg_attr_val_allows_ref: frozenset[tuple[None, str]]
svg_allow_local_href: frozenset[tuple[None, str]]
allowed_css_properties: frozenset[str]
allowed_css_keywords: frozenset[str]
allowed_svg_properties: frozenset[str]
allowed_protocols: frozenset[str]
allowed_content_types: frozenset[str]
data_content_type: re.Pattern[str]

@deprecated("html5lib's sanitizer is deprecated; see https://github.com/html5lib/html5lib-python/issues/443")
class Filter(base.Filter):
    """Sanitizes token stream of XHTML+MathML+SVG and of inline style attributes"""

    allowed_elements: Iterable[tuple[str | None, str]]
    allowed_attributes: Iterable[tuple[str | None, str]]
    allowed_css_properties: Iterable[str]
    allowed_css_keywords: Iterable[str]
    allowed_svg_properties: Iterable[str]
    allowed_protocols: Iterable[str]
    allowed_content_types: Iterable[str]
    attr_val_is_uri: Iterable[tuple[str | None, str]]
    svg_attr_val_allows_ref: Iterable[tuple[str | None, str]]
    svg_allow_local_href: Iterable[tuple[str | None, str]]
    def __init__(
        self,
        source,
        allowed_elements: Iterable[tuple[str | None, str]] = ...,
        allowed_attributes: Iterable[tuple[str | None, str]] = ...,
        allowed_css_properties: Iterable[str] = ...,
        allowed_css_keywords: Iterable[str] = ...,
        allowed_svg_properties: Iterable[str] = ...,
        allowed_protocols: Iterable[str] = ...,
        allowed_content_types: Iterable[str] = ...,
        attr_val_is_uri: Iterable[tuple[str | None, str]] = ...,
        svg_attr_val_allows_ref: Iterable[tuple[str | None, str]] = ...,
        svg_allow_local_href: Iterable[tuple[str | None, str]] = ...,
    ) -> None:
        """Creates a Filter

        :arg allowed_elements: set of elements to allow--everything else will
            be escaped

        :arg allowed_attributes: set of attributes to allow in
            elements--everything else will be stripped

        :arg allowed_css_properties: set of CSS properties to allow--everything
            else will be stripped

        :arg allowed_css_keywords: set of CSS keywords to allow--everything
            else will be stripped

        :arg allowed_svg_properties: set of SVG properties to allow--everything
            else will be removed

        :arg allowed_protocols: set of allowed protocols for URIs

        :arg allowed_content_types: set of allowed content types for ``data`` URIs.

        :arg attr_val_is_uri: set of attributes that have URI values--values
            that have a scheme not listed in ``allowed_protocols`` are removed

        :arg svg_attr_val_allows_ref: set of SVG attributes that can have
            references

        :arg svg_allow_local_href: set of SVG elements that can have local
            hrefs--these are removed

        """

    def __iter__(self): ...
    def sanitize_token(self, token): ...
    def allowed_token(self, token): ...
    def disallowed_token(self, token): ...
    def sanitize_css(self, style: str) -> str: ...
