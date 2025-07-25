from typing import Any

from .backends.base import Key

def encrypt(
    plaintext: str | bytes,
    # Internally it's passed down to jwk.construct(), which explicitly checks for
    # key as dict instance, instead of a Mapping
    key: str | bytes | dict[str, Any] | Key,
    encryption: str = "A256GCM",
    algorithm: str = "dir",
    zip: str | None = None,
    cty: str | None = None,
    kid: str | None = None,
) -> bytes:
    """Encrypts plaintext and returns a JWE compact serialization string.

    Args:
        plaintext (bytes): A bytes object to encrypt
        key (str or dict): The key(s) to use for encrypting the content. Can be
            individual JWK or JWK set.
        encryption (str, optional): The content encryption algorithm used to
            perform authenticated encryption on the plaintext to produce the
            ciphertext and the Authentication Tag.  Defaults to A256GCM.
        algorithm (str, optional): The cryptographic algorithm used
            to encrypt or determine the value of the CEK.  Defaults to dir.
        zip (str, optional): The compression algorithm) applied to the
            plaintext before encryption. Defaults to None.
        cty (str, optional): The media type for the secured content.
            See http://www.iana.org/assignments/media-types/media-types.xhtml
        kid (str, optional): Key ID for the provided key

    Returns:
        bytes: The string representation of the header, encrypted key,
            initialization vector, ciphertext, and authentication tag.

    Raises:
        JWEError: If there is an error signing the token.

    Examples:
        >>> from jose import jwe
        >>> jwe.encrypt('Hello, World!', 'asecret128bitkey', algorithm='dir', encryption='A128GCM')
        'eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4R0NNIn0..McILMB3dYsNJSuhcDzQshA.OfX9H_mcUpHDeRM4IA.CcnTWqaqxNsjT4eCaUABSg'

    """

def decrypt(
    jwe_str: str | bytes,
    # Internally it's passed down to jwk.construct(), which explicitly checks for
    # key as dict instance, instead of a Mapping
    key: str | bytes | dict[str, Any] | Key,
) -> bytes | None:
    """Decrypts a JWE compact serialized string and returns the plaintext.

    Args:
        jwe_str (str): A JWE to be decrypt.
        key (str or dict): A key to attempt to decrypt the payload with. Can be
            individual JWK or JWK set.

    Returns:
        bytes: The plaintext bytes, assuming the authentication tag is valid.

    Raises:
        JWEError: If there is an exception verifying the token.

    Examples:
        >>> from jose import jwe
        >>> jwe.decrypt(jwe_string, 'asecret128bitkey')
        'Hello, World!'
    """

def get_unverified_header(jwe_str: str | bytes | None) -> dict[str, Any]:
    """Returns the decoded headers without verification of any kind.

    Args:
        jwe_str (str): A compact serialized JWE to decode the headers from.

    Returns:
        dict: The dict representation of the JWE headers.

    Raises:
        JWEError: If there is an exception decoding the JWE.
    """
