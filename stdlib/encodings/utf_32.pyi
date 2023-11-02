import codecs
from _typeshed import Incomplete

encode: Incomplete

def decode(input, errors: str = ...): ...

class IncrementalEncoder(codecs.IncrementalEncoder):
    encoder: Incomplete
    def __init__(self, errors: str = ...) -> None: ...
    def encode(self, input, final: bool = ...): ...
    def reset(self) -> None: ...
    def getstate(self): ...
    def setstate(self, state) -> None: ...

class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    decoder: Incomplete
    def __init__(self, errors: str = ...) -> None: ...
    def reset(self) -> None: ...
    def getstate(self): ...
    def setstate(self, state) -> None: ...

class StreamWriter(codecs.StreamWriter):
    encoder: Incomplete
    def __init__(self, stream, errors: str = ...) -> None: ...
    def reset(self) -> None: ...
    def encode(self, input, errors: str = ...): ...

class StreamReader(codecs.StreamReader):
    def reset(self) -> None: ...
    def decode(self, input, errors: str = ...): ...

def getregentry(): ...
