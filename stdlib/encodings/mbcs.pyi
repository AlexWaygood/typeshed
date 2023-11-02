import codecs
from codecs import mbcs_decode, mbcs_encode

encode = mbcs_encode

def decode(input, errors: str = "strict"): ...

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input: str, final: bool = False) -> bytes: ...

class IncrementalDecoder(codecs.BufferedIncrementalDecoder): ...

class StreamWriter(codecs.StreamWriter):
    encode = mbcs_encode

class StreamReader(codecs.StreamReader):
    decode = mbcs_decode

def getregentry() -> codecs.CodecInfo: ...
