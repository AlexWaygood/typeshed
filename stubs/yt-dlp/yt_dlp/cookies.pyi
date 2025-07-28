from collections.abc import Collection, Iterator, KeysView
from enum import Enum
from http.cookiejar import Cookie, CookiePolicy, MozillaCookieJar
from http.cookies import SimpleCookie
from typing import TextIO, TypeVar

from . import _LoggerProtocol
from .minicurses import MultilinePrinter
from .utils._utils import YoutubeDLError
from .YoutubeDL import YoutubeDL

CHROMIUM_BASED_BROWSERS: set[str] = ...
SUPPORTED_BROWSERS: set[str] = ...

class _LinuxKeyring(Enum):
    """
    https://chromium.googlesource.com/chromium/src/+/refs/heads/main/components/os_crypt/sync/key_storage_util_linux.h
    SelectedLinuxBackend
    """

    BASICTEXT = 5
    GNOMEKEYRING = 4
    KWALLET = 1
    KWALLET5 = 2
    KWALLET6 = 3

SUPPORTED_KEYRINGS: KeysView[str]

class YDLLogger(_LoggerProtocol):
    def warning(self, message: str, only_once: bool = False) -> None: ...  # type: ignore[override]

    class ProgressBar(MultilinePrinter):
        def print(self, message: str) -> None: ...

    def progress_bar(self) -> ProgressBar:
        """Return a context manager with a print method. (Optional)"""

class CookieLoadError(YoutubeDLError): ...

class YoutubeDLCookieJar(MozillaCookieJar):
    """
    See [1] for cookie file format.

    1. https://curl.haxx.se/docs/http-cookies.html
    """

    def __init__(self, filename: str | None = ..., delayload: bool = False, policy: CookiePolicy | None = None) -> None: ...
    def open(self, file: str, *, write: bool = ...) -> Iterator[TextIO]: ...
    def get_cookie_header(self, url: str) -> str:
        """Generate a Cookie HTTP header for a given url"""

    def get_cookies_for_url(self, url: str) -> list[Cookie]:
        """Generate a list of Cookie objects for a given url"""

    def load(self, filename: str | None = None, ignore_discard: bool = True, ignore_expires: bool = True) -> None:
        """Load cookies from a file."""

    def save(self, filename: str | None = None, ignore_discard: bool = True, ignore_expires: bool = True) -> None:
        """
        Save cookies to a file.
        Code is taken from CPython 3.6
        https://github.com/python/cpython/blob/8d999cbf4adea053be6dbb612b9844635c4dfb8e/Lib/http/cookiejar.py#L2091-L2117
        """

def load_cookies(cookie_file: str, browser_specification: str | None, ydl: YoutubeDL) -> YoutubeDLCookieJar: ...
def extract_cookies_from_browser(
    browser_name: str,
    profile: str | None = ...,
    logger: _LoggerProtocol = ...,
    *,
    keyring: _LinuxKeyring | None = ...,
    container: str | None = ...,
) -> YoutubeDLCookieJar: ...

_T = TypeVar("_T", bound=MozillaCookieJar)

def parse_safari_cookies(data: bytes, jar: _T | None = None, logger: _LoggerProtocol = ...) -> _T:
    """
    References:
        - https://github.com/libyal/dtformats/blob/main/documentation/Safari%20Cookies.asciidoc
            - this data appears to be out of date but the important parts of the database structure is the same
            - there are a few bytes here and there which are skipped during parsing
    """

class ChromeCookieDecryptor:
    """
    Overview:

        Linux:
        - cookies are either v10 or v11
            - v10: AES-CBC encrypted with a fixed key
                - also attempts empty password if decryption fails
            - v11: AES-CBC encrypted with an OS protected key (keyring)
                - also attempts empty password if decryption fails
            - v11 keys can be stored in various places depending on the activate desktop environment [2]

        Mac:
        - cookies are either v10 or not v10
            - v10: AES-CBC encrypted with an OS protected key (keyring) and more key derivation iterations than linux
            - not v10: 'old data' stored as plaintext

        Windows:
        - cookies are either v10 or not v10
            - v10: AES-GCM encrypted with a key which is encrypted with DPAPI
            - not v10: encrypted with DPAPI

    Sources:
    - [1] https://chromium.googlesource.com/chromium/src/+/refs/heads/main/components/os_crypt/
    - [2] https://chromium.googlesource.com/chromium/src/+/refs/heads/main/components/os_crypt/sync/key_storage_linux.cc
        - KeyStorageLinux::CreateService
    """

    def decrypt(self, encrypted_value: bytes) -> str: ...

class LinuxChromeCookieDecryptor(ChromeCookieDecryptor):
    def __init__(
        self,
        browser_keyring_name: str,
        logger: _LoggerProtocol,
        *,
        keyring: _LinuxKeyring | None = ...,
        meta_version: int | None = ...,
    ) -> None: ...
    @staticmethod
    def derive_key(password: bytes) -> bytes: ...

class MacChromeCookieDecryptor(ChromeCookieDecryptor):
    def __init__(self, browser_keyring_name: str, logger: YDLLogger, meta_version: int | None = None) -> None: ...
    @staticmethod
    def derive_key(password: bytes) -> bytes: ...

class WindowsChromeCookieDecryptor(ChromeCookieDecryptor):
    def __init__(self, browser_root: str, logger: YDLLogger, meta_version: int | None = None) -> None: ...

def get_cookie_decryptor(
    browser_root: str,
    browser_keyring_name: str,
    logger: _LoggerProtocol,
    *,
    keyring: _LinuxKeyring | None = ...,
    meta_version: int | None = ...,
) -> ChromeCookieDecryptor: ...

class ParserError(Exception): ...

class DataParser:
    def __init__(self, data: bytes, logger: YDLLogger) -> None: ...
    def read_bytes(self, num_bytes: int) -> bytes: ...
    def expect_bytes(self, expected_value: bytes, message: str) -> None: ...
    def read_uint(self, big_endian: bool = False) -> int: ...
    def read_double(self, big_endian: bool = False) -> float: ...
    def read_cstring(self) -> bytes: ...
    def skip(self, num_bytes: int, description: str = "unknown") -> None: ...
    def skip_to(self, offset: int, description: str = "unknown") -> None: ...
    def skip_to_end(self, description: str = "unknown") -> None: ...

def pbkdf2_sha1(password: bytes, salt: bytes, iterations: int, key_length: int) -> bytes: ...

class LenientSimpleCookie(SimpleCookie):
    """More lenient version of http.cookies.SimpleCookie"""

    def load(self, data: str | Collection[str]) -> None: ...
