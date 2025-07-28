def fingerprint128(a: str, /) -> tuple[int, int]:
    """Fingerprint (i.e., good, portable, forever-fixed hash) function for a bytes-like object.  Returns a tuple of two unsigned 64-bit integers: (low64, high64).
    example: print farmhash.fingerprint128('abc')
    (13364216625615136468L, 11320522948082609695L)
    """

def fingerprint32(a: str, /) -> int:
    """Fingerprint (i.e., good, portable, forever-fixed hash) function for a bytes-like object.  Most useful in 32-bit binaries.
    example: print farmhash.fingerprint32('abc')
    2521517342
    """

def fingerprint64(a: str, /) -> int:
    """Fingerprint (i.e., good, portable, forever-fixed hash) function for a bytes-like object.  Returns an unsigned 64-bit integer.
    example: print farmhash.fingerprint64('abc')
    2640714258260161385L
    """

def hash128(a: str, /) -> tuple[int, int]:
    """Hash function for a bytes-like object.  Returns a tuple of two unsigned 64-bit integers: (low64, high64).
    example: print farmhash.hash128('abc')
    (4143508125394299908L, 11566915719555882565L)
    """

def hash128withseed(a: str, seed_low: int, seed_high: int, /) -> tuple[int, int]:
    """Hash function for a bytes-like object. For convenience, two 32-bit seeds are also hashed into the result.
    example: print farmhash.hash128withseed('abc', 1234, 0)
    (13364216625615136468L, 11320522948082609695L)
    """

def hash32(a: str, /) -> int:
    """Hash function for a bytes-like object.  Most useful in 32-bit binaries.
    example: print farmhash.hash32('abc')
    2521517342
    """

def hash32withseed(a: str, seed: int, /) -> int:
    """Hash function for a bytes-like object.  For convenience, a 32-bit seed is also hashed into the result.
    example: print farmhash.hash32withseed('abc', 1234)
    2521517342
    """

def hash64(a: str, /) -> int:
    """Hash function for a bytes-like object.  Returns an unsigned 64-bit integer.
    example: print farmhash.hash64('abc')
    2640714258260161385L
    """

def hash64withseed(a: str, seed: int, /) -> int:
    """Hash function for a bytes-like object.  For convenience, a 64-bit seed is also hashed into the result.
    example: print farmhash.hash64withseed('abc', 12345)
    13914286602242141520L
    """
