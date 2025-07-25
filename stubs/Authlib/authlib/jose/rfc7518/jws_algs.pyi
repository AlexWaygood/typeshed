"""authlib.jose.rfc7518.
~~~~~~~~~~~~~~~~~~~~

"alg" (Algorithm) Header Parameter Values for JWS per `Section 3`_.

.. _`Section 3`: https://tools.ietf.org/html/rfc7518#section-3
"""

import hashlib
from _typeshed import Incomplete

from authlib.jose.rfc7515 import JWSAlgorithm

class NoneAlgorithm(JWSAlgorithm):
    name: str
    description: str
    def prepare_key(self, raw_data) -> None: ...
    def sign(self, msg, key): ...
    def verify(self, msg, sig, key) -> bool: ...

class HMACAlgorithm(JWSAlgorithm):
    """HMAC using SHA algorithms for JWS. Available algorithms:

    - HS256: HMAC using SHA-256
    - HS384: HMAC using SHA-384
    - HS512: HMAC using SHA-512
    """

    SHA256 = hashlib.sha256
    SHA384 = hashlib.sha384
    SHA512 = hashlib.sha512
    name: Incomplete
    description: Incomplete
    hash_alg: Incomplete
    def __init__(self, sha_type) -> None: ...
    def prepare_key(self, raw_data): ...
    def sign(self, msg, key): ...
    def verify(self, msg, sig, key) -> bool: ...

class RSAAlgorithm(JWSAlgorithm):
    """RSA using SHA algorithms for JWS. Available algorithms:

    - RS256: RSASSA-PKCS1-v1_5 using SHA-256
    - RS384: RSASSA-PKCS1-v1_5 using SHA-384
    - RS512: RSASSA-PKCS1-v1_5 using SHA-512
    """

    SHA256: Incomplete
    SHA384: Incomplete
    SHA512: Incomplete
    name: Incomplete
    description: Incomplete
    hash_alg: Incomplete
    padding: Incomplete
    def __init__(self, sha_type) -> None: ...
    def prepare_key(self, raw_data): ...
    def sign(self, msg, key): ...
    def verify(self, msg, sig, key) -> bool: ...

class ECAlgorithm(JWSAlgorithm):
    """ECDSA using SHA algorithms for JWS. Available algorithms:

    - ES256: ECDSA using P-256 and SHA-256
    - ES384: ECDSA using P-384 and SHA-384
    - ES512: ECDSA using P-521 and SHA-512
    """

    SHA256: Incomplete
    SHA384: Incomplete
    SHA512: Incomplete
    name: Incomplete
    curve: Incomplete
    description: Incomplete
    hash_alg: Incomplete
    def __init__(self, name, curve, sha_type) -> None: ...
    def prepare_key(self, raw_data): ...
    def sign(self, msg, key): ...
    def verify(self, msg, sig, key) -> bool: ...

class RSAPSSAlgorithm(JWSAlgorithm):
    """RSASSA-PSS using SHA algorithms for JWS. Available algorithms:

    - PS256: RSASSA-PSS using SHA-256 and MGF1 with SHA-256
    - PS384: RSASSA-PSS using SHA-384 and MGF1 with SHA-384
    - PS512: RSASSA-PSS using SHA-512 and MGF1 with SHA-512
    """

    SHA256: Incomplete
    SHA384: Incomplete
    SHA512: Incomplete
    name: Incomplete
    description: Incomplete
    hash_alg: Incomplete
    def __init__(self, sha_type) -> None: ...
    def prepare_key(self, raw_data): ...
    def sign(self, msg, key): ...
    def verify(self, msg, sig, key) -> bool: ...

JWS_ALGORITHMS: list[JWSAlgorithm]
