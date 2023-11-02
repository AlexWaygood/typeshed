import codecs
from _typeshed import Incomplete

class Codec(codecs.Codec):
    def encode(self, input, errors: str = 'strict'): ...
    def decode(self, input, errors: str = 'strict'): ...

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final: bool = False): ...

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final: bool = False): ...

class StreamWriter(Codec, codecs.StreamWriter): ...
class StreamReader(Codec, codecs.StreamReader): ...

def getregentry(): ...

decoding_map: Incomplete
decoding_table: str
encoding_map: Incomplete
