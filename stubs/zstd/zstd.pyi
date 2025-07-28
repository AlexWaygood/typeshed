from _typeshed import ReadableBuffer

class Error(Exception): ...

def ZSTD_compress(data: ReadableBuffer, level: int = ..., threads: int = ..., /) -> bytes:
    """compress_mt(string[, level, threads]): bytes -- Returns compressed string.

    Optional arg level is the compression level, from 1 (fastest) to 22 (slowest). The default value is 3.
    Optional arg threads is the number of worker threads, from 0 to 200. 0 - auto-tune by cpu cores count. The default value is 0.
    Also supports ultra-fast levels from -100 (fastest) to -1 (less fast) since module compiled with ZSTD 1.3.4+.

    Input data length limited by 2Gb by Python API.
    Raises a zstd.Error exception if any error occurs.
    """

compress = ZSTD_compress
compress_real_mt = ZSTD_compress
dumps = ZSTD_compress
encode = ZSTD_compress

def ZSTD_check(data: ReadableBuffer) -> int:
    """check(bytes): string -- Returns 0 or 1.

    Raises a zstd.Error exception if any error occurs.
    """

check = ZSTD_check
verify = ZSTD_check

def ZSTD_uncompress(data: ReadableBuffer, /) -> bytes:
    """decompress(bytes): string -- Returns uncompressed string.

    Raises a zstd.Error exception if any error occurs.
    """

decompress = ZSTD_uncompress
uncompress = ZSTD_uncompress
loads = ZSTD_uncompress
decode = ZSTD_uncompress

def ZSTD_version() -> str:
    """ZSTD_version(): string -- Returns ZSTD library version as string."""

def ZSTD_version_number() -> int:
    """ZSTD_version_number(): int -- Returns ZSTD library version as integer.
    Format of the number is: major * 100*100 + minor * 100 + release.
    """

def ZSTD_threads_count() -> int:
    """ZSTD_threads_count(): int -- Returns ZSTD determined CPU cores count in integer."""

def ZSTD_max_threads_count() -> int:
    """ZSTD_max_threads_count(): int -- Returns ZSTD library determined maximum working threads count in integer."""

def ZSTD_external() -> int:
    """ZSTD_external(): int -- Returns 0 or 1 if ZSTD library build as external."""

def ZSTD_with_asm() -> int:
    """ZSTD_with_asm(): int -- Returns 0 or 1 if ZSTD library build with assembler support."""

def ZSTD_with_threads() -> int:
    """ZSTD_with_threads(): int -- Returns 0 or 1 if ZSTD library build with threads support."""

def ZSTD_legacy_support() -> int:
    """ZSTD_legacy_support(): int -- Returns 0 or 1 if ZSTD library build with legacy formats support."""

def ZSTD_max_compression_level() -> int:
    """ZSTD_max_compression_level(): int -- Returns ZSTD library determined maximum number of compression level in integer."""

def ZSTD_min_compression_level() -> int:
    """ZSTD_min_compression_level(): int -- Returns ZSTD library determined minimum number of compression level in integer."""

def ZSTD_default_compression_level() -> int:
    """ZSTD_default_compression_level(): int -- Returns ZSTD library determined default number of compression level in integer, must be 3."""

def ZSTD_is_debug_enabled() -> int: ...
def ZSTD_is_debug_error_enabled() -> int: ...
def ZSTD_is_debug_info_enabled() -> int: ...
def ZSTD_is_debug_notice_enabled() -> int: ...
def version() -> str:
    """version(): string -- Returns this module version as string."""
