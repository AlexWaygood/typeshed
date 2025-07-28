"""passlib.totp -- TOTP / RFC6238 / Google Authenticator utilities."""

from collections.abc import Callable
from datetime import datetime
from typing import Any, Literal
from typing_extensions import Self

from passlib.exc import (
    InvalidTokenError as InvalidTokenError,
    MalformedTokenError as MalformedTokenError,
    TokenError as TokenError,
    UsedTokenError as UsedTokenError,
)
from passlib.utils import SequenceMixin

class AppWallet:
    """
    This class stores application-wide secrets that can be used
    to encrypt & decrypt TOTP keys for storage.
    It's mostly an internal detail, applications usually just need
    to pass ``secrets`` or ``secrets_path`` to :meth:`TOTP.using`.

    .. seealso::

        :ref:`totp-storing-instances` for more details on this workflow.

    Arguments
    =========
    :param secrets:
        Dict of application secrets to use when encrypting/decrypting
        stored TOTP keys.  This should include a secret to use when encrypting
        new keys, but may contain additional older secrets to decrypt
        existing stored keys.

        The dict should map tags -> secrets, so that each secret is identified
        by a unique tag.  This tag will be stored along with the encrypted
        key in order to determine which secret should be used for decryption.
        Tag should be string that starts with regex range ``[a-z0-9]``,
        and the remaining characters must be in ``[a-z0-9_.-]``.

        It is recommended to use something like a incremental counter
        ("1", "2", ...), an ISO date ("2016-01-01", "2016-05-16", ...),
        or a timestamp ("19803495", "19813495", ...) when assigning tags.

        This mapping be provided in three formats:

        * A python dict mapping tag -> secret
        * A JSON-formatted string containing the dict
        * A multiline string with the format ``"tag: value\\ntag: value\\n..."``

        (This last format is mainly useful when loading from a text file via **secrets_path**)

        .. seealso:: :func:`generate_secret` to create a secret with sufficient entropy

    :param secrets_path:
        Alternately, callers can specify a separate file where the
        application-wide secrets are stored, using either of the string
        formats described in **secrets**.

    :param default_tag:
        Specifies which tag in **secrets** should be used as the default
        for encrypting new keys. If omitted, the tags will be sorted,
        and the largest tag used as the default.

        if all tags are numeric, they will be sorted numerically;
        otherwise they will be sorted alphabetically.
        this permits tags to be assigned numerically,
        or e.g. using ``YYYY-MM-DD`` dates.

    :param encrypt_cost:
        Optional time-cost factor for key encryption.
        This value corresponds to log2() of the number of PBKDF2
        rounds used.

    .. warning::

        The application secret(s) should be stored in a secure location by
        your application, and each secret should contain a large amount
        of entropy (to prevent brute-force attacks if the encrypted keys
        are leaked).

        :func:`generate_secret` is provided as a convenience helper
        to generate a new application secret of suitable size.

        Best practice is to load these values from a file via **secrets_path**,
        and then have your application give up permission to read this file
        once it's running.

    Public Methods
    ==============
    .. autoattribute:: has_secrets
    .. autoattribute:: default_tag

    Semi-Private Methods
    ====================
    The following methods are used internally by the :class:`TOTP`
    class in order to encrypt & decrypt keys using the provided application
    secrets.  They will generally not be publically useful, and may have their
    API changed periodically.

    .. automethod:: get_secret
    .. automethod:: encrypt_key
    .. automethod:: decrypt_key
    """

    salt_size: int
    encrypt_cost: int
    default_tag: str | None
    def __init__(
        self,
        secrets: dict[int, str] | dict[int, bytes] | dict[str, str] | dict[str, bytes] | str | None = None,
        default_tag: str | None = None,
        encrypt_cost: int | None = None,
        secrets_path: str | None = None,
    ) -> None: ...
    @property
    def has_secrets(self) -> bool:
        """whether at least one application secret is present"""

    def get_secret(self, tag: str) -> bytes:
        """
        resolve a secret tag to the secret (as bytes).
        throws a KeyError if not found.
        """

    def encrypt_key(self, key: bytes) -> dict[str, Any]:
        """
        Helper used to encrypt TOTP keys for storage.

        :param key:
            TOTP key to encrypt, as raw bytes.

        :returns:
            dict containing encrypted TOTP key & configuration parameters.
            this format should be treated as opaque, and potentially subject
            to change, though it is designed to be easily serialized/deserialized
            (e.g. via JSON).

        .. note::

            This function requires installation of the external
            `cryptography <https://cryptography.io>`_ package.

        To give some algorithm details:  This function uses AES-256-CTR to encrypt
        the provided data.  It takes the application secret and randomly generated salt,
        and uses PBKDF2-HMAC-SHA256 to combine them and generate the AES key & IV.
        """

    def decrypt_key(self, enckey: dict[str, Any]) -> tuple[bytes, bool]:
        """
        Helper used to decrypt TOTP keys from storage format.
        Consults configured secrets to decrypt key.

        :param source:
            source object, as returned by :meth:`encrypt_key`.

        :returns:
            ``(key, needs_recrypt)`` --

            **key** will be the decrypted key, as bytes.

            **needs_recrypt** will be a boolean flag indicating
            whether encryption cost or default tag is too old,
            and henace that key needs re-encrypting before storing.

        .. note::

            This function requires installation of the external
            `cryptography <https://cryptography.io>`_ package.
        """

class TOTP:
    """
    Helper for generating and verifying TOTP codes.

    Given a secret key and set of configuration options, this object
    offers methods for token generation, token validation, and serialization.
    It can also be used to track important persistent TOTP state,
    such as the last counter used.

    This class accepts the following options
    (only **key** and **format** may be specified as positional arguments).

    :arg str key:
        The secret key to use. By default, should be encoded as
        a base32 string (see **format** for other encodings).

        Exactly one of **key** or ``new=True`` must be specified.

    :arg str format:
        The encoding used by the **key** parameter. May be one of:
        ``"base32"`` (base32-encoded string),
        ``"hex"`` (hexadecimal string), or ``"raw"`` (raw bytes).
        Defaults to ``"base32"``.

    :param bool new:
        If ``True``, a new key will be generated using :class:`random.SystemRandom`.

        Exactly one ``new=True`` or **key** must be specified.

    :param str label:
        Label to associate with this token when generating a URI.
        Displayed to user by most OTP client applications (e.g. Google Authenticator),
        and typically has format such as ``"John Smith"`` or ``"jsmith@webservice.example.org"``.
        Defaults to ``None``.
        See :meth:`to_uri` for details.

    :param str issuer:
        String identifying the token issuer (e.g. the domain name of your service).
        Used internally by some OTP client applications (e.g. Google Authenticator) to distinguish entries
        which otherwise have the same label.
        Optional but strongly recommended if you're rendering to a URI.
        Defaults to ``None``.
        See :meth:`to_uri` for details.

    :param int size:
        Number of bytes when generating new keys. Defaults to size of hash algorithm (e.g. 20 for SHA1).

        .. warning::

            Overriding the default values for ``digits``, ``period``, or ``alg`` may
            cause problems with some OTP client programs (such as Google Authenticator),
            which may have these defaults hardcoded.

    :param int digits:
        The number of digits in the generated / accepted tokens. Defaults to ``6``.
        Must be in range [6 .. 10].

        .. rst-class:: inline-title
        .. caution::
           Due to a limitation of the HOTP algorithm, the 10th digit can only take on values 0 .. 2,
           and thus offers very little extra security.

    :param str alg:
        Name of hash algorithm to use. Defaults to ``"sha1"``.
        ``"sha256"`` and ``"sha512"`` are also accepted, per :rfc:`6238`.

    :param int period:
        The time-step period to use, in integer seconds. Defaults to ``30``.

    ..
        See the passlib documentation for a full list of attributes & methods.
    """

    min_json_version: int
    json_version: int
    wallet: AppWallet | None
    now: Callable[[], float]
    digits: int
    alg: str
    label: str | None
    issuer: str | None
    period: int
    changed: bool
    @classmethod
    def using(
        cls,
        digits: int | None = None,
        alg: Literal["sha1", "sha256", "sha512"] | None = None,
        period: int | None = None,
        issuer: str | None = None,
        wallet: AppWallet | None = None,
        now: Callable[[], float] | None = None,
        *,
        secrets: dict[int, str] | dict[int, bytes] | dict[str, str] | dict[str, bytes] | str | None = None,
        **kwds: Any,
    ) -> type[TOTP]:
        """
        Dynamically create subtype of :class:`!TOTP` class
        which has the specified defaults set.

        :parameters: **digits, alg, period, issuer**:

            All these options are the same as in the :class:`TOTP` constructor,
            and the resulting class will use any values you specify here
            as the default for all TOTP instances it creates.

        :param wallet:
            Optional :class:`AppWallet` that will be used for encrypting/decrypting keys.

        :param secrets, secrets_path, encrypt_cost:

            If specified, these options will be passed to the :class:`AppWallet` constructor,
            allowing you to directly specify the secret keys that should be used
            to encrypt & decrypt stored keys.

        :returns:
            subclass of :class:`!TOTP`.

        This method is useful for creating a TOTP class configured
        to use your application's secrets for encrypting & decrypting
        keys, as well as create new keys using it's desired configuration defaults.

        As an example::

            >>> # your application can create a custom class when it initializes
            >>> from passlib.totp import TOTP, generate_secret
            >>> TotpFactory = TOTP.using(secrets={"1": generate_secret()})

            >>> # subsequent TOTP objects created from this factory
            >>> # will use the specified secrets to encrypt their keys...
            >>> totp = TotpFactory.new()
            >>> totp.to_dict()
            {'enckey': {'c': 14,
              'k': 'H77SYXWORDPGVOQTFRR2HFUB3C45XXI7',
              's': 'G5DOQPIHIBUM2OOHHADQ',
              't': '1',
              'v': 1},
             'type': 'totp',
             'v': 1}

        .. seealso:: :ref:`totp-creation` and :ref:`totp-storing-instances` tutorials for a usage example
        """

    @classmethod
    def new(cls, **kwds: Any) -> Self:
        """
        convenience alias for creating new TOTP key, same as ``TOTP(new=True)``
        """

    def __init__(
        self,
        key: str | bytes | None = None,
        format: str = "base32",
        new: bool = False,
        digits: int | None = None,
        alg: Literal["sha1", "sha256", "sha512"] | None = None,
        size: int | None = None,
        period: int | None = None,
        label: str | None = None,
        issuer: str | None = None,
        changed: bool = False,
        **kwds: Any,
    ) -> None: ...
    @property
    def key(self) -> bytes:
        """
        secret key as raw bytes
        """

    @key.setter
    def key(self, value: bytes) -> None: ...
    @property
    def encrypted_key(self) -> dict[str, Any]:
        """
        secret key, encrypted using application secret.
        this match the output of :meth:`AppWallet.encrypt_key`,
        and should be treated as an opaque json serializable object.
        """

    @encrypted_key.setter
    def encrypted_key(self, value: dict[str, Any]) -> None: ...
    @property
    def hex_key(self) -> str:
        """
        secret key encoded as hexadecimal string
        """

    @property
    def base32_key(self) -> str:
        """
        secret key encoded as base32 string
        """

    def pretty_key(self, format: str = "base32", sep: str | Literal[False] = "-") -> str:
        """
        pretty-print the secret key.

        This is mainly useful for situations where the user cannot get the qrcode to work,
        and must enter the key manually into their TOTP client. It tries to format
        the key in a manner that is easier for humans to read.

        :param format:
            format to output secret key. ``"hex"`` and ``"base32"`` are both accepted.

        :param sep:
            separator to insert to break up key visually.
            can be any of ``"-"`` (the default), ``" "``, or ``False`` (no separator).

        :return:
            key as native string.

        Usage example::

            >>> t = TOTP('s3jdvb7qd2r7jpxx')
            >>> t.pretty_key()
            'S3JD-VB7Q-D2R7-JPXX'
        """

    @classmethod
    def normalize_time(cls, time: float | datetime | None) -> int:
        """
        Normalize time value to unix epoch seconds.

        :arg time:
            Can be ``None``, :class:`!datetime`,
            or unix epoch timestamp as :class:`!float` or :class:`!int`.
            If ``None``, uses current system time.
            Naive datetimes are treated as UTC.

        :returns:
            unix epoch timestamp as :class:`int`.
        """

    def normalize_token(self_or_cls, token: bytes | str | int) -> str:
        """
        Normalize OTP token representation:
        strips whitespace, converts integers to a zero-padded string,
        validates token content & number of digits.

        This is a hybrid method -- it can be called at the class level,
        as ``TOTP.normalize_token()``, or the instance level as ``TOTP().normalize_token()``.
        It will normalize to the instance-specific number of :attr:`~TOTP.digits`,
        or use the class default.

        :arg token:
            token as ascii bytes, unicode, or an integer.

        :raises ValueError:
            if token has wrong number of digits, or contains non-numeric characters.

        :returns:
            token as :class:`!unicode` string, containing only digits 0-9.
        """

    def generate(self, time: float | datetime | None = None) -> TotpToken:
        """
        Generate token for specified time
        (uses current time if none specified).

        :arg time:
            Can be ``None``, a :class:`!datetime`,
            or class:`!float` / :class:`!int` unix epoch timestamp.
            If ``None`` (the default), uses current system time.
            Naive datetimes are treated as UTC.

        :returns:

            A :class:`TotpToken` instance, which can be treated
            as a sequence of ``(token, expire_time)`` -- see that class
            for more details.

        Usage example::

            >>> # generate a new token, wrapped in a TotpToken instance...
            >>> otp = TOTP('s3jdvb7qd2r7jpxx')
            >>> otp.generate(1419622739)
            <TotpToken token='897212' expire_time=1419622740>

            >>> # when you just need the token...
            >>> otp.generate(1419622739).token
            '897212'
        """

    @classmethod
    def verify(
        cls,
        token: int | str,
        source: TOTP | dict[str, Any] | str | bytes,
        *,
        time: float | datetime | None = ...,
        window: int = ...,
        skew: int = ...,
        last_counter: int | None = ...,
    ) -> TotpMatch:
        """
        Convenience wrapper around :meth:`TOTP.from_source` and :meth:`TOTP.match`.

        This parses a TOTP key & configuration from the specified source,
        and tries and match the token.
        It's designed to parallel the :meth:`passlib.ifc.PasswordHash.verify` method.

        :param token:
            Token string to match.

        :param source:
            Serialized TOTP key.
            Can be anything accepted by :meth:`TOTP.from_source`.

        :param \\\\*\\\\*kwds:
            All additional keywords passed to :meth:`TOTP.match`.

        :return:
            A :class:`TotpMatch` instance, or raises a :exc:`TokenError`.
        """

    def match(
        self,
        token: int | str,
        time: float | datetime | None = None,
        window: int = 30,
        skew: int = 0,
        last_counter: int | None = None,
    ) -> TotpMatch:
        """
        Match TOTP token against specified timestamp.
        Searches within a window before & after the provided time,
        in order to account for transmission delay and small amounts of skew in the client's clock.

        :arg token:
            Token to validate.
            may be integer or string (whitespace and hyphens are ignored).

        :param time:
            Unix epoch timestamp, can be any of :class:`!float`, :class:`!int`, or :class:`!datetime`.
            if ``None`` (the default), uses current system time.
            *this should correspond to the time the token was received from the client*.

        :param int window:
            How far backward and forward in time to search for a match.
            Measured in seconds. Defaults to ``30``.  Typically only useful if set
            to multiples of :attr:`period`.

        :param int skew:
            Adjust timestamp by specified value, to account for excessive
            client clock skew. Measured in seconds. Defaults to ``0``.

            Negative skew (the common case) indicates transmission delay,
            and/or that the client clock is running behind the server.

            Positive skew indicates the client clock is running ahead of the server
            (and by enough that it cancels out any negative skew added by
            the transmission delay).

            You should ensure the server clock uses a reliable time source such as NTP,
            so that only the client clock's inaccuracy needs to be accounted for.

            This is an advanced parameter that should usually be left at ``0``;
            The **window** parameter is usually enough to account
            for any observed transmission delay.

        :param last_counter:
            Optional value of last counter value that was successfully used.
            If specified, verify will never search earlier counters,
            no matter how large the window is.

            Useful when client has previously authenticated,
            and thus should never provide a token older than previously
            verified value.

        :raises ~passlib.exc.TokenError:

            If the token is malformed, fails to match, or has already been used.

        :returns TotpMatch:

            Returns a :class:`TotpMatch` instance on successful match.
            Can be treated as tuple of ``(counter, time)``.
            Raises error if token is malformed / can't be verified.

        Usage example::

            >>> totp = TOTP('s3jdvb7qd2r7jpxx')

            >>> # valid token for this time period
            >>> totp.match('897212', 1419622729)
            <TotpMatch counter=47320757 time=1419622729 cache_seconds=60>

            >>> # token from counter step 30 sec ago (within allowed window)
            >>> totp.match('000492', 1419622729)
            <TotpMatch counter=47320756 time=1419622729 cache_seconds=60>

            >>> # invalid token -- token from 60 sec ago (outside of window)
            >>> totp.match('760389', 1419622729)
            Traceback:
                ...
            InvalidTokenError: Token did not match
        """

    @classmethod
    def from_source(cls, source: TOTP | dict[str, Any] | str | bytes) -> Self:
        """
        Load / create a TOTP object from a serialized source.
        This acts as a wrapper for the various deserialization methods:

        * TOTP URIs are handed off to :meth:`from_uri`
        * Any other strings are handed off to :meth:`from_json`
        * Dicts are handed off to :meth:`from_dict`

        :param source:
            Serialized TOTP object.

        :raises ValueError:
            If the key has been encrypted, but the application secret isn't available;
            or if the string cannot be recognized, parsed, or decoded.

            See :meth:`TOTP.using()` for how to configure application secrets.

        :returns:
            a :class:`TOTP` instance.
        """

    @classmethod
    def from_uri(cls, uri: str) -> Self:
        """
        create an OTP instance from a URI (such as returned by :meth:`to_uri`).

        :returns:
            :class:`TOTP` instance.

        :raises ValueError:
            if the uri cannot be parsed or contains errors.

        .. seealso:: :ref:`totp-configuring-clients` tutorial for a usage example
        """

    def to_uri(self, label: str | None = None, issuer: str | None = None) -> str:
        """
        Serialize key and configuration into a URI, per
        Google Auth's `KeyUriFormat <http://code.google.com/p/google-authenticator/wiki/KeyUriFormat>`_.

        :param str label:
            Label to associate with this token when generating a URI.
            Displayed to user by most OTP client applications (e.g. Google Authenticator),
            and typically has format such as ``"John Smith"`` or ``"jsmith@webservice.example.org"``.

            Defaults to **label** constructor argument. Must be provided in one or the other location.
            May not contain ``:``.

        :param str issuer:
            String identifying the token issuer (e.g. the domain or canonical name of your service).
            Optional but strongly recommended if you're rendering to a URI.
            Used internally by some OTP client applications (e.g. Google Authenticator) to distinguish entries
            which otherwise have the same label.

            Defaults to **issuer** constructor argument, or ``None``.
            May not contain ``:``.

        :raises ValueError:
            * if a label was not provided either as an argument, or in the constructor.
            * if the label or issuer contains invalid characters.

        :returns:
            all the configuration information for this OTP token generator,
            encoded into a URI.

        These URIs are frequently converted to a QRCode for transferring
        to a TOTP client application such as Google Auth.
        Usage example::

            >>> from passlib.totp import TOTP
            >>> tp = TOTP('s3jdvb7qd2r7jpxx')
            >>> uri = tp.to_uri("user@example.org", "myservice.another-example.org")
            >>> uri
            'otpauth://totp/user@example.org?secret=S3JDVB7QD2R7JPXX&issuer=myservice.another-example.org'

        .. versionchanged:: 1.7.2

            This method now prepends the issuer URI label.  This is recommended by the KeyURI
            specification, for compatibility with older clients.
        """

    @classmethod
    def from_json(cls, source: str | bytes) -> Self:
        """
        Load / create an OTP object from a serialized json string
        (as generated by :meth:`to_json`).

        :arg json:
            Serialized output from :meth:`to_json`, as unicode or ascii bytes.

        :raises ValueError:
            If the key has been encrypted, but the application secret isn't available;
            or if the string cannot be recognized, parsed, or decoded.

            See :meth:`TOTP.using()` for how to configure application secrets.

        :returns:
            a :class:`TOTP` instance.

        .. seealso:: :ref:`totp-storing-instances` tutorial for a usage example
        """

    def to_json(self, encrypt: bool | None = None) -> str:
        """
        Serialize configuration & internal state to a json string,
        mainly useful for persisting client-specific state in a database.
        All keywords passed to :meth:`to_dict`.

        :returns:
            json string containing serializes configuration & state.
        """

    @classmethod
    def from_dict(cls, source: dict[str, Any]) -> Self:
        """
        Load / create a TOTP object from a dictionary
        (as generated by :meth:`to_dict`)

        :param source:
            dict containing serialized TOTP key & configuration.

        :raises ValueError:
            If the key has been encrypted, but the application secret isn't available;
            or if the dict cannot be recognized, parsed, or decoded.

            See :meth:`TOTP.using()` for how to configure application secrets.

        :returns:
            A :class:`TOTP` instance.

        .. seealso:: :ref:`totp-storing-instances` tutorial for a usage example
        """

    def to_dict(self, encrypt: bool | None = None) -> dict[str, Any]:
        """
        Serialize configuration & internal state to a dict,
        mainly useful for persisting client-specific state in a database.

        :param encrypt:
            Whether to output should be encrypted.

            * ``None`` (the default) -- uses encrypted key if application
              secrets are available, otherwise uses plaintext key.
            * ``True`` -- uses encrypted key, or raises TypeError
              if application secret wasn't provided to OTP constructor.
            * ``False`` -- uses raw key.

        :returns:
            dictionary, containing basic (json serializable) datatypes.
        """

class TotpToken(SequenceMixin):
    """
    Object returned by :meth:`TOTP.generate`.
    It can be treated as a sequence of ``(token, expire_time)``,
    or accessed via the following attributes:

    .. autoattribute:: token
    .. autoattribute:: expire_time
    .. autoattribute:: counter
    .. autoattribute:: remaining
    .. autoattribute:: valid
    """

    totp: TOTP | None
    token: str | None
    counter: int | None
    def __init__(self, totp: TOTP, token: str, counter: int) -> None:
        """
        .. warning::
            the constructor signature is an internal detail, and is subject to change.
        """

    @property
    def start_time(self) -> int:
        """Timestamp marking beginning of period when token is valid"""

    @property
    def expire_time(self) -> int:
        """Timestamp marking end of period when token is valid"""

    @property
    def remaining(self) -> float:
        """number of (float) seconds before token expires"""

    @property
    def valid(self) -> bool:
        """whether token is still valid"""

class TotpMatch(SequenceMixin):
    """
    Object returned by :meth:`TOTP.match` and :meth:`TOTP.verify` on a successful match.

    It can be treated as a sequence of ``(counter, time)``,
    or accessed via the following attributes:

    .. autoattribute:: counter
        :annotation: = 0

    .. autoattribute:: time
        :annotation: = 0

    .. autoattribute:: expected_counter
        :annotation: = 0

    .. autoattribute:: skipped
        :annotation: = 0

    .. autoattribute:: expire_time
        :annotation: = 0

    .. autoattribute:: cache_seconds
        :annotation: = 60

    .. autoattribute:: cache_time
        :annotation: = 0

    This object will always have a ``True`` boolean value.
    """

    totp: TOTP | None
    counter: int
    time: int
    window: int
    def __init__(self, totp: TOTP, counter: int, time: int, window: int = 30) -> None:
        """
        .. warning::
            the constructor signature is an internal detail, and is subject to change.
        """

    @property
    def expected_counter(self) -> int:
        """
        Counter value expected for timestamp.
        """

    @property
    def skipped(self) -> int:
        """
        How many steps were skipped between expected and actual matched counter
        value (may be positive, zero, or negative).
        """

    @property
    def expire_time(self) -> int:
        """Timestamp marking end of period when token is valid"""

    @property
    def cache_seconds(self) -> int:
        """
        Number of seconds counter should be cached
        before it's guaranteed to have passed outside of verification window.
        """

    @property
    def cache_time(self) -> int:
        """
        Timestamp marking when counter has passed outside of verification window.
        """

__all__ = [
    "AppWallet",
    "TOTP",
    "TokenError",
    "MalformedTokenError",
    "InvalidTokenError",
    "UsedTokenError",
    "TotpToken",
    "TotpMatch",
]
