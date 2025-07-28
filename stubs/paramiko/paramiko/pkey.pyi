"""
Common API for all public keys.
"""

from _typeshed import FileDescriptorOrPath
from pathlib import Path
from re import Pattern
from typing import IO, TypeVar
from typing_extensions import Self

from paramiko.message import Message

OPENSSH_AUTH_MAGIC: bytes

_BytesT = TypeVar("_BytesT", bound=bytes | bytearray)

def _unpad_openssh(data: _BytesT) -> _BytesT: ...

class UnknownKeyType(Exception):
    """
    An unknown public/private key algorithm was attempted to be read.
    """

    key_type: str | type | None
    key_bytes: bytes | None
    def __init__(self, key_type: str | type | None = None, key_bytes: bytes | None = None) -> None: ...

class PKey:
    """
    Base class for public keys.

    Also includes some "meta" level convenience constructors such as
    `.from_type_string`.
    """

    name: str
    HASHES: dict[str, type]
    public_blob: PublicBlob | None
    BEGIN_TAG: Pattern[str]
    END_TAG: Pattern[str]
    @staticmethod
    def from_path(path: Path | str, passphrase: bytes | None = None) -> PKey:
        """
        Attempt to instantiate appropriate key subclass from given file path.

        :param Path path: The path to load (may also be a `str`).

        :returns:
            A `PKey` subclass instance.

        :raises:
            `UnknownKeyType`, if our crypto backend doesn't know this key type.

        .. versionadded:: 3.2
        """

    @staticmethod
    def from_type_string(key_type: str, key_bytes: bytes) -> PKey:
        """
        Given type `str` & raw `bytes`, return a `PKey` subclass instance.

        For example, ``PKey.from_type_string("ssh-ed25519", <public bytes>)``
        will (if successful) return a new `.Ed25519Key`.

        :param str key_type:
            The key type, eg ``"ssh-ed25519"``.
        :param bytes key_bytes:
            The raw byte data forming the key material, as expected by
            subclasses' ``data`` parameter.

        :returns:
            A `PKey` subclass instance.

        :raises:
            `UnknownKeyType`, if no registered classes knew about this type.

        .. versionadded:: 3.2
        """

    @classmethod
    def identifiers(cls) -> list[str]:
        """
        returns an iterable of key format/name strings this class can handle.

        Most classes only have a single identifier, and thus this default
        implementation suffices; see `.ECDSAKey` for one example of an
        override.
        """

    def __init__(self, msg: Message | None = None, data: str | None = None) -> None:
        """
        Create a new instance of this public key type.  If ``msg`` is given,
        the key's public part(s) will be filled in from the message.  If
        ``data`` is given, the key's public part(s) will be filled in from
        the string.

        :param .Message msg:
            an optional SSH `.Message` containing a public key of this type.
        :param bytes data:
            optional, the bytes of a public key of this type

        :raises: `.SSHException` --
            if a key cannot be created from the ``data`` or ``msg`` given, or
            no key was passed in.
        """

    def asbytes(self) -> bytes:
        """
        Return a string of an SSH `.Message` made up of the public part(s) of
        this key.  This string is suitable for passing to `__init__` to
        re-create the key object later.
        """

    def __bytes__(self) -> bytes: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def get_name(self) -> str:
        """
        Return the name of this private key implementation.

        :return:
            name of this private key type, in SSH terminology, as a `str` (for
            example, ``"ssh-rsa"``).
        """

    @property
    def algorithm_name(self) -> str:
        """
        Return the key algorithm identifier for this key.

        Similar to `get_name`, but aimed at pure algorithm name instead of SSH
        protocol field value.
        """

    def get_bits(self) -> int:
        """
        Return the number of significant bits in this key.  This is useful
        for judging the relative security of a key.

        :return: bits in the key (as an `int`)
        """

    def can_sign(self) -> bool:
        """
        Return ``True`` if this key has the private part necessary for signing
        data.
        """

    def get_fingerprint(self) -> bytes:
        """
        Return an MD5 fingerprint of the public part of this key.  Nothing
        secret is revealed.

        :return:
            a 16-byte `string <str>` (binary) of the MD5 fingerprint, in SSH
            format.
        """

    @property
    def fingerprint(self) -> str:
        """
        Modern fingerprint property designed to be comparable to OpenSSH.

        Currently only does SHA256 (the OpenSSH default).

        .. versionadded:: 3.2
        """

    def get_base64(self) -> str:
        """
        Return a base64 string containing the public part of this key.  Nothing
        secret is revealed.  This format is compatible with that used to store
        public key files or recognized host keys.

        :return: a base64 `string <str>` containing the public part of the key.
        """

    def sign_ssh_data(self, data: bytes, algorithm: str | None = None) -> Message:
        """
        Sign a blob of data with this private key, and return a `.Message`
        representing an SSH signature message.

        :param bytes data:
            the data to sign.
        :param str algorithm:
            the signature algorithm to use, if different from the key's
            internal name. Default: ``None``.
        :return: an SSH signature `message <.Message>`.

        .. versionchanged:: 2.9
            Added the ``algorithm`` kwarg.
        """

    def verify_ssh_sig(self, data: bytes, msg: Message) -> bool:
        """
        Given a blob of data, and an SSH message representing a signature of
        that data, verify that it was signed with this key.

        :param bytes data: the data that was signed.
        :param .Message msg: an SSH signature message
        :return:
            ``True`` if the signature verifies correctly; ``False`` otherwise.
        """

    @classmethod
    def from_private_key_file(cls, filename: FileDescriptorOrPath, password: str | None = None) -> Self:
        """
        Create a key object by reading a private key file.  If the private
        key is encrypted and ``password`` is not ``None``, the given password
        will be used to decrypt the key (otherwise `.PasswordRequiredException`
        is thrown).  Through the magic of Python, this factory method will
        exist in all subclasses of PKey (such as `.RSAKey` or `.DSSKey`), but
        is useless on the abstract PKey class.

        :param str filename: name of the file to read
        :param str password:
            an optional password to use to decrypt the key file, if it's
            encrypted
        :return: a new `.PKey` based on the given private key

        :raises: ``IOError`` -- if there was an error reading the file
        :raises: `.PasswordRequiredException` -- if the private key file is
            encrypted, and ``password`` is ``None``
        :raises: `.SSHException` -- if the key file is invalid
        """

    @classmethod
    def from_private_key(cls, file_obj: IO[str], password: str | None = None) -> Self:
        """
        Create a key object by reading a private key from a file (or file-like)
        object.  If the private key is encrypted and ``password`` is not
        ``None``, the given password will be used to decrypt the key (otherwise
        `.PasswordRequiredException` is thrown).

        :param file_obj: the file-like object to read from
        :param str password:
            an optional password to use to decrypt the key, if it's encrypted
        :return: a new `.PKey` based on the given private key

        :raises: ``IOError`` -- if there was an error reading the key
        :raises: `.PasswordRequiredException` --
            if the private key file is encrypted, and ``password`` is ``None``
        :raises: `.SSHException` -- if the key file is invalid
        """

    def write_private_key_file(self, filename: FileDescriptorOrPath, password: str | None = None) -> None:
        """
        Write private key contents into a file.  If the password is not
        ``None``, the key is encrypted before writing.

        :param str filename: name of the file to write
        :param str password:
            an optional password to use to encrypt the key file

        :raises: ``IOError`` -- if there was an error writing the file
        :raises: `.SSHException` -- if the key is invalid
        """

    def write_private_key(self, file_obj: IO[str], password: str | None = None) -> None:
        """
        Write private key contents into a file (or file-like) object.  If the
        password is not ``None``, the key is encrypted before writing.

        :param file_obj: the file-like object to write into
        :param str password: an optional password to use to encrypt the key

        :raises: ``IOError`` -- if there was an error writing to the file
        :raises: `.SSHException` -- if the key is invalid
        """

    def load_certificate(self, value: Message | str) -> None:
        """
        Supplement the private key contents with data loaded from an OpenSSH
        public key (``.pub``) or certificate (``-cert.pub``) file, a string
        containing such a file, or a `.Message` object.

        The .pub contents adds no real value, since the private key
        file includes sufficient information to derive the public
        key info. For certificates, however, this can be used on
        the client side to offer authentication requests to the server
        based on certificate instead of raw public key.

        See:
        https://github.com/openssh/openssh-portable/blob/master/PROTOCOL.certkeys

        Note: very little effort is made to validate the certificate contents,
        that is for the server to decide if it is good enough to authenticate
        successfully.
        """

class PublicBlob:
    """
    OpenSSH plain public key or OpenSSH signed public key (certificate).

    Tries to be as dumb as possible and barely cares about specific
    per-key-type data.

    .. note::

        Most of the time you'll want to call `from_file`, `from_string` or
        `from_message` for useful instantiation, the main constructor is
        basically "I should be using ``attrs`` for this."
    """

    key_type: str
    key_blob: bytes
    comment: str
    def __init__(self, type_: str, blob: bytes, comment: str | None = None) -> None:
        """
        Create a new public blob of given type and contents.

        :param str type_: Type indicator, eg ``ssh-rsa``.
        :param bytes blob: The blob bytes themselves.
        :param str comment: A comment, if one was given (e.g. file-based.)
        """

    @classmethod
    def from_file(cls, filename: FileDescriptorOrPath) -> Self:
        """
        Create a public blob from a ``-cert.pub``-style file on disk.
        """

    @classmethod
    def from_string(cls, string: str) -> Self:
        """
        Create a public blob from a ``-cert.pub``-style string.
        """

    @classmethod
    def from_message(cls, message: Message) -> Self:
        """
        Create a public blob from a network `.Message`.

        Specifically, a cert-bearing pubkey auth packet, because by definition
        OpenSSH-style certificates 'are' their own network representation."
        """

    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
