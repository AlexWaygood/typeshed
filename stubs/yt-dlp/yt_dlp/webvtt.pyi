"""
A partial parser for WebVTT segments. Interprets enough of the WebVTT stream
to be able to assemble a single stand-alone subtitle file, suitably adjusting
timestamps on the way, while everything else is passed through unmodified.

Regular expressions based on the W3C WebVTT specification
<https://www.w3.org/TR/webvtt1/>. The X-TIMESTAMP-MAP extension is described
in RFC 8216 §3.5 <https://tools.ietf.org/html/rfc8216#section-3.5>.
"""

import re
from collections.abc import Generator, Mapping
from typing import Any, TextIO, TypeVar

_AT = TypeVar("_AT", int, str, re.Match[str], None)

class _MatchParser:
    """
    An object that maintains the current parsing position and allows
    conveniently advancing it as syntax elements are successfully parsed.
    """

    def __init__(self, string: str) -> None: ...
    def match(self, r: re.Pattern[str]) -> re.Match[str] | int | None: ...
    def advance(self, by: _AT) -> _AT: ...
    def consume(self, r: re.Pattern[str]) -> re.Match[str]: ...
    def child(self) -> _MatchChildParser: ...

class _MatchChildParser(_MatchParser):
    """
    A child parser state, which advances through the same data as
    its parent, but has an independent position. This is useful when
    advancing through syntax elements we might later want to backtrack
    from.
    """

    def __init__(self, parent: _MatchParser) -> None: ...
    def commit(self) -> _MatchParser:
        """
        Advance the parent state to the current position of this child state.
        """

class ParseError(Exception):
    def __init__(self, parser: _MatchParser) -> None: ...

class Block:
    """
    An abstract WebVTT block.
    """

    def __init__(self, **kwargs: Any) -> None: ...  # Abstract. Accepts arbitrary keyword arguments.
    @classmethod
    def parse(cls, parser: _MatchParser) -> Block: ...
    def write_into(self, stream: TextIO) -> None: ...

class HeaderBlock(Block):
    """
    A WebVTT block that may only appear in the header part of the file,
    i.e. before any cue blocks.
    """

class Magic(HeaderBlock):
    @classmethod
    def parse(cls, parser: _MatchParser) -> Magic: ...
    def write_into(self, stream: TextIO) -> None: ...

class StyleBlock(HeaderBlock): ...
class RegionBlock(HeaderBlock): ...
class CommentBlock(Block): ...

class CueBlock(Block):
    """
    A cue block. The payload is not interpreted.
    """

    @classmethod
    def parse(cls, parser: _MatchParser) -> CueBlock: ...
    def write_into(self, stream: TextIO) -> None: ...
    @property
    def as_json(self) -> dict[str, Any]: ...
    def __eq__(self, other: object) -> bool: ...
    @classmethod
    def from_json(cls, json: Mapping[str, Any]) -> CueBlock: ...
    def hinges(self, other: Block) -> bool: ...

def parse_fragment(frag_content: bytes) -> Generator[Block]:
    """
    A generator that yields (partially) parsed WebVTT blocks when given
    a bytes object containing the raw contents of a WebVTT file.
    """
