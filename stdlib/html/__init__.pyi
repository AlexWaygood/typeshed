from typing import AnyStr

__all__ = ["escape", "unescape"]

def escape[AnyStr: (bytes, str)](s: AnyStr, quote: bool = True) -> AnyStr: ...
def unescape[AnyStr: (bytes, str)](s: AnyStr) -> AnyStr: ...
