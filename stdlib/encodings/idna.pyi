import codecs
from _typeshed import Incomplete

dots: Incomplete
ace_prefix: bytes
sace_prefix: str

def nameprep(label): ...
def ToASCII(label): ...
def ToUnicode(label): ...

class Codec(codecs.Codec):
    def encode(self, input, errors: str = "strict"): ...
    def decode(self, input, errors: str = "strict"): ...

class IncrementalEncoder(codecs.BufferedIncrementalEncoder): ...
class IncrementalDecoder(codecs.BufferedIncrementalDecoder): ...
class StreamWriter(Codec, codecs.StreamWriter): ...
class StreamReader(Codec, codecs.StreamReader): ...

def getregentry(): ...
