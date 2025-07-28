import json
from collections.abc import Callable, Generator, Iterator
from typing import Any

from docker._types import JSON

json_decoder: json.JSONDecoder

def stream_as_text(stream: Iterator[str | bytes]) -> Generator[str]:
    """
    Given a stream of bytes or text, if any of the items in the stream
    are bytes convert them to text.
    This function can be removed once we return text streams
    instead of byte streams.
    """

def json_splitter(buffer: str) -> tuple[JSON, str] | None:
    """Attempt to parse a json object from a buffer. If there is at least one
    object, return it and the rest of the buffer, otherwise return None.
    """

def json_stream(stream: Iterator[str]) -> Generator[JSON]:
    """Given a stream of text, return a stream of json objects.
    This handles streams which are inconsistently buffered (some entries may
    be newline delimited, and others are not).
    """

def line_splitter(buffer: str, separator: str = "\n") -> tuple[str, str] | None: ...
def split_buffer(
    stream: Iterator[str | bytes], splitter: Callable[[str], tuple[str, str]] | None = None, decoder: Callable[[str], Any] = ...
) -> Generator[Any]:
    """Given a generator which yields strings and a splitter function,
    joins all input, splits on the separator and yields each chunk.
    Unlike string.split(), each chunk includes the trailing
    separator, except for the last one if none was found on the end
    of the input.
    """
