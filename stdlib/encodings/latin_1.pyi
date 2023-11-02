import codecs
from _typeshed import Incomplete

class Codec(codecs.Codec):
    encode: Incomplete
    decode: Incomplete

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final: bool = False): ...

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final: bool = False): ...

class StreamWriter(Codec, codecs.StreamWriter): ...
class StreamReader(Codec, codecs.StreamReader): ...

class StreamConverter(StreamWriter, StreamReader):
    encode: Incomplete
    decode: Incomplete

def getregentry(): ...
