"""Reference implementation for reflection client in gRPC Python.

For usage instructions, see the Python Reflection documentation at
``doc/python/server_reflection.md``.
"""

import grpc
from google.protobuf.descriptor_database import DescriptorDatabase
from google.protobuf.descriptor_pb2 import FileDescriptorProto

class ProtoReflectionDescriptorDatabase(DescriptorDatabase):
    """
    A container and interface for receiving descriptors from a server's
    Reflection service.

    ProtoReflectionDescriptorDatabase takes a channel to a server with
    Reflection service, and provides an interface to retrieve the Reflection
    information. It implements the DescriptorDatabase interface.

    It is typically used to feed a DescriptorPool instance.
    """

    def __init__(self, channel: grpc.Channel) -> None: ...
    def get_services(self) -> list[str]:
        """
        Get list of full names of the registered services.

        Returns:
            A list of strings corresponding to the names of the services.
        """

    def FindFileByName(self, name: str) -> FileDescriptorProto:
        """
        Find a file descriptor by file name.

        This function implements a DescriptorDatabase interface, and is
        typically not called directly; prefer using a DescriptorPool instead.

        Args:
            name: The name of the file. Typically this is a relative path ending in ".proto".

        Returns:
            A FileDescriptorProto for the file.

        Raises:
            KeyError: the file was not found.
        """

    def FindFileContainingSymbol(self, symbol: str) -> FileDescriptorProto:
        """
        Find the file containing the symbol, and return its file descriptor.

        The symbol should be a fully qualified name including the file
        descriptor's package and any containing messages. Some examples:

            * "some.package.name.Message"
            * "some.package.name.Message.NestedEnum"
            * "some.package.name.Message.some_field"

        This function implements a DescriptorDatabase interface, and is
        typically not called directly; prefer using a DescriptorPool instead.

        Args:
            symbol: The fully-qualified name of the symbol.

        Returns:
            FileDescriptorProto for the file containing the symbol.

        Raises:
            KeyError: the symbol was not found.
        """

    def FindAllExtensionNumbers(self, extendee_name: str) -> list[int]:
        """
        Find the field numbers used by all known extensions of `extendee_name`.

        This function implements a DescriptorDatabase interface, and is
        typically not called directly; prefer using a DescriptorPool instead.

        Args:
            extendee_name: fully-qualified name of the extended message type.

        Returns:
            A list of field numbers used by all known extensions.

        Raises:
            KeyError: The message type `extendee_name` was not found.
        """

    def FindFileContainingExtension(self, extendee_name: str, extension_number: int) -> FileDescriptorProto:
        """
        Find the file which defines an extension for the given message type
        and field number.

        This function implements a DescriptorDatabase interface, and is
        typically not called directly; prefer using a DescriptorPool instead.

        Args:
            extendee_name: fully-qualified name of the extended message type.
            extension_number: the number of the extension field.

        Returns:
            FileDescriptorProto for the file containing the extension.

        Raises:
            KeyError: The message or the extension number were not found.
        """
