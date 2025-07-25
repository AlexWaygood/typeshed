"""authlib.oauth2.rfc7523.
~~~~~~~~~~~~~~~~~~~~~~

This module represents a direct implementation of
JSON Web Token (JWT) Profile for OAuth 2.0 Client
Authentication and Authorization Grants.

https://tools.ietf.org/html/rfc7523
"""

from .assertion import client_secret_jwt_sign as client_secret_jwt_sign, private_key_jwt_sign as private_key_jwt_sign
from .auth import ClientSecretJWT as ClientSecretJWT, PrivateKeyJWT as PrivateKeyJWT
from .client import JWTBearerClientAssertion as JWTBearerClientAssertion
from .jwt_bearer import JWTBearerGrant as JWTBearerGrant
from .token import JWTBearerTokenGenerator as JWTBearerTokenGenerator
from .validator import JWTBearerToken as JWTBearerToken, JWTBearerTokenValidator as JWTBearerTokenValidator

__all__ = [
    "JWTBearerGrant",
    "JWTBearerClientAssertion",
    "client_secret_jwt_sign",
    "private_key_jwt_sign",
    "ClientSecretJWT",
    "PrivateKeyJWT",
    "JWTBearerToken",
    "JWTBearerTokenGenerator",
    "JWTBearerTokenValidator",
]
