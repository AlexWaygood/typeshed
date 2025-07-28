"""Protobuf Runtime versions and validators.

It should only be accessed by Protobuf gencodes and tests. DO NOT USE it
elsewhere.
"""

from enum import Enum
from typing import Final

class Domain(Enum):
    GOOGLE_INTERNAL = 1
    PUBLIC = 2

OSS_DOMAIN: Final[Domain]
OSS_MAJOR: Final[int]
OSS_MINOR: Final[int]
OSS_PATCH: Final[int]
OSS_SUFFIX: Final[str]
DOMAIN: Final[Domain]
MAJOR: Final[int]
MINOR: Final[int]
PATCH: Final[int]
SUFFIX: Final[str]

class VersionError(Exception):
    """Exception class for version violation."""

def ValidateProtobufRuntimeVersion(
    gen_domain: Domain, gen_major: int, gen_minor: int, gen_patch: int, gen_suffix: str, location: str
) -> None:
    """Function to validate versions.

    Args:
      gen_domain: The domain where the code was generated from.
      gen_major: The major version number of the gencode.
      gen_minor: The minor version number of the gencode.
      gen_patch: The patch version number of the gencode.
      gen_suffix: The version suffix e.g. '-dev', '-rc1' of the gencode.
      location: The proto location that causes the version violation.

    Raises:
      VersionError: if gencode version is invalid or incompatible with the
      runtime.
    """
