import codecs

def quopri_encode(input, errors: str = 'strict'): ...
def quopri_decode(input, errors: str = 'strict'): ...

class Codec(codecs.Codec):
    def encode(self, input, errors: str = 'strict'): ...
    def decode(self, input, errors: str = 'strict'): ...

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final: bool = False): ...

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final: bool = False): ...

class StreamWriter(Codec, codecs.StreamWriter):
    charbuffertype = bytes

class StreamReader(Codec, codecs.StreamReader):
    charbuffertype = bytes

def getregentry(): ...
