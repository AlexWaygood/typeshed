"""
Shim module between Bleach and html5lib. This makes it easier to upgrade the
html5lib library without having to change a lot of code.
"""

import re
from codecs import CodecInfo
from collections.abc import Generator, Iterable, Iterator
from typing import Any, Final, Protocol

# We don't re-export any `html5lib` types / values here, because they are not
# really public and may change at any time. This is just a helper module,
# import things directly from `html5lib` instead!
from html5lib import HTMLParser
from html5lib._inputstream import HTMLBinaryInputStream, HTMLUnicodeInputStream
from html5lib._tokenizer import HTMLTokenizer
from html5lib._trie import Trie
from html5lib.serializer import HTMLSerializer
from html5lib.treewalkers.base import TreeWalker

# Is actually webencodings.Encoding
class _Encoding(Protocol):
    name: str
    codec_info: CodecInfo
    def __init__(self, name: str, codec_info: CodecInfo) -> None: ...

HTML_TAGS: Final[frozenset[str]]
HTML_TAGS_BLOCK_LEVEL: Final[frozenset[str]]
AMP_SPLIT_RE: Final[re.Pattern[str]]
ENTITIES: Final[dict[str, str]]
ENTITIES_TRIE: Final[Trie]
TAG_TOKEN_TYPES: Final[set[int]]
TAG_TOKEN_TYPE_CHARACTERS: Final[int]
TAG_TOKEN_TYPE_END: Final[int]
TAG_TOKEN_TYPE_PARSEERROR: Final[int]
TAG_TOKEN_TYPE_START: Final[int]

class InputStreamWithMemory:
    """Wraps an HTMLInputStream to remember characters since last <

    This wraps existing HTMLInputStream classes to keep track of the stream
    since the last < which marked an open tag state.

    """

    position = HTMLUnicodeInputStream.position
    reset = HTMLUnicodeInputStream.reset
    def __init__(self, inner_stream: HTMLUnicodeInputStream) -> None: ...
    @property
    def errors(self) -> list[str]: ...
    @property
    def charEncoding(self) -> tuple[_Encoding, str]: ...
    # If inner_stream wasn't a HTMLBinaryInputStream, this will error at runtime
    # Is a property returning a method, simplified:
    changeEncoding = HTMLBinaryInputStream.changeEncoding
    def char(self) -> str: ...
    def charsUntil(self, characters: Iterable[str], opposite: bool = False) -> str: ...
    def unget(self, char: str | None) -> None: ...
    def get_tag(self) -> str:
        """Returns the stream history since last '<'

        Since the buffer starts at the last '<' as as seen by tagOpenState(),
        we know that everything from that point to when this method is called
        is the "tag" that is being tokenized.

        """

    def start_tag(self) -> None:
        """Resets stream history to just '<'

        This gets called by tagOpenState() which marks a '<' that denotes an
        open tag. Any time we see that, we reset the buffer.

        """

class BleachHTMLTokenizer(HTMLTokenizer):
    """Tokenizer that doesn't consume character entities"""

    consume_entities: bool
    stream: InputStreamWithMemory
    emitted_last_token: dict[str, Any] | None
    def __init__(self, consume_entities: bool = False, **kwargs: Any) -> None: ...

class BleachHTMLParser(HTMLParser):
    """Parser that uses BleachHTMLTokenizer"""

    tags: list[str] | None
    strip: bool
    consume_entities: bool
    def __init__(self, tags: Iterable[str] | None, strip: bool, consume_entities: bool, **kwargs: Any) -> None:
        """
        :arg tags: set of allowed tags--everything else is either stripped or
            escaped; if None, then this doesn't look at tags at all
        :arg strip: whether to strip disallowed tags (True) or escape them (False);
            if tags=None, then this doesn't have any effect
        :arg consume_entities: whether to consume entities (default behavior) or
            leave them as is when tokenizing (BleachHTMLTokenizer-added behavior)

        """

class BleachHTMLSerializer(HTMLSerializer):
    """HTMLSerializer that undoes & -> &amp; in attributes and sets
    escape_rcdata to True
    """

    escape_rcdata: bool
    def escape_base_amp(self, stoken: str) -> Generator[str, None, None]:
        """Escapes just bare & in HTML attribute values"""

    def serialize(self, treewalker: TreeWalker, encoding: str | None = None) -> Generator[str, None, None]:  # type: ignore[override]
        """Wrap HTMLSerializer.serialize and conver & to &amp; in attribute values

        Note that this converts & to &amp; in attribute values where the & isn't
        already part of an unambiguous character entity.

        """

def convert_entity(value: str) -> str | None:
    """Convert an entity (minus the & and ; part) into what it represents

    This handles numeric, hex, and text entities.

    :arg value: the string (minus the ``&`` and ``;`` part) to convert

    :returns: unicode character or None if it's an ambiguous ampersand that
        doesn't match a character entity

    """

def convert_entities(text: str) -> str:
    """Converts all found entities in the text

    :arg text: the text to convert entities in

    :returns: unicode text with converted entities

    """

def match_entity(stream: str) -> str | None:
    """Returns first entity in stream or None if no entity exists

    Note: For Bleach purposes, entities must start with a "&" and end with a
    ";". This ignores ambiguous character entities that have no ";" at the end.

    :arg stream: the character stream

    :returns: the entity string without "&" or ";" if it's a valid character
        entity; ``None`` otherwise

    """

def next_possible_entity(text: str) -> Iterator[str]:
    """Takes a text and generates a list of possible entities

    :arg text: the text to look at

    :returns: generator where each part (except the first) starts with an
        "&"

    """
