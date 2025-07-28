"""
Copyright (c) 2015, 2018, 2019 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

import logging
from collections.abc import Mapping, Sequence
from typing import IO, ClassVar, TypedDict

from .util import Context

logger: logging.Logger

class KeyValues(dict[str, str]):
    """
    Abstract base class for allowing direct write access to Dockerfile
    instructions which result in a set of key value pairs.

    Subclasses must override the `parser_attr` value.
    """

    parser_attr: ClassVar[str | None]
    parser: DockerfileParser
    def __init__(self, key_values: Mapping[str, str], parser: DockerfileParser) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __setitem__(self, key: str, value: str) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...  # type: ignore[override]

class Labels(KeyValues):
    """
    A class for allowing direct write access to Dockerfile labels, e.g.:

    parser.labels['label'] = 'value'
    """

class Envs(KeyValues):
    """
    A class for allowing direct write access to Dockerfile env. vars., e.g.:

    parser.envs['variable_name'] = 'value'
    """

class Args(KeyValues):
    """
    A class for allowing direct write access to Dockerfile build args, e.g.:

    parser.args['variable_name'] = 'value'
    """

class _InstructionDict(TypedDict):
    instruction: str
    startline: int
    endline: int
    content: str
    value: str

class DockerfileParser:
    fileobj: IO[str]
    dockerfile_path: str
    cache_content: bool
    cached_content: str
    env_replace: bool
    parent_env: dict[str, str]
    build_args: dict[str, str]
    def __init__(
        self,
        path: str | None = None,
        cache_content: bool = False,
        env_replace: bool = True,
        parent_env: dict[str, str] | None = None,
        fileobj: IO[str] | None = None,
        build_args: dict[str, str] | None = None,
    ) -> None:
        """
        Initialize source of Dockerfile
        :param path: path to (directory with) Dockerfile; if not provided,
                     and fileobj is not provided, the current working
                     directory will be used
        :param cache_content: cache Dockerfile content inside DockerfileParser
        :param env_replace: return content with variables replaced
        :param parent_env: python dict of inherited env vars from parent image
        :param fileobj: seekable file-like object containing Dockerfile content
                        as bytes (will be truncated on write)
        :param build_args: python dict of build args used when building image
        """
    lines: list[str]
    content: str
    @property
    def structure(self) -> list[_InstructionDict]:
        """
        Returns a list of dicts describing the commands:
        [
            {"instruction": "FROM",       # always upper-case
             "startline": 0,              # 0-based
             "endline": 0,                # 0-based
             "content": "From fedora
",
             "value": "fedora"},

            {"instruction": "CMD",
             "startline": 1,
             "endline": 2,
             "content": "CMD yum -y update && \\
    yum clean all
",
             "value": "yum -y update && yum clean all"}
        ]
        """

    @property
    def json(self) -> str:
        """
        :return: JSON formatted string with instructions & values from Dockerfile
        """
    parent_images: Sequence[str]
    @property
    def is_multistage(self) -> bool: ...
    baseimage: str
    cmd: str
    labels: Mapping[str, str]
    envs: Mapping[str, str]
    args: Mapping[str, str]
    def add_lines(
        self, *lines: str, all_stages: bool | None = ..., at_start: bool | None = ..., skip_scratch: bool | None = ...
    ) -> None:
        """
        Add lines to the beginning or end of the build.
        :param lines: one or more lines to add to the content, by default at the end.
        :param all_stages: bool for whether to add in all stages for a multistage build
                           or (by default) only the last.
        :param at_start: adds at the beginning (after FROM) of the stage(s) instead of the end.
        :param skip_scratch: skip stages which use "FROM scratch"
        """

    def add_lines_at(
        self, anchor: str | int | dict[str, int], *lines: str, replace: bool | None = ..., after: bool | None = ...
    ) -> None:
        """
        Add lines at a specific location in the file.
        :param anchor: structure_dict|line_str|line_num a reference to where adds should occur
        :param lines: one or more lines to add to the content
        :param replace: if True -- replace the anchor
        :param after: if True -- insert after the anchor (conflicts with "replace")
        """

    @property
    def context_structure(self) -> list[Context]:
        """
        :return: list of Context objects
            (Contains info about build arguments, labels, and environment variables for each line.)
        """

def image_from(from_value: str) -> tuple[str | None, str | None]:
    """
    :param from_value: string like "image:tag" or "image:tag AS name"
    :return: tuple of the image and stage name, e.g. ("image:tag", None)
    """
