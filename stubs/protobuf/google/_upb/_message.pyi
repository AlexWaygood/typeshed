"""Protobuf Module"""

from _typeshed import Incomplete
from typing import ClassVar, final

default_pool: DescriptorPool

@final
class Arena: ...

@final
class Descriptor:
    containing_type: Incomplete
    enum_types: Incomplete
    enum_types_by_name: Incomplete
    enum_values_by_name: Incomplete
    extension_ranges: Incomplete
    extensions: Incomplete
    extensions_by_name: Incomplete
    fields: Incomplete
    fields_by_camelcase_name: Incomplete
    fields_by_name: Incomplete
    fields_by_number: Incomplete
    file: Incomplete
    full_name: Incomplete
    has_options: Incomplete
    is_extendable: Incomplete
    name: Incomplete
    nested_types: Incomplete
    nested_types_by_name: Incomplete
    oneofs: Incomplete
    oneofs_by_name: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...  # incomplete
    def CopyToProto(self, object, /): ...
    def EnumValueName(self, *args, **kwargs): ...  # incomplete
    def GetOptions(self): ...

@final
class DescriptorPool:
    def __init__(self, *args, **kwargs) -> None: ...  # incomplete
    def Add(self, object, /):
        """Adds the FileDescriptorProto and its types to this pool."""

    def AddSerializedFile(self, object, /):
        """Adds a serialized FileDescriptorProto to this pool."""

    def FindAllExtensions(self, object, /):
        """Gets all known extensions of the given message descriptor."""

    def FindEnumTypeByName(self, object, /):
        """Searches for enum type descriptor by full name."""

    def FindExtensionByName(self, object, /):
        """Searches for extension descriptor by full name."""

    def FindExtensionByNumber(self, *args, **kwargs):  # incomplete
        """Gets the extension descriptor for the given number."""

    def FindFieldByName(self, object, /):
        """Searches for a field descriptor by full name."""

    def FindFileByName(self, object, /):
        """Searches for a file descriptor by its .proto name."""

    def FindFileContainingSymbol(self, object, /):
        """Gets the FileDescriptor containing the specified symbol."""

    def FindMessageTypeByName(self, object, /):
        """Searches for a message descriptor by full name."""

    def FindMethodByName(self, object, /):
        """Searches for method descriptor by full name."""

    def FindOneofByName(self, object, /):
        """Searches for oneof descriptor by full name."""

    def FindServiceByName(self, object, /):
        """Searches for service descriptor by full name."""

    def SetFeatureSetDefaults(self, object, /):
        """Sets the default feature mappings used during the build."""

@final
class EnumDescriptor:
    containing_type: Incomplete
    file: Incomplete
    full_name: Incomplete
    has_options: Incomplete
    is_closed: Incomplete
    name: Incomplete
    values: Incomplete
    values_by_name: Incomplete
    values_by_number: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...  # incomplete
    def CopyToProto(self, object, /): ...
    def GetOptions(self): ...

@final
class EnumValueDescriptor:
    has_options: Incomplete
    index: Incomplete
    name: Incomplete
    number: Incomplete
    type: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...  # incomplete
    def GetOptions(self): ...

@final
class ExtensionDict:
    def __contains__(self, other) -> bool:
        """Return bool(key in self)."""

    def __delitem__(self, other) -> None:
        """Delete self[key]."""

    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __getitem__(self, index):
        """Return self[key]."""

    def __gt__(self, other: object) -> bool: ...
    def __iter__(self):
        """Implement iter(self)."""

    def __le__(self, other: object) -> bool: ...
    def __len__(self) -> int:
        """Return len(self)."""

    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __setitem__(self, index, object) -> None:
        """Set self[key] to value."""

@final
class ExtensionIterator:
    def __iter__(self):
        """Implement iter(self)."""

    def __next__(self):
        """Implement next(self)."""

@final
class FieldDescriptor:
    CPPTYPE_BOOL: ClassVar[int] = ...
    CPPTYPE_BYTES: ClassVar[int] = ...
    CPPTYPE_DOUBLE: ClassVar[int] = ...
    CPPTYPE_ENUM: ClassVar[int] = ...
    CPPTYPE_FLOAT: ClassVar[int] = ...
    CPPTYPE_INT32: ClassVar[int] = ...
    CPPTYPE_INT64: ClassVar[int] = ...
    CPPTYPE_MESSAGE: ClassVar[int] = ...
    CPPTYPE_STRING: ClassVar[int] = ...
    CPPTYPE_UINT32: ClassVar[int] = ...
    CPPTYPE_UINT64: ClassVar[int] = ...
    LABEL_OPTIONAL: ClassVar[int] = ...
    LABEL_REPEATED: ClassVar[int] = ...
    LABEL_REQUIRED: ClassVar[int] = ...
    TYPE_BOOL: ClassVar[int] = ...
    TYPE_BYTES: ClassVar[int] = ...
    TYPE_DOUBLE: ClassVar[int] = ...
    TYPE_ENUM: ClassVar[int] = ...
    TYPE_FIXED32: ClassVar[int] = ...
    TYPE_FIXED64: ClassVar[int] = ...
    TYPE_FLOAT: ClassVar[int] = ...
    TYPE_GROUP: ClassVar[int] = ...
    TYPE_INT32: ClassVar[int] = ...
    TYPE_INT64: ClassVar[int] = ...
    TYPE_MESSAGE: ClassVar[int] = ...
    TYPE_SFIXED32: ClassVar[int] = ...
    TYPE_SFIXED64: ClassVar[int] = ...
    TYPE_SINT32: ClassVar[int] = ...
    TYPE_SINT64: ClassVar[int] = ...
    TYPE_STRING: ClassVar[int] = ...
    TYPE_UINT32: ClassVar[int] = ...
    TYPE_UINT64: ClassVar[int] = ...
    camelcase_name: Incomplete
    containing_oneof: Incomplete
    containing_type: Incomplete
    cpp_type: Incomplete
    default_value: Incomplete
    enum_type: Incomplete
    extension_scope: Incomplete
    file: Incomplete
    full_name: Incomplete
    has_default_value: Incomplete
    has_options: Incomplete
    has_presence: Incomplete
    index: Incomplete
    is_extension: Incomplete
    is_packed: Incomplete
    json_name: Incomplete
    label: Incomplete
    message_type: Incomplete
    name: Incomplete
    number: Incomplete
    type: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...  # incomplete
    def GetOptions(self): ...

@final
class FileDescriptor:
    dependencies: Incomplete
    enum_types_by_name: Incomplete
    extensions_by_name: Incomplete
    has_options: Incomplete
    message_types_by_name: Incomplete
    name: Incomplete
    package: Incomplete
    pool: Incomplete
    public_dependencies: Incomplete
    serialized_pb: Incomplete
    services_by_name: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...  # incomplete
    def CopyToProto(self, object, /): ...
    def GetOptions(self): ...

@final
class MapIterator:
    def __iter__(self):
        """Implement iter(self)."""

    def __next__(self):
        """Implement next(self)."""

@final
class Message:
    """A ProtocolMessage"""

    Extensions: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...  # incomplete  # incomplete
    def ByteSize(self):
        """Returns the size of the message in bytes."""

    def Clear(self):
        """Clears the message."""

    def ClearExtension(self, object, /):
        """Clears a message field."""

    def ClearField(self, object, /):
        """Clears a message field."""

    def CopyFrom(self, object, /):
        """Copies a protocol message into the current message."""

    def DiscardUnknownFields(self):
        """Discards the unknown fields."""

    def FindInitializationErrors(self):
        """Finds unset required fields."""

    @classmethod
    def FromString(cls, object, /):
        """Creates new method instance from given serialized data."""

    def HasExtension(self, object, /):
        """Checks if a message field is set."""

    def HasField(self, object, /):
        """Checks if a message field is set."""

    def IsInitialized(self, *args, **kwargs):  # incomplete
        """Checks if all required fields of a protocol message are set."""

    def ListFields(self):
        """Lists all set fields of a message."""

    def MergeFrom(self, object, /):
        """Merges a protocol message into the current message."""

    def MergeFromString(self, object, /):
        """Merges a serialized message into the current message."""

    def ParseFromString(self, object, /):
        """Parses a serialized message into the current message."""

    def SerializePartialToString(self, *args, **kwargs):  # incomplete
        """Serializes the message to a string, even if it isn't initialized."""

    def SerializeToString(self, *args, **kwargs):  # incomplete
        """Serializes the message to a string, only for initialized messages."""

    def SetInParent(self):
        """Sets the has bit of the given field in its parent message."""

    def UnknownFields(self):
        """Parse unknown field set"""

    def WhichOneof(self, object, /):
        """Returns the name of the field set inside a oneof, or None if no field is set."""

    def __contains__(self, other) -> bool:
        """Checks if a message field is set."""

    def __deepcopy__(self, memo=None):
        """Makes a deep copy of the class."""

    def __delattr__(self, name): ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __setattr__(self, name, value): ...

@final
class MessageMeta(type): ...

@final
class MethodDescriptor:
    client_streaming: Incomplete
    containing_service: Incomplete
    full_name: Incomplete
    index: Incomplete
    input_type: Incomplete
    name: Incomplete
    output_type: Incomplete
    server_streaming: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...  # incomplete
    def CopyToProto(self, object, /): ...
    def GetOptions(self): ...

@final
class OneofDescriptor:
    containing_type: Incomplete
    fields: Incomplete
    full_name: Incomplete
    has_options: Incomplete
    index: Incomplete
    name: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...  # incomplete
    def GetOptions(self): ...

@final
class RepeatedCompositeContainer:
    def __init__(self, *args, **kwargs) -> None: ...  # incomplete
    def MergeFrom(self, object, /):
        """Adds objects to the repeated container."""

    def add(self, *args, **kwargs):  # incomplete
        """Adds an object to the repeated container."""

    def append(self, object, /):
        """Appends a message to the end of the repeated container."""

    def extend(self, object, /):
        """Adds objects to the repeated container."""

    def insert(self, *args, **kwargs):  # incomplete
        """Inserts a message before the specified index."""

    def pop(self, *args, **kwargs):  # incomplete
        """Removes an object from the repeated container and returns it."""

    def remove(self, object, /):
        """Removes an object from the repeated container."""

    def reverse(self):
        """Reverses elements order of the repeated container."""

    def sort(self, *args, **kwargs):  # incomplete
        """Sorts the repeated container."""

    def __deepcopy__(self, memo=None):
        """Makes a deep copy of the class."""

    def __delitem__(self, other) -> None:
        """Delete self[key]."""

    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __getitem__(self, index):
        """Return self[key]."""

    def __gt__(self, other: object) -> bool: ...
    def __le__(self, other: object) -> bool: ...
    def __len__(self) -> int:
        """Return len(self)."""

    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __setitem__(self, index, object) -> None:
        """Set self[key] to value."""

@final
class RepeatedScalarContainer:
    def __init__(self, *args, **kwargs) -> None: ...  # incomplete
    def MergeFrom(self, object, /):
        """Merges a repeated container into the current container."""

    def append(self, object, /):
        """Appends an object to the repeated container."""

    def extend(self, object, /):
        """Appends objects to the repeated container."""

    def insert(self, *args, **kwargs):  # incomplete
        """Inserts an object at the specified position in the container."""

    def pop(self, *args, **kwargs):  # incomplete
        """Removes an object from the repeated container and returns it."""

    def remove(self, object, /):
        """Removes an object from the repeated container."""

    def reverse(self):
        """Reverses elements order of the repeated container."""

    def sort(self, *args, **kwargs):  # incomplete
        """Sorts the repeated container."""

    def __deepcopy__(self, memo=None):
        """Makes a deep copy of the class."""

    def __delitem__(self, other) -> None:
        """Delete self[key]."""

    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __getitem__(self, index):
        """Return self[key]."""

    def __gt__(self, other: object) -> bool: ...
    def __le__(self, other: object) -> bool: ...
    def __len__(self) -> int:
        """Return len(self)."""

    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __reduce__(self):
        """Outputs picklable representation of the repeated field."""

    def __setitem__(self, index, object) -> None:
        """Set self[key] to value."""

@final
class ServiceDescriptor:
    file: Incomplete
    full_name: Incomplete
    index: Incomplete
    methods: Incomplete
    methods_by_name: Incomplete
    name: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...  # incomplete
    def CopyToProto(self, object, /): ...
    def FindMethodByName(self, object, /): ...
    def GetOptions(self): ...

@final
class UnknownFieldSet:
    def __init__(self, *args, **kwargs) -> None: ...  # incomplete
    def __getitem__(self, index):
        """Return self[key]."""

    def __len__(self) -> int:
        """Return len(self)."""

def SetAllowOversizeProtos(object, /):  # incomplete
    """Enable/disable oversize proto parsing."""
