"""authlib.jose.draft.
~~~~~~~~~~~~~~~~~~~~

Content Encryption per `Section 4`_.

.. _`Section 4`: https://datatracker.ietf.org/doc/html/draft-amringer-jose-chacha-02#section-4
"""

from _typeshed import Incomplete

from authlib.jose.rfc7516 import JWEEncAlgorithm

class C20PEncAlgorithm(JWEEncAlgorithm):
    IV_SIZE: int
    name: str
    description: str
    key_size: Incomplete
    CEK_SIZE: Incomplete
    def __init__(self, key_size) -> None: ...
    def encrypt(self, msg, aad, iv, key):
        """Content Encryption with AEAD_CHACHA20_POLY1305.

        :param msg: text to be encrypt in bytes
        :param aad: additional authenticated data in bytes
        :param iv: initialization vector in bytes
        :param key: encrypted key in bytes
        :return: (ciphertext, tag)
        """

    def decrypt(self, ciphertext, aad, iv, tag, key):
        """Content Decryption with AEAD_CHACHA20_POLY1305.

        :param ciphertext: ciphertext in bytes
        :param aad: additional authenticated data in bytes
        :param iv: initialization vector in bytes
        :param tag: authentication tag in bytes
        :param key: encrypted key in bytes
        :return: message
        """
