from authlib.jose.rfc7516 import JWEZipAlgorithm

class DeflateZipAlgorithm(JWEZipAlgorithm):
    name: str
    description: str
    def compress(self, s):
        """Compress bytes data with DEFLATE algorithm."""

    def decompress(self, s):
        """Decompress DEFLATE bytes data."""

def register_jwe_rfc7518() -> None: ...
