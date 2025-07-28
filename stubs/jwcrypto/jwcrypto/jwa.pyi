from abc import ABCMeta, abstractmethod
from collections.abc import Mapping
from typing import ClassVar

default_max_pbkdf2_iterations: int

class JWAAlgorithm(metaclass=ABCMeta):
    @property
    @abstractmethod
    def name(self) -> str:
        """The algorithm Name"""

    @property
    @abstractmethod
    def description(self) -> str:
        """A short description"""

    @property
    @abstractmethod
    def keysize(self) -> int:
        """The algorithm key size"""

    @property
    @abstractmethod
    def algorithm_usage_location(self) -> str:
        """One of 'alg', 'enc' or 'JWK'"""

    @property
    @abstractmethod
    def algorithm_use(self) -> str:
        """One of 'sig', 'kex', 'enc'"""

    @property
    def input_keysize(self) -> int:
        """The input key size"""

class JWA:
    """JWA Signing Algorithms.

    This class provides access to all JWA algorithms.
    """

    algorithms_registry: ClassVar[Mapping[str, JWAAlgorithm]]
    @classmethod
    def instantiate_alg(cls, name: str, use: str | None = None) -> JWAAlgorithm: ...
    @classmethod
    def signing_alg(cls, name: str) -> JWAAlgorithm: ...
    @classmethod
    def keymgmt_alg(cls, name: str) -> JWAAlgorithm: ...
    @classmethod
    def encryption_alg(cls, name: str) -> JWAAlgorithm: ...
