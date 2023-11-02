import codecs
from _typeshed import Incomplete

class Codec(codecs.Codec):
    encode: Incomplete
    decode: Incomplete

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input: str, final: bool = False) -> bytes: ...

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final: bool = False) -> str: ...

class StreamWriter(Codec, codecs.StreamWriter): ...
class StreamReader(Codec, codecs.StreamReader): ...

class StreamConverter(StreamWriter, StreamReader):
    encode: Incomplete
    decode: Incomplete

def getregentry() -> codecs.CodecInfo: ...
