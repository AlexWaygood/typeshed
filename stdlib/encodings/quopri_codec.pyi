import codecs

def quopri_encode(input, errors: str = ...): ...
def quopri_decode(input, errors: str = ...): ...

class Codec(codecs.Codec):
    def encode(self, input, errors: str = ...): ...
    def decode(self, input, errors: str = ...): ...

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final: bool = ...): ...

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final: bool = ...): ...

class StreamWriter(Codec, codecs.StreamWriter):
    charbuffertype = bytes

class StreamReader(Codec, codecs.StreamReader):
    charbuffertype = bytes

def getregentry(): ...
