import codecs
from _typeshed import Incomplete

encode: Incomplete

def decode(input, errors: str = 'strict'): ...

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final: bool = False): ...

class IncrementalDecoder(codecs.BufferedIncrementalDecoder): ...

class StreamWriter(codecs.StreamWriter):
    encode: Incomplete

class StreamReader(codecs.StreamReader):
    decode: Incomplete

def getregentry(): ...
