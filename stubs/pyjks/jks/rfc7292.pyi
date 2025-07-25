from hashlib import _Hash
from typing import Final, Literal
from typing_extensions import TypeAlias

from pyasn1.type.namedtype import NamedTypes
from pyasn1.type.univ import Sequence

PBE_WITH_SHA1_AND_TRIPLE_DES_CBC_OID: Final[tuple[int, ...]]
PURPOSE_KEY_MATERIAL: Final = 1
PURPOSE_IV_MATERIAL: Final = 2
PURPOSE_MAC_MATERIAL: Final = 3

_Purpose: TypeAlias = Literal[1, 2, 3]

class Pkcs12PBEParams(Sequence):
    """Virtually identical to PKCS#5's PBEParameter, but nevertheless has its own definition in its own RFC, so gets its own class."""

    componentType: NamedTypes

def derive_key(
    hashfn: _Hash, purpose_byte: _Purpose, password_str: str, salt: bytes, iteration_count: int, desired_key_size: int
) -> bytes:
    """
    Implements PKCS#12 key derivation as specified in RFC 7292, Appendix B, "Deriving Keys and IVs from Passwords and Salt".
    Ported from BC's implementation in org.bouncycastle.crypto.generators.PKCS12ParametersGenerator.

    hashfn:            hash function to use (expected to support the hashlib interface and attributes)
    password_str:      text string (not yet transformed into bytes)
    salt:              byte sequence
    purpose:           "purpose byte", signifies the purpose of the generated pseudorandom key material
    desired_key_size:  desired amount of bytes of key material to generate
    """

def decrypt_PBEWithSHAAnd3KeyTripleDESCBC(
    data: bytes | bytearray, password_str: str, salt: bytes, iteration_count: int
) -> bytes: ...
def decrypt_PBEWithSHAAndTwofishCBC(encrypted_data: bytes | bytearray, password: str, salt: bytes, iteration_count: int) -> bytes:
    """
    Decrypts PBEWithSHAAndTwofishCBC, assuming PKCS#12-generated PBE parameters.
    (Not explicitly defined as an algorithm in RFC 7292, but defined here nevertheless because of the assumption of PKCS#12 parameters).
    """

def encrypt_PBEWithSHAAndTwofishCBC(plaintext_data: bytes | bytearray, password: str, salt: bytes, iteration_count: int) -> bytes:
    """
    Encrypts a value with PBEWithSHAAndTwofishCBC, assuming PKCS#12-generated PBE parameters.
    (Not explicitly defined as an algorithm in RFC 7292, but defined here nevertheless because of the assumption of PKCS#12 parameters).
    """
