from _typeshed import ReadableBuffer
from typing import Literal

__all__ = [
    "aes_cbc_decrypt",
    "aes_cbc_decrypt_bytes",
    "aes_cbc_encrypt",
    "aes_cbc_encrypt_bytes",
    "aes_ctr_decrypt",
    "aes_ctr_encrypt",
    "aes_decrypt",
    "aes_decrypt_text",
    "aes_ecb_decrypt",
    "aes_ecb_encrypt",
    "aes_encrypt",
    "aes_gcm_decrypt_and_verify",
    "aes_gcm_decrypt_and_verify_bytes",
    "key_expansion",
    "pad_block",
    "pkcs7_padding",
    "unpad_pkcs7",
]

def aes_cbc_decrypt_bytes(data: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypt bytes with AES-CBC using native implementation since pycryptodome is unavailable"""

def aes_gcm_decrypt_and_verify_bytes(data: bytes, key: bytes, tag: bytes, nonce: bytes) -> bytes:
    """Decrypt bytes with AES-GCM using native implementation since pycryptodome is unavailable"""

def aes_cbc_encrypt_bytes(
    data: bytes, key: bytes, iv: bytes, *, padding_mode: Literal["pkcs7", "iso7816", "whitespace", "zero"]
) -> bytes: ...
def unpad_pkcs7(data: list[int]) -> list[int]: ...
def pkcs7_padding(data: list[int]) -> list[int]:
    """
    PKCS#7 padding

    @param {int[]} data        cleartext
    @returns {int[]}           padding data
    """

def pad_block(block: list[int], padding_mode: Literal["pkcs7", "iso7816", "whitespace", "zero"]) -> list[int]:
    """
    Pad a block with the given padding mode
    @param {int[]} block        block to pad
    @param padding_mode         padding mode
    """

def aes_ecb_encrypt(data: list[int], key: list[int], iv: list[int] | None = None) -> list[int]:
    """
    Encrypt with aes in ECB mode. Using PKCS#7 padding

    @param {int[]} data        cleartext
    @param {int[]} key         16/24/32-Byte cipher key
    @param {int[]} iv          Unused for this mode
    @returns {int[]}           encrypted data
    """

def aes_ecb_decrypt(data: list[int], key: list[int], iv: list[int] | None = None) -> list[int]:
    """
    Decrypt with aes in ECB mode

    @param {int[]} data        cleartext
    @param {int[]} key         16/24/32-Byte cipher key
    @param {int[]} iv          Unused for this mode
    @returns {int[]}           decrypted data
    """

def aes_ctr_decrypt(data: list[int], key: list[int], iv: list[int]) -> list[int]:
    """
    Decrypt with aes in counter mode

    @param {int[]} data        cipher
    @param {int[]} key         16/24/32-Byte cipher key
    @param {int[]} iv          16-Byte initialization vector
    @returns {int[]}           decrypted data
    """

def aes_ctr_encrypt(data: list[int], key: list[int], iv: list[int]) -> list[int]:
    """
    Encrypt with aes in counter mode

    @param {int[]} data        cleartext
    @param {int[]} key         16/24/32-Byte cipher key
    @param {int[]} iv          16-Byte initialization vector
    @returns {int[]}           encrypted data
    """

def aes_cbc_decrypt(data: list[int], key: list[int], iv: list[int]) -> list[int]:
    """
    Decrypt with aes in CBC mode

    @param {int[]} data        cipher
    @param {int[]} key         16/24/32-Byte cipher key
    @param {int[]} iv          16-Byte IV
    @returns {int[]}           decrypted data
    """

def aes_cbc_encrypt(data: list[int], key: list[int], iv: list[int], *, padding_mode: str = "pkcs7") -> list[int]:
    """
    Encrypt with aes in CBC mode

    @param {int[]} data        cleartext
    @param {int[]} key         16/24/32-Byte cipher key
    @param {int[]} iv          16-Byte IV
    @param padding_mode        Padding mode to use
    @returns {int[]}           encrypted data
    """

def aes_gcm_decrypt_and_verify(data: list[int], key: list[int], tag: list[int], nonce: list[int]) -> list[int]:
    """
    Decrypt with aes in GBM mode and checks authenticity using tag

    @param {int[]} data        cipher
    @param {int[]} key         16-Byte cipher key
    @param {int[]} tag         authentication tag
    @param {int[]} nonce       IV (recommended 12-Byte)
    @returns {int[]}           decrypted data
    """

def aes_encrypt(data: list[int], expanded_key: list[int]) -> list[int]:
    """
    Encrypt one block with aes

    @param {int[]} data          16-Byte state
    @param {int[]} expanded_key  176/208/240-Byte expanded key
    @returns {int[]}             16-Byte cipher
    """

def aes_decrypt(data: list[int], expanded_key: list[int]) -> list[int]:
    """
    Decrypt one block with aes

    @param {int[]} data          16-Byte cipher
    @param {int[]} expanded_key  176/208/240-Byte expanded key
    @returns {int[]}             16-Byte state
    """

def aes_decrypt_text(data: str | ReadableBuffer, password: str, key_size_bytes: int) -> str:
    """
    Decrypt text
    - The first 8 Bytes of decoded 'data' are the 8 high Bytes of the counter
    - The cipher key is retrieved by encrypting the first 16 Byte of 'password'
      with the first 'key_size_bytes' Bytes from 'password' (if necessary filled with 0's)
    - Mode of operation is 'counter'

    @param {str} data                    Base64 encoded string
    @param {str,unicode} password        Password (will be encoded with utf-8)
    @param {int} key_size_bytes          Possible values: 16 for 128-Bit, 24 for 192-Bit or 32 for 256-Bit
    @returns {str}                       Decrypted data
    """

def key_expansion(data: list[int]) -> list[int]:
    """
    Generate key schedule

    @param {int[]} data  16/24/32-Byte cipher key
    @returns {int[]}     176/208/240-Byte expanded key
    """
