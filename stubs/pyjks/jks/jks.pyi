"""JKS/JCEKS file format decoder. Use in conjunction with PyOpenSSL
to translate to PEM, or load private key and certs directly into
openssl structs and wrap sockets.

Notes on Python2/3 compatibility:

Whereever possible, we rely on the 'natural' byte string
representation of each Python version, i.e. 'str' in Python2 and
'bytes' in Python3.

Python2.6+ aliases the 'bytes' type to 'str', so we can universally
write bytes(...) or b"" to get each version's natural byte string
representation.

The libraries we interact with are written to expect these natural
types in their respective Py2/Py3 versions, so this works well.

Things get slightly more complicated when we need to manipulate
individual bytes from a byte string. str[x] returns a 'str' in Python2
and an 'int' in Python3. You can't do 'int' operations on a 'str' and
vice-versa, so we need some form of common data type.  We use
bytearray() for this purpose; in both Python2 and Python3, this will
return individual elements as an 'int'.

"""

from _typeshed import SupportsKeysAndGetItem, Unused
from collections.abc import Iterable
from typing import Final, Literal, NoReturn, overload
from typing_extensions import Self, TypeAlias

from .util import AbstractKeystore, AbstractKeystoreEntry

__version_info__: Final[tuple[int, int, int] | tuple[int, int, int, str]]
__version__: Final[str]
MAGIC_NUMBER_JKS: Final[bytes]
MAGIC_NUMBER_JCEKS: Final[bytes]
SIGNATURE_WHITENING: Final[bytes]

_JksType: TypeAlias = Literal["jks", "jceks"]
_CertType: TypeAlias = Literal["X.509"]
_KeyFormat: TypeAlias = Literal["pkcs8", "rsa_raw"]

class TrustedCertEntry(AbstractKeystoreEntry):
    """Represents a trusted certificate entry in a JKS or JCEKS keystore."""

    store_type: _JksType | None
    type: _CertType | None
    cert: bytes
    # NB! For most use cases, use TrustedCertEntry.new() classmethod.
    def __init__(
        self,
        *,
        type: _CertType | None = None,
        cert: bytes,
        store_type: _JksType | None = None,
        alias: str,
        timestamp: int,
        **kwargs: Unused,
    ) -> None: ...
    @classmethod
    def new(cls, alias: str, cert: bytes) -> Self:  # type: ignore[override]
        """
        Helper function to create a new TrustedCertEntry.

        :param str alias: The alias for the Trusted Cert Entry
        :param str certs: The certificate, as a byte string.

        :returns: A loaded :class:`TrustedCertEntry` instance, ready
          to be placed in a keystore.
        """

    def is_decrypted(self) -> Literal[True]:
        """Always returns ``True`` for this entry type."""

class PrivateKeyEntry(AbstractKeystoreEntry):
    """Represents a private key entry in a JKS or JCEKS keystore (e.g. an RSA or DSA private key)."""

    store_type: _JksType | None
    cert_chain: list[tuple[_CertType, bytes]]
    # Properties provided by __getattr__ after decryption
    @property
    def pkey(self) -> bytes: ...
    @property
    def pkey_pkcs8(self) -> bytes: ...
    @property
    def algorithm_oid(self) -> tuple[int, ...]: ...
    # NB! For most use cases, use PrivateKeyEntry.new() classmethod.
    # Overloaded: must provide `encrypted` OR `pkey`, `pkey_pkcs8`, `algorithm_oid`
    @overload
    def __init__(
        self,
        *,
        cert_chain: list[tuple[_CertType, bytes]],
        encrypted: bytes,
        store_type: _JksType | None = None,
        alias: str,
        timestamp: int,
        **kwargs: Unused,
    ) -> None: ...
    @overload
    def __init__(
        self,
        *,
        cert_chain: list[tuple[_CertType, bytes]],
        pkey: bytes,
        pkey_pkcs8: bytes,
        algorithm_oid: tuple[int, ...],
        store_type: _JksType | None = None,
        alias: str,
        timestamp: int,
        **kwargs: Unused,
    ) -> None: ...
    @classmethod
    def new(  # type: ignore[override]
        cls, alias: str, certs: Iterable[bytes], key: bytes, key_format: _KeyFormat = "pkcs8"
    ) -> Self:
        """
        Helper function to create a new PrivateKeyEntry.

        :param str alias: The alias for the Private Key Entry
        :param list certs: An list of certificates, as byte strings.
          The first one should be the one belonging to the private key,
          the others the chain (in correct order).
        :param str key: A byte string containing the private key in the
          format specified in the key_format parameter (default pkcs8).
        :param str key_format: The format of the provided private key.
          Valid options are pkcs8 or rsa_raw. Defaults to pkcs8.

        :returns: A loaded :class:`PrivateKeyEntry` instance, ready
          to be placed in a keystore.

        :raises UnsupportedKeyFormatException: If the key format is
          unsupported.
        """

class SecretKeyEntry(AbstractKeystoreEntry):
    """Represents a secret (symmetric) key entry in a JCEKS keystore (e.g. an AES or DES key)."""

    store_type: _JksType | None
    # Properties provided by __getattr__
    @property
    def algorithm(self) -> str: ...
    @property
    def key(self) -> bytes: ...
    @property
    def key_size(self) -> int: ...
    # Overloaded: must provide `sealed_obj` OR `algorithm`, `key`, `key_size`
    @overload
    def __init__(
        self, *, sealed_obj: bytes, store_type: _JksType | None = None, alias: str, timestamp: int, **kwargs: Unused
    ) -> None: ...
    @overload
    def __init__(
        self,
        *,
        algorithm: str,
        key: bytes,
        key_size: int,
        store_type: _JksType | None = None,
        alias: str,
        timestamp: int,
        **kwargs: Unused,
    ) -> None: ...
    # Not implemented by pyjks
    @classmethod
    def new(cls, alias: str, sealed_obj: bool, algorithm: str, key: bytes, key_size: int) -> NoReturn:  # type: ignore[override]
        """
        Helper function to create a new SecretKeyEntry.

        :returns: A loaded :class:`SecretKeyEntry` instance, ready
          to be placed in a keystore.
        """
    # Not implemented by pyjks
    def encrypt(self, key_password: str) -> NoReturn:
        """
        Encrypts the Secret Key so that the keystore can be saved
        """

class KeyStore(AbstractKeystore):
    """
    Represents a loaded JKS or JCEKS keystore.
    """

    entries: dict[str, TrustedCertEntry | PrivateKeyEntry | SecretKeyEntry]  # type: ignore[assignment]
    store_type: _JksType
    @classmethod
    def new(cls, store_type: _JksType, store_entries: Iterable[TrustedCertEntry | PrivateKeyEntry | SecretKeyEntry]) -> Self:
        """
        Helper function to create a new KeyStore.

        :param string store_type: What kind of keystore
          the store should be. Valid options are jks or jceks.
        :param list store_entries: Existing entries that
          should be added to the keystore.

        :returns: A loaded :class:`KeyStore` instance,
          with the specified entries.

        :raises DuplicateAliasException: If some of the
          entries have the same alias.
        :raises UnsupportedKeyStoreTypeException: If the keystore is of
          an unsupported type
        :raises UnsupportedKeyStoreEntryTypeException: If some
          of the keystore entries are unsupported (in this keystore type)
        """

    @classmethod
    def loads(cls, data: bytes, store_password: str | None, try_decrypt_keys: bool = True) -> Self:
        """Loads the given keystore file using the supplied password for
        verifying its integrity, and returns a :class:`KeyStore` instance.

        Note that entries in the store that represent some form of
        cryptographic key material are stored in encrypted form, and
        therefore require decryption before becoming accessible.

        Upon original creation of a key entry in a Java keystore,
        users are presented with the choice to either use the same
        password as the store password, or use a custom one. The most
        common choice is to use the store password for the individual
        key entries as well.

        For ease of use in this typical scenario, this function will
        attempt to decrypt each key entry it encounters with the store
        password:

         - If the key can be successfully decrypted with the store
           password, the entry is returned in its decrypted form, and
           its attributes are immediately accessible.
         - If the key cannot be decrypted with the store password, the
           entry is returned in its encrypted form, and requires a
           manual follow-up decrypt(key_password) call from the user
           before its individual attributes become accessible.

        Setting ``try_decrypt_keys`` to ``False`` disables this automatic
        decryption attempt, and returns all key entries in encrypted
        form.

        You can query whether a returned entry object has already been
        decrypted by calling the :meth:`is_decrypted` method on it.
        Attempting to access attributes of an entry that has not yet
        been decrypted will result in a
        :class:`~jks.util.NotYetDecryptedException`.

        :param bytes data: Byte string representation of the keystore
          to be loaded.
        :param str password: Keystore password string
        :param bool try_decrypt_keys: Whether to automatically try to
          decrypt any encountered key entries using the same password
          as the keystore password.

        :returns: A loaded :class:`KeyStore` instance, if the keystore
          could be successfully parsed and the supplied store password
          is correct.

          If the ``try_decrypt_keys`` parameter was set to ``True``, any
          keys that could be successfully decrypted using the store
          password have already been decrypted; otherwise, no atttempt
          to decrypt any key entries is made.

        :raises BadKeystoreFormatException: If the keystore is malformed
          in some way
        :raises UnsupportedKeystoreVersionException: If the keystore
          contains an unknown format version number
        :raises KeystoreSignatureException: If the keystore signature
          could not be verified using the supplied store password
        :raises DuplicateAliasException: If the keystore contains
          duplicate aliases
        """

    def saves(self, store_password: str) -> bytes:
        """
        Saves the keystore so that it can be read by other applications.

        If any of the private keys are unencrypted, they will be encrypted
        with the same password as the keystore.

        :param str store_password: Password for the created keystore
          (and for any unencrypted keys)

        :returns: A byte string representation of the keystore.

        :raises UnsupportedKeystoreTypeException: If the keystore
          is of an unsupported type
        :raises UnsupportedKeystoreEntryTypeException: If the keystore
          contains an unsupported entry type
        """
    # NB! For most use cases, use KeyStore.new() classmethod.
    def __init__(
        self, store_type: _JksType, entries: SupportsKeysAndGetItem[str, TrustedCertEntry | PrivateKeyEntry | SecretKeyEntry]
    ) -> None: ...
    @property
    def certs(self) -> dict[str, TrustedCertEntry]:
        """A subset of the :attr:`entries` dictionary, filtered down to only
        those entries of type :class:`TrustedCertEntry`.
        """

    @property
    def secret_keys(self) -> dict[str, SecretKeyEntry]:
        """A subset of the :attr:`entries` dictionary, filtered down to only
        those entries of type :class:`SecretKeyEntry`.
        """

    @property
    def private_keys(self) -> dict[str, PrivateKeyEntry]:
        """A subset of the :attr:`entries` dictionary, filtered down to only
        those entries of type :class:`PrivateKeyEntry`.
        """
