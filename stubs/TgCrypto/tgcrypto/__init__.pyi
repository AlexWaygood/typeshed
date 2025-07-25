"""Fast and Portable Cryptography Extension Library for Pyrogram
TgCrypto is part of Pyrogram, a Telegram MTProto library for Python
You can learn more about Pyrogram here: https://pyrogram.org
"""

from typing_extensions import Buffer

def ige256_encrypt(data: Buffer, key: Buffer, iv: Buffer, /) -> bytes:
    """AES-256-IGE Encryption"""

def ige256_decrypt(data: Buffer, key: Buffer, iv: Buffer, /) -> bytes:
    """AES-256-IGE Decryption"""

def ctr256_encrypt(data: Buffer, key: Buffer, iv: Buffer, state: Buffer, /) -> bytes:
    """AES-256-CTR Encryption"""

def ctr256_decrypt(data: Buffer, key: Buffer, iv: Buffer, state: Buffer, /) -> bytes:
    """AES-256-CTR Decryption"""

def cbc256_encrypt(data: Buffer, key: Buffer, iv: Buffer, /) -> bytes:
    """AES-256-CBC Encryption"""

def cbc256_decrypt(data: Buffer, key: Buffer, iv: Buffer, /) -> bytes:
    """AES-256-CBC Encryption"""
