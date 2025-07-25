from _typeshed import FileDescriptorOrPath, SupportsKeysAndGetItem, Unused
from collections.abc import Iterable
from struct import Struct
from typing import Final, Literal
from typing_extensions import Self, TypeAlias

from .bks import BksKeyEntry
from .jks import PrivateKeyEntry

b8: Final[Struct]
b4: Final[Struct]
b2: Final[Struct]
b1: Final[Struct]
py23basestring: Final[tuple[type[str], type[str]]]
RSA_ENCRYPTION_OID: Final[tuple[int, ...]]
DSA_OID: Final[tuple[int, ...]]
DSA_WITH_SHA1_OID: Final[tuple[int, ...]]

_KeystoreType: TypeAlias = Literal["jks", "jceks", "bks", "uber"]
_PemType: TypeAlias = Literal["CERTIFICATE", "PUBLIC KEY", "PRIVATE KEY", "RSA PRIVATE KEY"]

class KeystoreException(Exception):
    """Superclass for all pyjks exceptions."""

class KeystoreSignatureException(KeystoreException):
    """Signifies that the supplied password for a keystore integrity check is incorrect."""

class DuplicateAliasException(KeystoreException):
    """Signifies that duplicate aliases were encountered in a keystore."""

class NotYetDecryptedException(KeystoreException):
    """
    Signifies that an attribute of a key store entry can not be accessed because the entry has not yet been decrypted.

    By default, the keystore ``load`` and ``loads`` methods automatically try to decrypt all key entries using the store password.
    Any keys for which that attempt fails are returned undecrypted, and will raise this exception when its attributes are accessed.

    To resolve, first call decrypt() with the correct password on the entry object whose attributes you want to access.
    """

class BadKeystoreFormatException(KeystoreException):
    """Signifies that a structural error was encountered during key store parsing."""

class BadDataLengthException(KeystoreException):
    """Signifies that given input data was of wrong or unexpected length."""

class BadPaddingException(KeystoreException):
    """Signifies that bad padding was encountered during decryption."""

class BadHashCheckException(KeystoreException):
    """Signifies that a hash computation did not match an expected value."""

class DecryptionFailureException(KeystoreException):
    """Signifies failure to decrypt a value."""

class UnsupportedKeystoreVersionException(KeystoreException):
    """Signifies an unexpected or unsupported keystore format version."""

class UnexpectedJavaTypeException(KeystoreException):
    """Signifies that a serialized Java object of unexpected type was encountered."""

class UnexpectedAlgorithmException(KeystoreException):
    """Signifies that an unexpected cryptographic algorithm was used in a keystore."""

class UnexpectedKeyEncodingException(KeystoreException):
    """Signifies that a key was stored in an unexpected format or encoding."""

class UnsupportedKeystoreTypeException(KeystoreException):
    """Signifies that the keystore was an unsupported type."""

class UnsupportedKeystoreEntryTypeException(KeystoreException):
    """Signifies that the keystore entry was an unsupported type."""

class UnsupportedKeyFormatException(KeystoreException):
    """Signifies that the key format was an unsupported type."""

class AbstractKeystore:
    """
    Abstract superclass for keystores.
    """

    store_type: _KeystoreType
    entries: dict[str, AbstractKeystoreEntry]
    def __init__(self, store_type: _KeystoreType, entries: SupportsKeysAndGetItem[str, AbstractKeystoreEntry]) -> None: ...
    @classmethod
    def load(cls, filename: FileDescriptorOrPath, store_password: str | None, try_decrypt_keys: bool = True) -> Self:
        """
        Convenience wrapper function; reads the contents of the given file
        and passes it through to :func:`loads`. See :func:`loads`.
        """

    def save(self, filename: FileDescriptorOrPath, store_password: str) -> None:
        """
        Convenience wrapper function; calls the :func:`saves`
        and saves the content to a file.
        """

class AbstractKeystoreEntry:
    """Abstract superclass for keystore entries."""

    store_type: _KeystoreType | None
    alias: str
    timestamp: int
    def __init__(self, *, store_type: _KeystoreType | None = None, alias: str, timestamp: int, **kwargs: Unused) -> None: ...
    @classmethod
    def new(cls, alias: str) -> Self:
        """
        Helper function to create a new KeyStoreEntry.
        """

    def is_decrypted(self) -> bool:
        """
        Returns ``True`` if the entry has already been decrypted, ``False`` otherwise.
        """

    def decrypt(self, key_password: str) -> None:
        """
        Decrypts the entry using the given password. Has no effect if the entry has already been decrypted.

        :param str key_password: The password to decrypt the entry with.
        :raises DecryptionFailureException: If the entry could not be decrypted using the given password.
        :raises UnexpectedAlgorithmException: If the entry was encrypted with an unknown or unexpected algorithm
        """

    def encrypt(self, key_password: str) -> None:
        """
        Encrypts the entry using the given password, so that it can be saved.

        :param str key_password: The password to encrypt the entry with.
        """

def as_hex(ba: bytes | bytearray) -> str: ...
def as_pem(der_bytes: bytes, type: _PemType) -> str: ...
def bitstring_to_bytes(bitstr: Iterable[int]) -> bytes:
    """
    Converts a pyasn1 univ.BitString instance to byte sequence of type 'bytes'.
    The bit string is interpreted big-endian and is left-padded with 0 bits to form a multiple of 8.
    """

def xor_bytearrays(a: bytes | bytearray, b: bytes | bytearray) -> bytearray: ...
def print_pem(der_bytes: bytes, type: _PemType) -> None: ...
def pkey_as_pem(pk: PrivateKeyEntry | BksKeyEntry) -> str: ...
def strip_pkcs5_padding(m: bytes | bytearray) -> bytes:
    """
    Drop PKCS5 padding:  8-(||M|| mod 8) octets each with value 8-(||M|| mod 8)
    Note: ideally we would use pycrypto for this, but it doesn't provide padding functionality and the project is virtually dead at this point.
    """

def strip_pkcs7_padding(m: bytes | bytearray, block_size: int) -> bytes:
    """
    Same as PKCS#5 padding, except generalized to block sizes other than 8.
    """

def add_pkcs7_padding(m: bytes | bytearray, block_size: int) -> bytes: ...
