from contextlib import AbstractContextManager
from typing import Any, TextIO, TypeVar

from .ansitowin32 import StreamWrapper

_TextIOT = TypeVar("_TextIOT", bound=TextIO)

orig_stdout: TextIO | None
orig_stderr: TextIO | None
wrapped_stdout: TextIO | StreamWrapper
wrapped_stderr: TextIO | StreamWrapper
atexit_done: bool
fixed_windows_console: bool

def reset_all() -> None: ...
def init(autoreset: bool = False, convert: bool | None = None, strip: bool | None = None, wrap: bool = True) -> None: ...
def deinit() -> None: ...
def colorama_text(*args: Any, **kwargs: Any) -> AbstractContextManager[None]: ...
def reinit() -> None: ...
def wrap_stream[_TextIOT: TextIO](
    stream: _TextIOT, convert: bool | None, strip: bool | None, autoreset: bool, wrap: bool
) -> _TextIOT | StreamWrapper: ...
def just_fix_windows_console() -> None: ...
