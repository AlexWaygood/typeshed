"""
Copyright (c) 2015 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

from collections.abc import Generator, Mapping, MutableMapping
from io import StringIO
from typing import ClassVar, Literal
from typing_extensions import TypeAlias

def b2u(string: bytes | str) -> str:
    """bytes to unicode"""

def u2b(string: str | bytes) -> bytes:
    """unicode to bytes"""

_Quotes: TypeAlias = Literal["'", '"']
_ContextType: TypeAlias = Literal["ARG", "ENV", "LABEL"]

class WordSplitter:
    """
    Split string into words, substituting environment variables if provided

    Methods defined here:

    dequote()
        Returns the string with escaped and quotes consumed

    split(maxsplit=None, dequote=True)
        Returns an iterable of words, split at whitespace
    """

    SQUOTE: ClassVar[_Quotes]
    DQUOTE: ClassVar[_Quotes]
    stream: StringIO
    args: Mapping[str, str] | None
    envs: Mapping[str, str] | None
    quotes: _Quotes | None
    escaped: bool
    def __init__(self, s: str, args: Mapping[str, str] | None = None, envs: Mapping[str, str] | None = None) -> None:
        """
        :param s: str, string to process
        :param args: dict, build arguments to use; if None, do not
            attempt substitution
        :param envs: dict, environment variables to use; if None, do not
            attempt substitution
        """

    def dequote(self) -> str: ...
    def split(self, maxsplit: int | None = None, dequote: bool = True) -> Generator[str | None]:
        """
        Generator for the words of the string

        :param maxsplit: perform at most maxsplit splits;
            if None, do not limit the number of splits
        :param dequote: remove quotes and escape characters once consumed
        """

def extract_key_values(
    env_replace: bool, args: Mapping[str, str], envs: Mapping[str, str], instruction_value: str
) -> list[tuple[str, str]]: ...
def get_key_val_dictionary(
    instruction_value: str,
    env_replace: bool = False,
    args: Mapping[str, str] | None = None,
    envs: Mapping[str, str] | None = None,
) -> dict[str, str]: ...

class Context:
    args: MutableMapping[str, str]
    envs: MutableMapping[str, str]
    labels: MutableMapping[str, str]
    line_args: Mapping[str, str]
    line_envs: Mapping[str, str]
    line_labels: Mapping[str, str]
    def __init__(
        self,
        args: MutableMapping[str, str] | None = None,
        envs: MutableMapping[str, str] | None = None,
        labels: MutableMapping[str, str] | None = None,
        line_args: Mapping[str, str] | None = None,
        line_envs: Mapping[str, str] | None = None,
        line_labels: Mapping[str, str] | None = None,
    ) -> None:
        """
        Class representing current state of build arguments, environment variables and labels.

        :param args: dict with arguments valid for this line
            (all variables defined to this line)
        :param envs: dict with variables valid for this line
            (all variables defined to this line)
        :param labels: dict with labels valid for this line
            (all labels defined to this line)
        :param line_args: dict with arguments defined on this line
        :param line_envs: dict with variables defined on this line
        :param line_labels: dict with labels defined on this line
        """

    def set_line_value(self, context_type: _ContextType, value: Mapping[str, str]) -> None:
        """
        Set value defined on this line ('line_args'/'line_envs'/'line_labels')
        and update 'args'/'envs'/'labels'.

        :param context_type: "ARG" or "ENV" or "LABEL"
        :param value: new value for this line
        """

    def get_line_value(self, context_type: _ContextType) -> Mapping[str, str]:
        """
        Get the values defined on this line.

        :param context_type: "ARG" or "ENV" or "LABEL"
        :return: values of given type defined on this line
        """

    def get_values(self, context_type: _ContextType) -> Mapping[str, str]:
        """
        Get the values valid on this line.

        :param context_type: "ARG" or "ENV" or "LABEL"
        :return: values of given type valid on this line
        """
