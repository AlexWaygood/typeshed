"""The credentials classes are used to encapsulate all authentication
information for the :class:`~pika.connection.ConnectionParameters` class.

The :class:`~pika.credentials.PlainCredentials` class returns the properly
formatted username and password to the :class:`~pika.connection.Connection`.

To authenticate with Pika, create a :class:`~pika.credentials.PlainCredentials`
object passing in the username and password and pass it as the credentials
argument value to the :class:`~pika.connection.ConnectionParameters` object.

If you are using :class:`~pika.connection.URLParameters` you do not need a
credentials object, one will automatically be created for you.

If you are looking to implement SSL certificate style authentication, you would
extend the :class:`~pika.credentials.ExternalCredentials` class implementing
the required behavior.

"""

from logging import Logger
from typing import ClassVar, Protocol

from .spec import Connection

class _Credentials(Protocol):
    TYPE: ClassVar[str]
    erase_on_connect: bool
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def response_for(self, start: Connection.Start) -> tuple[str | None, bytes | None]: ...
    def erase_credentials(self) -> None: ...

LOGGER: Logger

class PlainCredentials:
    """A credentials object for the default authentication methodology with
    RabbitMQ.

    If you do not pass in credentials to the ConnectionParameters object, it
    will create credentials for 'guest' with the password of 'guest'.

    If you pass True to erase_on_connect the credentials will not be stored
    in memory after the Connection attempt has been made.

    :param str username: The username to authenticate with
    :param str password: The password to authenticate with
    :param bool erase_on_connect: erase credentials on connect.

    """

    TYPE: ClassVar[str]
    erase_on_connect: bool
    username: str
    password: str
    def __init__(self, username: str, password: str, erase_on_connect: bool = False) -> None:
        """Create a new instance of PlainCredentials

        :param str username: The username to authenticate with
        :param str password: The password to authenticate with
        :param bool erase_on_connect: erase credentials on connect.

        """

    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def response_for(self, start: Connection.Start) -> tuple[str | None, bytes | None]:
        """Validate that this type of authentication is supported

        :param spec.Connection.Start start: Connection.Start method
        :rtype: tuple(str|None, str|None)

        """

    def erase_credentials(self) -> None:
        """Called by Connection when it no longer needs the credentials"""

class ExternalCredentials:
    """The ExternalCredentials class allows the connection to use EXTERNAL
    authentication, generally with a client SSL certificate.

    """

    TYPE: ClassVar[str]
    erase_on_connect: bool
    def __init__(self) -> None:
        """Create a new instance of ExternalCredentials"""

    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def response_for(self, start: Connection.Start) -> tuple[str | None, bytes | None]:
        """Validate that this type of authentication is supported

        :param spec.Connection.Start start: Connection.Start method
        :rtype: tuple(str or None, str or None)

        """

    def erase_credentials(self) -> None:
        """Called by Connection when it no longer needs the credentials"""

VALID_TYPES: list[_Credentials]
