import ssl
from asyncio.events import AbstractEventLoop
from asyncio.protocols import BaseProtocol
from collections.abc import Callable
from typing import Any
from typing_extensions import TypeAlias

ProtocolFactory: TypeAlias = Callable[[], BaseProtocol]
ExceptionHandlerContext: TypeAlias = dict[str, Any]
LoopExceptionHandler: TypeAlias = Callable[[AbstractEventLoop, ExceptionHandlerContext], object]
SSLContext: TypeAlias = bool | None | ssl.SSLContext
