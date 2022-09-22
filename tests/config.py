from dataclasses import dataclass, field
from functools import cached_property
from typing import Any

import tomli

from utils import minor_version_from_version_string


@dataclass
class TypeshedConfig:
    min_supported_version: str
    max_supported_version: str
    supported_platforms: list[str]
    supported_versions: list[str] = field(init=False)

    def __post_init__(self) -> None:
        minor_version_range = range(
            minor_version_from_version_string(self.max_supported_version),
            minor_version_from_version_string(self.min_supported_version) - 1,
            -1,
        )
        self.supported_versions = [f"3.{minor_ver}" for minor_ver in minor_version_range]


def get_typeshed_config() -> TypeshedConfig:
    with open("pyproject.toml", "rb") as f:
        data = tomli.load(f)["tool"]["typeshed"]

    return TypeshedConfig(
        min_supported_version=data["min_supported_version"],
        max_supported_version=data["max_supported_version"],
        supported_platforms=data["supported_platforms"],
    )
