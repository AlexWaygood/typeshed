import codecs

def segregate(str): ...
def selective_len(str, max): ...
def selective_find(str, char, index, pos): ...
def insertion_unsort(str, extended): ...
def T(j, bias): ...

digits: bytes

def generate_generalized_integer(N, bias): ...
def adapt(delta, first, numchars): ...
def generate_integers(baselen, deltas): ...
def punycode_encode(text): ...
def decode_generalized_number(extended, extpos, bias, errors): ...
def insertion_sort(base, extended, errors): ...
def punycode_decode(text, errors): ...

class Codec(codecs.Codec):
    def encode(self, input, errors: str = "strict"): ...
    def decode(self, input, errors: str = "strict"): ...

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input: str, final: bool = False) -> bytes: ...

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final: bool = False) -> str: ...

class StreamWriter(Codec, codecs.StreamWriter): ...
class StreamReader(Codec, codecs.StreamReader): ...

def getregentry() -> codecs.CodecInfo: ...
