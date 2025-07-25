from _typeshed import SupportsKeysAndGetItem, Unused
from typing import Final, Literal
from typing_extensions import Self, TypeAlias

from .jks import TrustedCertEntry
from .util import AbstractKeystore, AbstractKeystoreEntry

_BksType: TypeAlias = Literal["bks", "uber"]
_CertType: TypeAlias = Literal["X.509"]
_EntryFormat: TypeAlias = Literal["PKCS8", "PKCS#8", "X.509", "X509", "RAW"]
_BksVersion: TypeAlias = Literal[1, 2]

ENTRY_TYPE_CERTIFICATE: Final = 1
ENTRY_TYPE_KEY: Final = 2
ENTRY_TYPE_SECRET: Final = 3
ENTRY_TYPE_SEALED: Final = 4

KEY_TYPE_PRIVATE: Final = 0
KEY_TYPE_PUBLIC: Final = 1
KEY_TYPE_SECRET: Final = 2
_KeyType: TypeAlias = Literal[0, 1, 2]

class AbstractBksEntry(AbstractKeystoreEntry):
    """Abstract superclass for BKS keystore entry types"""

    store_type: _BksType | None
    cert_chain: list[tuple[_CertType, bytes]]
    def __init__(
        self,
        *,
        cert_chain: list[tuple[_CertType, bytes]] = ...,
        encrypted: bytes | None = None,
        store_type: _BksType | None = None,
        alias: str,
        timestamp: int,
        **kwargs: Unused,
    ) -> None: ...

class BksTrustedCertEntry(TrustedCertEntry):
    """Represents a trusted certificate entry in a BKS or UBER keystore."""

    store_type: _BksType | None  # type: ignore[assignment]

class BksKeyEntry(AbstractBksEntry):
    """
    Represents a non-encrypted cryptographic key (public, private or secret) stored in a BKS keystore.
    May exceptionally appear as a top-level entry type in (very) old keystores, but you are most likely
    to encounter these as the nested object inside a :class:`BksSealedKeyEntry` once decrypted.
    """

    type: _KeyType
    format: _EntryFormat
    algorithm: str
    encoded: bytes
    # type == KEY_TYPE_PRIVATE
    pkey_pkcs8: bytes
    pkey: bytes
    algorithm_oid: tuple[int, ...]
    # type == KEY_TYPE_PUBLIC
    public_key_info: bytes
    public_key: bytes
    # type == KEY_TYPE_SECRET
    key: bytes
    key_size: int
    def __init__(
        self,
        type: _KeyType,
        format: _EntryFormat,
        algorithm: str,
        encoded: bytes,
        *,
        cert_chain: list[tuple[_CertType, bytes]] = ...,
        encrypted: bytes | None = None,
        store_type: _BksType | None = None,
        alias: str,
        timestamp: int,
        **kwargs: Unused,
    ) -> None: ...
    @classmethod
    def type2str(cls, t: _KeyType) -> Literal["PRIVATE", "PUBLIC", "SECRET"]:
        """
        Returns a string representation of the given key type. Returns one of ``PRIVATE``, ``PUBLIC`` or ``SECRET``, or ``None``
        if no such key type is known.

        :param int t: Key type constant. One of :const:`KEY_TYPE_PRIVATE`, :const:`KEY_TYPE_PUBLIC`, :const:`KEY_TYPE_SECRET`.
        """

    def is_decrypted(self) -> Literal[True]:
        """Always returns ``True`` for this entry type."""

class BksSecretKeyEntry(AbstractBksEntry):
    """
    Conceptually similar to, but not to be confused with, :class:`BksKeyEntry` objects of type :const:`KEY_TYPE_SECRET`:

      - :class:`BksSecretKeyEntry` objects store the result of arbitrary user-supplied byte[]s, which, per the Java Keystore SPI, keystores are
        obligated to assume have already been protected by the user in some unspecified way. Because of this assumption, no password is
        provided for these entries when adding them to the keystore, and keystores are thus forced to store these bytes as-is.

        Produced by a call to ``KeyStore.setKeyEntry(String alias, byte[] key, Certificate[] chain)`` call.

        The bouncycastle project appears to have completely abandoned these entry types well over a decade ago now, and it is no
        longer possible to retrieve these entries through the Java APIs in any (remotely) recent BC version.

      - :class:`BksKeyEntry` objects of type :const:`KEY_TYPE_SECRET` store the result of a getEncoded() call on proper Java objects of type SecretKey.

        Produced by a call to ``KeyStore.setKeyEntry(String alias, Key key, char[] password, Certificate[] chain)``.

        The difference here is that the KeyStore implementation knows it's getting a proper (Secret)Key Java object, and can decide
        for itself how to store it given the password supplied by the user. I.e., in this version of setKeyEntry it is left up to
        the keystore implementation to encode and protect the supplied Key object, instead of in advance by the user.
    """

    key: bytes
    def is_decrypted(self) -> Literal[True]:
        """Always returns ``True`` for this entry type."""

class BksSealedKeyEntry(AbstractBksEntry):
    """
    PBEWithSHAAnd3-KeyTripleDES-CBC-encrypted wrapper around a :class:`BksKeyEntry`. The contained key type is unknown until decrypted.

    Once decrypted, objects of this type can be used in the same way as :class:`BksKeyEntry`: attribute accesses are forwarded
    to the wrapped :class:`BksKeyEntry` object.
    """

    # Properties provided by __getattr__
    nested: BksKeyEntry | None
    # __getattr__ proxies all attributes of nested BksKeyEntry after decrypting
    type: _KeyType
    format: _EntryFormat
    algorithm: str
    encoded: bytes
    # if type == KEY_TYPE_PRIVATE
    pkey_pkcs8: bytes
    pkey: bytes
    algorithm_oid: tuple[int, ...]
    # if type == KEY_TYPE_PUBLIC
    public_key_info: bytes
    public_key: bytes
    # if type == KEY_TYPE_SECRET
    key: bytes
    key_size: int

class BksKeyStore(AbstractKeystore):
    """
    Bouncycastle "BKS" keystore parser. Supports both the current V2 and old V1 formats.
    """

    store_type: Literal["bks"]
    entries: dict[str, BksTrustedCertEntry | BksKeyEntry | BksSealedKeyEntry | BksSecretKeyEntry]  # type: ignore[assignment]
    version: _BksVersion
    def __init__(
        self,
        store_type: Literal["bks"],
        entries: SupportsKeysAndGetItem[str, BksTrustedCertEntry | BksKeyEntry | BksSealedKeyEntry | BksSecretKeyEntry],
        version: _BksVersion = 2,
    ) -> None: ...
    @property
    def certs(self) -> dict[str, BksTrustedCertEntry]:
        """A subset of the :attr:`entries` dictionary, filtered down to only
        those entries of type :class:`BksTrustedCertEntry`.
        """

    @property
    def plain_keys(self) -> dict[str, BksKeyEntry]:
        """A subset of the :attr:`entries` dictionary, filtered down to only
        those entries of type :class:`BksKeyEntry`.
        """

    @property
    def sealed_keys(self) -> dict[str, BksSealedKeyEntry]:
        """A subset of the :attr:`entries` dictionary, filtered down to only
        those entries of type :class:`BksSealedKeyEntry`.
        """

    @property
    def secret_keys(self) -> dict[str, BksSecretKeyEntry]:
        """A subset of the :attr:`entries` dictionary, filtered down to only
        those entries of type :class:`BksSecretKeyEntry`.
        """

    @classmethod
    def loads(cls, data: bytes, store_password: str, try_decrypt_keys: bool = True) -> Self:
        """
        See :meth:`jks.jks.KeyStore.loads`.

        :param bytes data: Byte string representation of the keystore to be loaded.
        :param str password: Keystore password string
        :param bool try_decrypt_keys: Whether to automatically try to decrypt any encountered key entries using the same password
                                      as the keystore password.

        :returns: A loaded :class:`BksKeyStore` instance, if the keystore could be successfully parsed and the supplied store password is correct.

                  If the ``try_decrypt_keys`` parameters was set to ``True``, any keys that could be successfully decrypted using the
                  store password have already been decrypted; otherwise, no atttempt to decrypt any key entries is made.

        :raises BadKeystoreFormatException: If the keystore is malformed in some way
        :raises UnsupportedKeystoreVersionException: If the keystore contains an unknown format version number
        :raises KeystoreSignatureException: If the keystore signature could not be verified using the supplied store password
        :raises DuplicateAliasException: If the keystore contains duplicate aliases
        """

class UberKeyStore(BksKeyStore):
    """
    BouncyCastle "UBER" keystore format parser.
    """

    store_type: Literal["uber"]  # type: ignore[assignment]
    version: Literal[1]
    def __init__(
        self,
        store_type: Literal["uber"],
        entries: SupportsKeysAndGetItem[str, BksTrustedCertEntry | BksKeyEntry | BksSealedKeyEntry | BksSecretKeyEntry],
        version: Literal[1] = 1,
    ) -> None: ...
