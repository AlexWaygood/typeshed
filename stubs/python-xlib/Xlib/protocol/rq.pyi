from _typeshed import ConvertibleToInt, SliceableBuffer, Unused
from array import array

# Avoid name collision with List.type
from builtins import type as Type
from collections.abc import Callable, Iterable, Sequence
from typing import Any, Final, Literal, SupportsIndex, TypeVar, overload, type_check_only
from typing_extensions import LiteralString, TypeAlias

from Xlib._typing import ErrorHandler
from Xlib.display import _BaseDisplay, _ResourceBaseClass
from Xlib.error import XError
from Xlib.ext.xinput import ClassInfoClass
from Xlib.protocol import display

_T = TypeVar("_T")
_ModifierMappingList8Elements: TypeAlias = Sequence[Sequence[int]]

def decode_string(bs: bytes | bytearray) -> str: ...
def encode_array(a: array[Any] | memoryview) -> str: ...

class BadDataError(Exception): ...

signed_codes: Final[dict[int, str]]
unsigned_codes: Final[dict[int, str]]
array_unsigned_codes: Final[dict[int, LiteralString]]
struct_to_array_codes: Final[dict[str, LiteralString]]

class Field:
    """Field objects represent the data fields of a Struct.

    Field objects must have the following attributes:

       name         -- the field name, or None
       structcode   -- the struct codes representing this field
       structvalues -- the number of values encodes by structcode

    Additionally, these attributes should either be None or real methods:

       check_value  -- check a value before it is converted to binary
       parse_value  -- parse a value after it has been converted from binary

    If one of these attributes are None, no check or additional
    parsings will be done one values when converting to or from binary
    form.  Otherwise, the methods should have the following behaviour:

       newval = check_value(val)
         Check that VAL is legal when converting to binary form.  The
         value can also be converted to another Python value.  In any
         case, return the possibly new value.  NEWVAL should be a
         single Python value if structvalues is 1, a tuple of
         structvalues elements otherwise.

       newval = parse_value(val, display)
         VAL is an unpacked Python value, which now can be further
         refined.  DISPLAY is the current Display object.  Return the
         new value.  VAL will be a single value if structvalues is 1,
         a tuple of structvalues elements otherwise.

    If `structcode' is None the Field must have the method
    f.parse_binary_value() instead.  See its documentation string for
    details.
    """

    name: str
    default: int | None
    pack_value: Callable[[Any], tuple[Any, int | None, int | None]] | None
    structcode: str | None
    structvalues: int
    check_value: Callable[[Any], Any] | None
    parse_value: Callable[[Any, Any], Any] | None
    keyword_args: int

    def parse_binary_value(
        self, data: SliceableBuffer, display: display.Display | None, length: int | None, format: int
    ) -> tuple[Any, SliceableBuffer]:
        """value, remaindata = f.parse_binary_value(data, display, length, format)

        Decode a value for this field from the binary string DATA.
        If there are a LengthField and/or a FormatField connected to this
        field, their values will be LENGTH and FORMAT, respectively.  If
        there are no such fields the parameters will be None.

        DISPLAY is the display involved, which is really only used by
        the Resource fields.

        The decoded value is returned as VALUE, and the remaining part
        of DATA shold be returned as REMAINDATA.
        """

class Pad(Field):
    size: int
    value: bytes
    structcode: str
    def __init__(self, size: int) -> None: ...

class ConstantField(Field):
    value: int
    def __init__(self, value: int) -> None: ...

class Opcode(ConstantField):
    structcode: str

class ReplyCode(ConstantField):
    structcode: str
    value: int
    def __init__(self) -> None: ...

class LengthField(Field):
    """A LengthField stores the length of some other Field whose size
    may vary, e.g. List and String8.

    Its name should be the same as the name of the field whose size
    it stores.  The other_fields attribute can be used to specify the
    names of other fields whose sizes are stored by this field, so
    a single length field can set the length of multiple fields.

    The lf.get_binary_value() method of LengthFields is not used, instead
    a lf.get_binary_length() should be provided.

    Unless LengthField.get_binary_length() is overridden in child classes,
    there should also be a lf.calc_length().
    """

    structcode: str
    other_fields: list[str] | tuple[str, ...] | None
    def calc_length(self, length: int) -> int:
        """newlen = lf.calc_length(length)

        Return a new length NEWLEN based on the provided LENGTH.
        """

class TotalLengthField(LengthField): ...
class RequestLength(TotalLengthField): ...
class ReplyLength(TotalLengthField): ...

class LengthOf(LengthField):
    other_fields: list[str] | tuple[str, ...] | None
    def __init__(self, name: str | list[str] | tuple[str, ...], size: int) -> None: ...

class OddLength(LengthField):
    def __init__(self, name: str) -> None: ...
    def parse_value(self, value: int, display: Unused) -> Literal["even", "odd"]: ...  # type: ignore[override]

class FormatField(Field):
    """A FormatField encodes the format of some other field, in a manner
    similar to LengthFields.

    The ff.get_binary_value() method is not used, replaced by
    ff.get_binary_format().
    """

    structcode: str
    def __init__(self, name: str, size: int) -> None: ...

Format = FormatField

class ValueField(Field):
    def __init__(self, name: str, default: int | None = None) -> None: ...

class Int8(ValueField):
    structcode: str

class Int16(ValueField):
    structcode: str

class Int32(ValueField):
    structcode: str

class Card8(ValueField):
    structcode: str

class Card16(ValueField):
    structcode: str

class Card32(ValueField):
    structcode: str

class Resource(Card32):
    cast_function: str
    class_name: str
    codes: tuple[int, ...]
    def __init__(self, name: str, codes: tuple[int, ...] = (), default: int | None = None) -> None: ...
    @overload  # type: ignore[override]
    def check_value(self, value: Callable[[], _T]) -> _T: ...
    @overload
    def check_value(self, value: _T) -> _T: ...
    def parse_value(self, value: int, display: _BaseDisplay) -> int: ...  # type: ignore[override]  # display: None will error. See: https://github.com/python-xlib/python-xlib/pull/248

class Window(Resource):
    cast_function: str
    class_name: str

class Pixmap(Resource):
    cast_function: str
    class_name: str

class Drawable(Resource):
    cast_function: str
    class_name: str

class Fontable(Resource):
    cast_function: str
    class_name: str

class Font(Resource):
    cast_function: str
    class_name: str

class GC(Resource):
    cast_function: str
    class_name: str

class Colormap(Resource):
    cast_function: str
    class_name: str

class Cursor(Resource):
    cast_function: str
    class_name: str

class Bool(ValueField):
    structcode: str
    def check_value(self, value: object) -> bool: ...  # type: ignore[override]

class Set(ValueField):
    structcode: str
    values: Sequence[object]
    def __init__(self, name: str, size: int, values: Sequence[object], default: int | None = None) -> None: ...
    def check_value(self, val: _T) -> _T: ...  # type: ignore[override]

class Gravity(Set):
    def __init__(self, name: str) -> None: ...

class FixedBinary(ValueField):
    structcode: str
    def __init__(self, name: str, size: int) -> None: ...

class Binary(ValueField):
    structcode: None
    pad: int
    def __init__(self, name: str, pad: int = 1) -> None: ...
    def pack_value(  # type: ignore[override]  # Override Callable
        self, val: bytes | bytearray
    ) -> tuple[bytes | bytearray, int, None]: ...
    @overload  # type: ignore[override]  # Overload for specific values
    def parse_binary_value(self, data: _T, display: Unused, length: None, format: Unused) -> tuple[_T, Literal[b""]]: ...
    @overload
    def parse_binary_value(
        self, data: SliceableBuffer, display: Unused, length: int, format: Unused
    ) -> tuple[SliceableBuffer, SliceableBuffer]: ...

class String8(ValueField):
    structcode: None
    pad: int
    def __init__(self, name: str, pad: int = 1) -> None: ...
    def pack_value(self, val: bytes | str) -> tuple[bytes, int, None]: ...  # type: ignore[override]  # Override Callable
    @overload  # type: ignore[override]  # Overload for specific values
    def parse_binary_value(
        self, data: bytes | bytearray, display: Unused, length: None, format: Unused
    ) -> tuple[str, Literal[b""]]: ...
    @overload
    def parse_binary_value(
        self, data: SliceableBuffer, display: Unused, length: int, format: Unused
    ) -> tuple[str, SliceableBuffer]: ...

class String16(ValueField):
    structcode: None
    pad: int
    def __init__(self, name: str, pad: int = 1) -> None: ...
    def pack_value(self, val: Sequence[object]) -> tuple[bytes, int, None]:  # type: ignore[override]  # Override Callable
        """Convert 8-byte string into 16-byte list"""

    def parse_binary_value(  # type: ignore[override]  # length: None will error. See: https://github.com/python-xlib/python-xlib/pull/248
        self, data: SliceableBuffer, display: Unused, length: int | Literal["odd", "even"], format: Unused
    ) -> tuple[tuple[Any, ...], SliceableBuffer]: ...

class List(ValueField):
    """The List, FixedList and Object fields store compound data objects.
    The type of data objects must be provided as an object with the
    following attributes and methods:

    ...

    """

    structcode: None
    type: Struct | ScalarObj | ResourceObj | ClassInfoClass | type[ValueField]
    pad: int
    def __init__(
        self, name: str, type: Struct | ScalarObj | ResourceObj | ClassInfoClass | Type[ValueField], pad: int = 1
    ) -> None: ...
    def parse_binary_value(
        self, data: SliceableBuffer, display: display.Display | None, length: SupportsIndex | None, format: Unused
    ) -> tuple[list[DictWrapper | None], SliceableBuffer]: ...
    def pack_value(  # type: ignore[override]  # Override Callable
        self, val: Sequence[object] | dict[str, Any]
    ) -> tuple[bytes, int, None]: ...

class FixedList(List):
    size: int
    def __init__(self, name: str, size: int, type: Struct | ScalarObj, pad: int = 1) -> None: ...
    def parse_binary_value(
        self, data: SliceableBuffer, display: display.Display | None, length: Unused, format: Unused
    ) -> tuple[list[DictWrapper | None], SliceableBuffer]: ...

class Object(ValueField):
    type: Struct
    structcode: str | None
    def __init__(self, name: str, type: Struct, default: int | None = None) -> None: ...
    def parse_binary_value(
        self, data: SliceableBuffer, display: display.Display | None, length: Unused, format: Unused
    ) -> tuple[DictWrapper, SliceableBuffer]: ...
    def parse_value(self, val: SliceableBuffer, display: display.Display | None) -> DictWrapper: ...  # type: ignore[override]
    def pack_value(  # type: ignore[override]  # Override Callable
        self, val: tuple[object, ...] | dict[str, Any] | DictWrapper
    ) -> bytes: ...
    def check_value(self, val: tuple[_T, ...] | dict[str, _T] | DictWrapper) -> list[_T]: ...  # type: ignore[override]

class PropertyData(ValueField):
    structcode: None
    def parse_binary_value(
        self, data: SliceableBuffer, display: Unused, length: ConvertibleToInt | None, format: int
    ) -> tuple[tuple[int, SliceableBuffer] | None, SliceableBuffer]: ...
    def pack_value(  # type: ignore[override]  # Override Callable
        self, value: tuple[int, Sequence[float] | Sequence[str]]
    ) -> tuple[bytes, int, Literal[8, 16, 32]]: ...

class FixedPropertyData(PropertyData):
    size: int
    def __init__(self, name: str, size: int) -> None: ...

class ValueList(Field):
    structcode: None
    keyword_args: int
    default: str  # type: ignore[assignment]  # Actually different from base class
    maskcode: bytes
    maskcodelen: int
    fields: list[tuple[Field, int]]
    def __init__(self, name: str, mask: int, pad: int, *fields: Field) -> None: ...
    def pack_value(  # type: ignore[override]  # Override Callable
        self, arg: str | dict[str, Any], keys: dict[str, Any]
    ) -> tuple[bytes, None, None]: ...
    def parse_binary_value(
        self, data: SliceableBuffer, display: display.Display | None, length: Unused, format: Unused
    ) -> tuple[DictWrapper, SliceableBuffer]: ...

class KeyboardMapping(ValueField):
    structcode: None
    def parse_binary_value(
        self, data: SliceableBuffer, display: Unused, length: int | None, format: int
    ) -> tuple[list[int], SliceableBuffer]: ...
    def pack_value(  # type: ignore[override]  # Override Callable
        self, value: Sequence[Sequence[object]]
    ) -> tuple[bytes, int, int]: ...

class ModifierMapping(ValueField):
    structcode: None
    def parse_binary_value(
        self, data: SliceableBuffer, display: Unused, length: Unused, format: int
    ) -> tuple[list[array[int]], SliceableBuffer]: ...
    def pack_value(  # type: ignore[override]  # Override Callable
        self, value: _ModifierMappingList8Elements
    ) -> tuple[bytes, int, int]: ...

class EventField(ValueField):
    structcode: None
    def pack_value(self, value: Event) -> tuple[SliceableBuffer, None, None]: ...  # type: ignore[override]  # Override Callable
    def parse_binary_value(  # type: ignore[override]
        self, data: SliceableBuffer, display: display.Display, length: Unused, format: Unused
    ) -> tuple[Event, SliceableBuffer]: ...

class ScalarObj:
    structcode: str
    structvalues: int
    parse_value: None
    check_value: None
    def __init__(self, code: str) -> None: ...

Card8Obj: ScalarObj
Card16Obj: ScalarObj
Card32Obj: ScalarObj

class ResourceObj:
    structcode: str
    structvalues: int
    class_name: str
    check_value: None
    def __init__(self, class_name: str) -> None: ...
    def parse_value(self, value: int, display: _BaseDisplay) -> int | _ResourceBaseClass: ...

WindowObj: ResourceObj
ColormapObj: ResourceObj

class StrClass:
    structcode: None
    def pack_value(self, val: str) -> bytes: ...
    def parse_binary(self, data: bytes | bytearray, display: Unused) -> tuple[str, bytes | bytearray]: ...

Str: StrClass

class Struct:
    """Struct objects represents a binary data structure.  It can
    contain both fields with static and dynamic sizes.  However, all
    static fields must appear before all dynamic fields.

    Fields are represented by various subclasses of the abstract base
    class Field.  The fields of a structure are given as arguments
    when instantiating a Struct object.

    Struct objects have two public methods:

      to_binary()    -- build a binary representation of the structure
                        with the values given as arguments
      parse_binary() -- convert a binary (string) representation into
                        a Python dictionary or object.

    These functions will be generated dynamically for each Struct
    object to make conversion as fast as possible.  They are
    generated the first time the methods are called.
    """

    name: str
    check_value: Callable[[Any], Any] | None
    keyword_args: bool
    fields: tuple[Field]
    static_codes: str
    static_values: int
    static_fields: list[Field]
    static_size: int
    var_fields: list[Field]
    structcode: str | None
    structvalues: int
    def __init__(self, *fields: Field) -> None: ...
    def to_binary(self, *varargs: object, **keys: object) -> bytes:
        """data = s.to_binary(...)

        Convert Python values into the binary representation.  The
        arguments will be all value fields with names, in the order
        given when the Struct object was instantiated.  With one
        exception: fields with default arguments will be last.

        Returns the binary representation as the string DATA.
        """

    def pack_value(self, value: tuple[object, ...] | dict[str, Any] | DictWrapper) -> bytes:
        """This function allows Struct objects to be used in List and
        Object fields.  Each item represents the arguments to pass to
        to_binary, either a tuple, a dictionary or a DictWrapper.

        """

    @overload
    def parse_value(self, val: SliceableBuffer, display: display.Display | None, rawdict: Literal[True]) -> dict[str, Any]:
        """This function is used by List and Object fields to convert
        Struct objects with no var_fields into Python values.

        """

    @overload
    def parse_value(
        self, val: SliceableBuffer, display: display.Display | None, rawdict: Literal[False] = False
    ) -> DictWrapper: ...
    @overload
    def parse_binary(
        self, data: SliceableBuffer, display: display.Display | None, rawdict: Literal[True]
    ) -> tuple[dict[str, Any], SliceableBuffer]:
        """values, remdata = s.parse_binary(data, display, rawdict = False)

        Convert a binary representation of the structure into Python values.

        DATA is a string or a buffer containing the binary data.
        DISPLAY should be a Xlib.protocol.display.Display object if
        there are any Resource fields or Lists with ResourceObjs.

        The Python values are returned as VALUES.  If RAWDICT is true,
        a Python dictionary is returned, where the keys are field
        names and the values are the corresponding Python value.  If
        RAWDICT is false, a DictWrapper will be returned where all
        fields are available as attributes.

        REMDATA are the remaining binary data, unused by the Struct object.

        """

    @overload
    def parse_binary(
        self, data: SliceableBuffer, display: display.Display | None, rawdict: Literal[False] = False
    ) -> tuple[DictWrapper, SliceableBuffer]: ...
    # Structs generate their attributes
    # TODO: Create a specific type-only class for all instances of `Struct`
    @type_check_only
    def __getattr__(self, name: str, /) -> Any: ...

class TextElements8(ValueField):
    string_textitem: Struct
    def pack_value(  # type: ignore[override]  # Override Callable
        self, value: Iterable[Field | str | bytes | tuple[Sequence[object], ...] | dict[str, Sequence[object]] | DictWrapper]
    ) -> tuple[bytes, None, None]: ...
    def parse_binary_value(  # type: ignore[override]  # See: https://github.com/python-xlib/python-xlib/pull/249
        self, data: SliceableBuffer, display: display.Display | None, length: Unused, format: Unused
    ) -> tuple[list[DictWrapper], Literal[""]]: ...

class TextElements16(TextElements8):
    string_textitem: Struct

class GetAttrData:
    # GetAttrData classes get their attributes dynamically
    # TODO: Complete all classes inheriting from GetAttrData
    def __getattr__(self, attr: str) -> Any: ...
    def __setattr__(self, name: str, value: Any, /) -> None: ...

class DictWrapper(GetAttrData):
    def __init__(self, dict: dict[str, Any]) -> None: ...
    def __getitem__(self, key: str) -> object: ...
    def __setitem__(self, key: str, value: object) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __setattr__(self, key: str, value: object) -> None: ...

class Request:
    def __init__(
        self, display: _BaseDisplay, onerror: ErrorHandler[object] | None = None, *args: object, **keys: object
    ) -> None: ...

class ReplyRequest(GetAttrData):
    def __init__(self, display: display.Display, defer: bool = False, *args: object, **keys: object) -> None: ...
    def reply(self) -> None: ...

class Event(GetAttrData):
    def __init__(
        self, binarydata: SliceableBuffer | None = None, display: display.Display | None = None, **keys: object
    ) -> None: ...

def call_error_handler(
    handler: Callable[[XError, Request | None], _T], error: XError, request: Request | None
) -> _T | Literal[0]: ...
