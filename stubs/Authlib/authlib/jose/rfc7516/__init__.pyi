"""authlib.jose.rfc7516.
~~~~~~~~~~~~~~~~~~~~~

This module represents a direct implementation of
JSON Web Encryption (JWE).

https://tools.ietf.org/html/rfc7516
"""

from .jwe import JsonWebEncryption as JsonWebEncryption
from .models import (
    JWEAlgorithm as JWEAlgorithm,
    JWEAlgorithmWithTagAwareKeyAgreement as JWEAlgorithmWithTagAwareKeyAgreement,
    JWEEncAlgorithm as JWEEncAlgorithm,
    JWEZipAlgorithm as JWEZipAlgorithm,
)

__all__ = ["JsonWebEncryption", "JWEAlgorithm", "JWEAlgorithmWithTagAwareKeyAgreement", "JWEEncAlgorithm", "JWEZipAlgorithm"]
