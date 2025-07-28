"""Provides a factory class for generating dynamic messages.

The easiest way to use this class is if you have access to the FileDescriptor
protos containing the messages you want to create you can just do the following:

message_classes = message_factory.GetMessages(iterable_of_file_descriptors)
my_proto_instance = message_classes['some.proto.package.MessageName']()
"""

from collections.abc import Iterable
from typing import Any

from google.protobuf.descriptor import Descriptor
from google.protobuf.descriptor_pb2 import FileDescriptorProto
from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message import Message

class MessageFactory:
    """Factory for creating Proto2 messages from descriptors in a pool."""

    pool: Any
    def __init__(self, pool: DescriptorPool | None = None) -> None:
        """Initializes a new factory."""

def GetMessageClass(descriptor: Descriptor) -> type[Message]:
    """Obtains a proto2 message class based on the passed in descriptor.

    Passing a descriptor with a fully qualified name matching a previous
    invocation will cause the same class to be returned.

    Args:
      descriptor: The descriptor to build from.

    Returns:
      A class describing the passed in descriptor.
    """

def GetMessageClassesForFiles(files: Iterable[str], pool: DescriptorPool) -> dict[str, type[Message]]:
    """Gets all the messages from specified files.

    This will find and resolve dependencies, failing if the descriptor
    pool cannot satisfy them.

    Args:
      files: The file names to extract messages from.
      pool: The descriptor pool to find the files including the dependent files.

    Returns:
      A dictionary mapping proto names to the message classes.
    """

def GetMessages(file_protos: Iterable[FileDescriptorProto], pool: DescriptorPool | None = None) -> dict[str, type[Message]]:
    """Builds a dictionary of all the messages available in a set of files.

    Args:
      file_protos: Iterable of FileDescriptorProto to build messages out of.
      pool: The descriptor pool to add the file protos.

    Returns:
      A dictionary mapping proto names to the message classes. This will include
      any dependent messages as well as any messages defined in the same file as
      a specified message.
    """
