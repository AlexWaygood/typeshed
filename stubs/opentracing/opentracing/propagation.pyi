from typing import Final

class UnsupportedFormatException(Exception):
    """UnsupportedFormatException should be used when the provided format
    value is unknown or disallowed by the :class:`Tracer`.

    See :meth:`Tracer.inject()` and :meth:`Tracer.extract()`.
    """

class InvalidCarrierException(Exception):
    """InvalidCarrierException should be used when the provided carrier
    instance does not match what the `format` argument requires.

    See :meth:`Tracer.inject()` and :meth:`Tracer.extract()`.
    """

class SpanContextCorruptedException(Exception):
    """SpanContextCorruptedException should be used when the underlying
    :class:`SpanContext` state is seemingly present but not well-formed.

    See :meth:`Tracer.inject()` and :meth:`Tracer.extract()`.
    """

class Format:
    """A namespace for builtin carrier formats.

    These static constants are intended for use in the :meth:`Tracer.inject()`
    and :meth:`Tracer.extract()` methods. E.g.::

        tracer.inject(span.context, Format.BINARY, binary_carrier)

    """

    BINARY: Final = "binary"
    TEXT_MAP: Final = "text_map"
    HTTP_HEADERS: Final = "http_headers"
