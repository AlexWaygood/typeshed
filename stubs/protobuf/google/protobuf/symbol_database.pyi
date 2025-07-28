"""A database of Python protocol buffer generated symbols.

SymbolDatabase is the MessageFactory for messages generated at compile time,
and makes it easy to create new instances of a registered type, given only the
type's protocol buffer symbol name.

Example usage::

  db = symbol_database.SymbolDatabase()

  # Register symbols of interest, from one or multiple files.
  db.RegisterFileDescriptor(my_proto_pb2.DESCRIPTOR)
  db.RegisterMessage(my_proto_pb2.MyMessage)
  db.RegisterEnumDescriptor(my_proto_pb2.MyEnum.DESCRIPTOR)

  # The database can be used as a MessageFactory, to generate types based on
  # their name:
  types = db.GetMessages(['my_proto.proto'])
  my_message_instance = types['MyMessage']()

  # The database's underlying descriptor pool can be queried, so it's not
  # necessary to know a type's filename to be able to generate it:
  filename = db.pool.FindFileContainingSymbol('MyMessage')
  my_message_instance = db.GetMessages([filename])['MyMessage']()

  # This functionality is also provided directly via a convenience method:
  my_message_instance = db.GetSymbol('MyMessage')()
"""

from collections.abc import Iterable

from google.protobuf.descriptor import Descriptor, EnumDescriptor, FileDescriptor, ServiceDescriptor
from google.protobuf.message import Message
from google.protobuf.message_factory import MessageFactory

class SymbolDatabase(MessageFactory):
    """A database of Python generated symbols."""

    def RegisterMessage(self, message: type[Message] | Message) -> type[Message] | Message:
        """Registers the given message type in the local database.

        Calls to GetSymbol() and GetMessages() will return messages registered here.

        Args:
          message: A :class:`google.protobuf.message.Message` subclass (or
            instance); its descriptor will be registered.

        Returns:
          The provided message.
        """

    def RegisterMessageDescriptor(self, message_descriptor: Descriptor) -> None:
        """Registers the given message descriptor in the local database.

        Args:
          message_descriptor (Descriptor): the message descriptor to add.
        """

    def RegisterEnumDescriptor(self, enum_descriptor: EnumDescriptor) -> EnumDescriptor:
        """Registers the given enum descriptor in the local database.

        Args:
          enum_descriptor (EnumDescriptor): The enum descriptor to register.

        Returns:
          EnumDescriptor: The provided descriptor.
        """

    def RegisterServiceDescriptor(self, service_descriptor: ServiceDescriptor) -> None:
        """Registers the given service descriptor in the local database.

        Args:
          service_descriptor (ServiceDescriptor): the service descriptor to
            register.
        """

    def RegisterFileDescriptor(self, file_descriptor: FileDescriptor) -> None:
        """Registers the given file descriptor in the local database.

        Args:
          file_descriptor (FileDescriptor): The file descriptor to register.
        """

    def GetSymbol(self, symbol: str) -> type[Message]:
        """Tries to find a symbol in the local database.

        Currently, this method only returns message.Message instances, however, if
        may be extended in future to support other symbol types.

        Args:
          symbol (str): a protocol buffer symbol.

        Returns:
          A Python class corresponding to the symbol.

        Raises:
          KeyError: if the symbol could not be found.
        """

    def GetMessages(self, files: Iterable[str]) -> dict[str, type[Message]]:
        """Gets all registered messages from a specified file.

        Only messages already created and registered will be returned; (this is the
        case for imported _pb2 modules)
        But unlike MessageFactory, this version also returns already defined nested
        messages, but does not register any message extensions.

        Args:
          files (list[str]): The file names to extract messages from.

        Returns:
          A dictionary mapping proto names to the message classes.

        Raises:
          KeyError: if a file could not be found.
        """

def Default() -> SymbolDatabase:
    """Returns the default SymbolDatabase."""
