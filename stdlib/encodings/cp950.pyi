import abc
import codecs
from _typeshed import Incomplete

import _multibytecodec as mbc

codec: Incomplete

class Codec(codecs.Codec):
    encode: Incomplete
    decode: Incomplete

class IncrementalEncoder(mbc.MultibyteIncrementalEncoder, codecs.IncrementalEncoder, metaclass=abc.ABCMeta):
    codec = codec

class IncrementalDecoder(mbc.MultibyteIncrementalDecoder, codecs.IncrementalDecoder, metaclass=abc.ABCMeta):
    codec = codec

class StreamReader(Codec, mbc.MultibyteStreamReader, codecs.StreamReader):
    codec = codec

class StreamWriter(Codec, mbc.MultibyteStreamWriter, codecs.StreamWriter):
    codec = codec

def getregentry() -> codecs.CodecInfo: ...
