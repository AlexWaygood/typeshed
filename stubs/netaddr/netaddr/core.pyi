"""Common code shared between various netaddr sub modules"""

from _typeshed import SupportsWrite
from collections.abc import Iterator, Mapping
from typing import Final

BIG_ENDIAN_PLATFORM: bool
INET_PTON: Final = 1
ZEROFILL: Final = 2
NOHOST: Final = 4
INET_ATON: Final = 8

class AddrFormatError(Exception):
    """
    An Exception indicating a network address is not correctly formatted.
    """

class AddrConversionError(Exception):
    """
    An Exception indicating a failure to convert between address types or
    notations.
    """

class NotRegisteredError(Exception):
    """
    An Exception indicating that an OUI or IAB was not found in the IEEE
    Registry.
    """

class Subscriber:
    """
    An abstract class defining the interface expected by a Publisher.
    """

    def update(self, data) -> None:
        """
        A callback method used by a Publisher to notify this Subscriber about
        updates.

        :param data: a Python object containing data provided by Publisher.
        """

class PrettyPrinter(Subscriber):
    """
    A concrete Subscriber that employs the pprint in the standard library to
    format all data from updates received, writing them to a file-like
    object.

    Useful as a debugging aid.
    """

    fh: SupportsWrite[str]
    write_eol: bool
    def __init__(self, fh: SupportsWrite[str] = ..., write_eol: bool = True) -> None:
        """
        Constructor.

        :param fh: a file-like object to write updates to.
            Default: sys.stdout.


        :param write_eol: if ``True`` this object will write newlines to
            output, if ``False`` it will not.
        """

    def update(self, data: object) -> None:
        """
        A callback method used by a Publisher to notify this Subscriber about
        updates.

        :param data: a Python object containing data provided by Publisher.
        """

class Publisher:
    """
    A 'push' Publisher that maintains a list of Subscriber objects notifying
    them of state changes by passing them update data when it encounter events
    of interest.
    """

    subscribers: list[Subscriber]
    def __init__(self) -> None:
        """Constructor"""

    def attach(self, subscriber: Subscriber) -> None:
        """
        Add a new subscriber.

        :param subscriber: a new object that implements the Subscriber object
            interface.
        """

    def detach(self, subscriber: Subscriber) -> None:
        """
        Remove an existing subscriber.

        :param subscriber: a new object that implements the Subscriber object
            interface.
        """

    def notify(self, data: object) -> None:
        """
        Send update data to to all registered Subscribers.

        :param data: the data to be passed to each registered Subscriber.
        """

class DictDotLookup:
    """
    Creates objects that behave much like a dictionaries, but allow nested
    key access using object '.' (dot) lookups.

    Recipe 576586: Dot-style nested lookups over dictionary based data
    structures - http://code.activestate.com/recipes/576586/

    """

    def __init__(self, d: Mapping[str, object]) -> None: ...
    def __getitem__(self, name: str) -> object: ...
    def __iter__(self) -> Iterator[str]: ...
