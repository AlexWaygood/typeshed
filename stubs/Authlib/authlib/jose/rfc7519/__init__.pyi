"""authlib.jose.rfc7519.
~~~~~~~~~~~~~~~~~~~~

This module represents a direct implementation of
JSON Web Token (JWT).

https://tools.ietf.org/html/rfc7519
"""

from .claims import BaseClaims as BaseClaims, JWTClaims as JWTClaims
from .jwt import JsonWebToken as JsonWebToken

__all__ = ["JsonWebToken", "BaseClaims", "JWTClaims"]
