"""Provides a container for DescriptorProtos."""

from typing import Final

from google.protobuf.descriptor_pb2 import FileDescriptorProto

__author__: Final[str]

class Error(Exception): ...

class DescriptorDatabaseConflictingDefinitionError(Error):
    """Raised when a proto is added with the same name & different descriptor."""

class DescriptorDatabase:
    """A container accepting FileDescriptorProtos and maps DescriptorProtos."""

    def __init__(self) -> None: ...
    def Add(self, file_desc_proto) -> None:
        """Adds the FileDescriptorProto and its types to this database.

        Args:
          file_desc_proto: The FileDescriptorProto to add.
        Raises:
          DescriptorDatabaseConflictingDefinitionError: if an attempt is made to
            add a proto with the same name but different definition than an
            existing proto in the database.
        """

    def FindFileByName(self, name):
        """Finds the file descriptor proto by file name.

        Typically the file name is a relative path ending to a .proto file. The
        proto with the given name will have to have been added to this database
        using the Add method or else an error will be raised.

        Args:
          name: The file name to find.

        Returns:
          The file descriptor proto matching the name.

        Raises:
          KeyError if no file by the given name was added.
        """

    def FindFileContainingSymbol(self, symbol):
        """Finds the file descriptor proto containing the specified symbol.

        The symbol should be a fully qualified name including the file descriptor's
        package and any containing messages. Some examples:

        'some.package.name.Message'
        'some.package.name.Message.NestedEnum'
        'some.package.name.Message.some_field'

        The file descriptor proto containing the specified symbol must be added to
        this database using the Add method or else an error will be raised.

        Args:
          symbol: The fully qualified symbol name.

        Returns:
          The file descriptor proto containing the symbol.

        Raises:
          KeyError if no file contains the specified symbol.
        """

    def FindFileContainingExtension(self, extendee_name, extension_number) -> FileDescriptorProto | None: ...
    def FindAllExtensionNumbers(self, extendee_name) -> list[int]: ...
