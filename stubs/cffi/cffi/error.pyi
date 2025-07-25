class FFIError(Exception):
    __module__: str

class CDefError(Exception):
    __module__: str

class VerificationError(Exception):
    """An error raised when verification fails"""

    __module__: str

class VerificationMissing(Exception):
    """An error raised when incomplete structures are passed into
    cdef, but no verification has been done
    """

    __module__: str

class PkgConfigError(Exception):
    """An error raised for missing modules in pkg-config"""

    __module__: str
