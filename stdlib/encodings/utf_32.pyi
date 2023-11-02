import codecs
from _typeshed import Incomplete

encode: Incomplete

def decode(input, errors: str = "strict"): ...

class IncrementalEncoder(codecs.IncrementalEncoder):
    encoder: Incomplete
    def __init__(self, errors: str = "strict") -> None: ...
    def encode(self, input: str, final: bool = False) -> bytes: ...
    def reset(self) -> None: ...
    def getstate(self): ...
    def setstate(self, state) -> None: ...

class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    decoder: Incomplete
    def __init__(self, errors: str = "strict") -> None: ...
    def reset(self) -> None: ...
    def getstate(self): ...
    def setstate(self, state) -> None: ...

class StreamWriter(codecs.StreamWriter):
    encoder: Incomplete
    def __init__(self, stream, errors: str = "strict") -> None: ...
    def reset(self) -> None: ...
    def encode(self, input, errors: str = "strict"): ...

class StreamReader(codecs.StreamReader):
    def reset(self) -> None: ...
    def decode(self, input, errors: str = "strict"): ...

def getregentry() -> codecs.CodecInfo: ...
