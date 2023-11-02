import codecs
from codecs import oem_decode, oem_encode

encode = oem_encode

def decode(input, errors: str = "strict"): ...

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input: str, final: bool = False) -> bytes: ...

class IncrementalDecoder(codecs.BufferedIncrementalDecoder): ...

class StreamWriter(codecs.StreamWriter):
    encode = oem_encode

class StreamReader(codecs.StreamReader):
    decode = oem_decode

def getregentry() -> codecs.CodecInfo: ...
