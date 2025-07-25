"""ASN1 encoding helpers for converting between PKCS1 and PKCS8.

Required by rsa_backend but not cryptography_backend.
"""

from pyasn1.type import namedtype, univ

RSA_ENCRYPTION_ASN1_OID: str

class RsaAlgorithmIdentifier(univ.Sequence):
    """ASN1 structure for recording RSA PrivateKeyAlgorithm identifiers."""

    componentType: namedtype.NamedTypes

class PKCS8PrivateKey(univ.Sequence):
    """ASN1 structure for recording PKCS8 private keys."""

    componentType: namedtype.NamedTypes

class PublicKeyInfo(univ.Sequence):
    """ASN1 structure for recording PKCS8 public keys."""

    componentType: namedtype.NamedTypes

def rsa_private_key_pkcs8_to_pkcs1(pkcs8_key) -> bytes:
    """Convert a PKCS8-encoded RSA private key to PKCS1."""

def rsa_private_key_pkcs1_to_pkcs8(pkcs1_key) -> bytes:
    """Convert a PKCS1-encoded RSA private key to PKCS8."""

def rsa_public_key_pkcs1_to_pkcs8(pkcs1_key) -> bytes:
    """Convert a PKCS1-encoded RSA private key to PKCS8."""

def rsa_public_key_pkcs8_to_pkcs1(pkcs8_key) -> bytes:
    """Convert a PKCS8-encoded RSA private key to PKCS1."""
