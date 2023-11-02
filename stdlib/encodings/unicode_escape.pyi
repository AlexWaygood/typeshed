import codecs
from _typeshed import Incomplete

class Codec(codecs.Codec):
    encode: Incomplete
    decode: Incomplete

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final: bool = False): ...

class IncrementalDecoder(codecs.BufferedIncrementalDecoder): ...
class StreamWriter(Codec, codecs.StreamWriter): ...

class StreamReader(Codec, codecs.StreamReader):
    def decode(self, input, errors: str = 'strict'): ...

def getregentry(): ...
