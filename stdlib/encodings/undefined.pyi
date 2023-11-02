import codecs

class Codec(codecs.Codec):
    def encode(self, input, errors: str = "strict") -> None: ...
    def decode(self, input, errors: str = "strict") -> None: ...

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final: bool = False) -> None: ...

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final: bool = False) -> None: ...

class StreamWriter(Codec, codecs.StreamWriter): ...
class StreamReader(Codec, codecs.StreamReader): ...

def getregentry(): ...
