from typing import Any
from typing_extensions import Self

class Key:
    """
    A simple interface for implementing JWK keys.
    """

    # Enable when we can use stubs from installed dependencies,
    # as `key` can be of type cryptography.x509.base.Certificate:
    # from cryptography.x509 import Certificate
    def __init__(self, key, algorithm) -> None: ...
    def sign(self, msg: bytes) -> bytes: ...
    def verify(self, msg: bytes, sig: bytes) -> bool: ...
    def public_key(self) -> Self: ...
    def to_pem(self) -> bytes: ...
    def to_dict(self) -> dict[str, Any]: ...
    def encrypt(self, plain_text: str | bytes, aad: bytes | None = None) -> tuple[bytes, bytes, bytes | None]:
        """
        Encrypt the plain text and generate an auth tag if appropriate

        Args:
            plain_text (bytes): Data to encrypt
            aad (bytes, optional): Authenticated Additional Data if key's algorithm supports auth mode

        Returns:
            (bytes, bytes, bytes): IV, cipher text, and auth tag
        """

    def decrypt(
        self, cipher_text: str | bytes, iv: str | bytes | None = None, aad: bytes | None = None, tag: bytes | None = None
    ) -> bytes:
        """
        Decrypt the cipher text and validate the auth tag if present
        Args:
            cipher_text (bytes): Cipher text to decrypt
            iv (bytes): IV if block mode
            aad (bytes): Additional Authenticated Data to verify if auth mode
            tag (bytes): Authentication tag if auth mode

        Returns:
            bytes: Decrypted value
        """

    def wrap_key(self, key_data: bytes) -> bytes:
        """
        Wrap the the plain text key data

        Args:
            key_data (bytes): Key data to wrap

        Returns:
            bytes: Wrapped key
        """

    def unwrap_key(self, wrapped_key: bytes) -> bytes:
        """
        Unwrap the the wrapped key data

        Args:
            wrapped_key (bytes): Wrapped key data to unwrap

        Returns:
            bytes: Unwrapped key
        """

class DIRKey(Key):
    def __init__(self, key_data: str | bytes, algorithm: str) -> None: ...
    def to_dict(self) -> dict[str, Any]: ...
