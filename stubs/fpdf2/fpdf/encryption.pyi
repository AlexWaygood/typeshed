"""
Utilities to perform encryption following the PDF standards.

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

from _typeshed import Incomplete, SupportsLenAndGetItem
from collections.abc import Generator, Iterable
from logging import Logger
from typing import ClassVar, Protocol, TypeVar, overload
from typing_extensions import TypeAlias

from .enums import AccessPermission, EncryptionMethod
from .fpdf import FPDF
from .syntax import Name, PDFObject

_Key: TypeAlias = SupportsLenAndGetItem[int]
_T_co = TypeVar("_T_co", covariant=True)

LOGGER: Logger

import_error: ImportError | None

class _SupportsGetItem(Protocol[_T_co]):
    def __getitem__(self, k: int, /) -> _T_co: ...

class ARC4:
    """
    This is a simplified version of the ARC4 (alleged RC4) algorithm,
    created based on the following sources:
    * Wikipedia article on RC4
    * github.com/manojpandey/rc4 (MIT License)
    * http://people.csail.mit.edu/rivest/pubs/RS14.pdf

    Having this ARC4 implementation makes it possible to have basic
    encryption functions without additional dependencies
    """

    MOD: ClassVar[int]
    def KSA(self, key: _Key) -> list[int]: ...
    def PRGA(self, S: _SupportsGetItem[int]) -> Generator[int, None, None]: ...
    def encrypt(self, key: _Key, text: Iterable[int]) -> list[int]: ...

class CryptFilter:
    """Represents one crypt filter, listed under CF inside the encryption dictionary"""

    type: Name
    c_f_m: Name
    length: int
    def __init__(self, mode: str, length: int) -> None: ...
    def serialize(self) -> str: ...

class EncryptionDictionary(PDFObject):
    """
    This class represents an encryption dictionary
    PDF 32000 reference - Table 20
    The PDF trailer must reference this object (/Encrypt)
    """

    filter: Name
    length: int
    r: int
    o: str
    u: str
    v: int
    p: int
    encrypt_metadata: str  # not always defined
    c_f: str  # not always defined
    stm_f: Name
    str_f: Name
    def __init__(self, security_handler: StandardSecurityHandler) -> None: ...

class StandardSecurityHandler:
    """
    This class is referenced in the main PDF class and is used to handle all encryption functions
        * Calculate password and hashes
        * Provide encrypt method to be called by stream and strings
        * Set the access permissions on the document
    """

    DEFAULT_PADDING: ClassVar[bytes]
    fpdf: FPDF
    access_permission: int
    owner_password: str
    user_password: str
    encryption_method: EncryptionMethod | None
    cf: CryptFilter | None
    key_length: int
    version: int
    revision: int
    encrypt_metadata: bool

    # The following fields are only defined after a call to generate_passwords().
    file_id: Incomplete
    info_id: Incomplete
    o: str
    k: str
    u: str
    # The following field is only defined after a call to generate_user_password_rev6().
    ue: Incomplete
    # The following field is only defined after a call to generate_owner_password_rev6().
    oe: Incomplete
    # The following field is only defined after a call to generate_perms_rev6().
    perms_rev6: Incomplete

    def __init__(
        self,
        fpdf: FPDF,
        owner_password: str,
        user_password: str | None = None,
        permission: AccessPermission = ...,
        encryption_method: EncryptionMethod = ...,
        encrypt_metadata: bool = False,
    ) -> None: ...
    def generate_passwords(self, file_id: str) -> None:
        """File_id is the first hash of the PDF file id"""

    def get_encryption_obj(self) -> EncryptionDictionary:
        """Return an encryption dictionary"""

    @overload
    def encrypt(self, text: bytes | bytearray, obj_id: int) -> bytes:
        """Method invoked by PDFObject and PDFContentStream to encrypt strings and streams"""

    @overload
    def encrypt(self, text: str, obj_id: int) -> str: ...
    def encrypt_string(self, string: str, obj_id: int) -> str: ...
    def encrypt_stream(self, stream: bytes, obj_id: int) -> bytes: ...
    def is_aes_algorithm(self) -> bool: ...
    def encrypt_bytes(self, data: bytes, obj_id: int) -> list[int]:
        """
        PDF32000 reference - Algorithm 1: Encryption of data using the RC4 or AES algorithms
        Append object ID and generation ID to the key and encrypt the data
        Generation ID is fixed as 0. Will need to revisit if the application start changing generation ID
        """

    def encrypt_AES_cryptography(self, key: bytes, data: bytes) -> bytes:
        """Encrypts an array of bytes using AES algorithms (AES 128 or AES 256)"""

    @classmethod
    def get_random_bytes(cls, size: int) -> bytes:
        """
        https://docs.python.org/3/library/os.html#os.urandom
        os.urandom will use OS-specific sources to generate random bytes
        suitable for cryptographic use
        """

    @classmethod
    def prepare_string(cls, string: str) -> bytes:
        """
        PDF2.0 - ISO 32000-2:2020
        All passwords for revision 6 shall be based on Unicode. Preprocessing of a user-provided password
        consists first of normalizing its representation by applying the "SASLPrep" profile (Internet RFC 4013)
        of the "stringprep" algorithm (Internet RFC 3454) to the supplied password using the Normalize and BiDi
        options. Next, the password string shall be converted to UTF-8 encoding, and then truncated to the
        first 127 bytes if the string is longer than 127 bytes

        Python offers a stringprep module with the tables mapped in methods
        """

    def padded_password(self, password: str) -> bytearray:
        """
        PDF32000 reference - Algorithm 2: Computing an encryption key
        Step (a) - Add the default padding at the end of provided password to make it 32 bit long
        """

    def generate_owner_password(self) -> str:
        """
        PDF32000 reference - Algorithm 3: Computing the encryption dictionary's O (owner password) value
        The security handler is only using revision 3 or 4, so the legacy r2 version is not implemented here
        """

    def generate_user_password(self) -> str:
        """
        PDF32000 reference - Algorithm 5: Computing the encryption dictionary's U (user password) value
        The security handler is only using revision 3 or 4, so the legacy r2 version is not implemented here
        """

    @classmethod
    def compute_hash(cls, input_password: bytes, salt: bytes, user_key: bytes = ...) -> bytes:
        """
        Algorithm 2B - section 7.6.4.3.4 of the ISO 32000-2:2020
        Applied on Security handlers revision 6
        """

    def generate_user_password_rev6(self) -> None:
        """
        Generating the U (user password) and UE (user encryption)
        for security handlers of revision 6
        Algorithm 8 - Section 7.6.4.4.7 of the ISO 32000-2:2020
        """

    def generate_owner_password_rev6(self) -> None:
        """
        Generating the O (owner password) and OE (owner encryption)
        for security handlers of revision 6
        Algorithm 9 - Section 7.6.4.4.8 of the ISO 32000-2:2020
        """

    def generate_perms_rev6(self) -> None:
        """
        7.6.4.4.9 Algorithm 10: Computing the encryption dictionary’s Perms (permissions) value
        (Security handlers of revision 6) of the ISO 32000-2:2020
        """

    def generate_encryption_key(self) -> bytes:
        """
        PDF32000 reference
        Algorithm 2: Computing an encryption key
        """

def md5(data: bytes | bytearray) -> bytes: ...
def int32(n: int) -> int:
    """convert long to signed 32 bit integer"""
