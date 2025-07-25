from _typeshed import Incomplete, Unused
from abc import ABCMeta, abstractmethod
from collections.abc import Callable

from pyasn1.type import base, char, univ, useful
from pyasn1.type.base import Asn1Type
from pyasn1.type.tag import TagSet

__all__ = ["StreamingDecoder", "Decoder", "decode"]

class AbstractPayloadDecoder:
    protoComponent: Asn1Type | None
    @abstractmethod
    def valueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state=None,
        decodeFun: Callable[..., Incomplete] | None = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ) -> None:
        """Decode value with fixed byte length.

        The decoder is allowed to consume as many bytes as necessary.
        """
    # Abstract, but implementation is optional
    def indefLenValueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state=None,
        decodeFun: Callable[..., Incomplete] | None = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ) -> None:
        """Decode value with undefined length.

        The decoder is allowed to consume as many bytes as necessary.
        """

class AbstractSimplePayloadDecoder(AbstractPayloadDecoder, metaclass=ABCMeta):
    @staticmethod
    def substrateCollector(asn1Object, substrate, length, options): ...

class RawPayloadDecoder(AbstractSimplePayloadDecoder):
    protoComponent: univ.Any
    def valueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Callable[..., Incomplete] | None = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ): ...
    def indefLenValueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Callable[..., Incomplete] | None = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ): ...

class IntegerPayloadDecoder(AbstractSimplePayloadDecoder):
    protoComponent: univ.Integer
    def valueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Unused = None,
        substrateFun: Unused = None,
        **options,
    ): ...

class BooleanPayloadDecoder(IntegerPayloadDecoder):
    protoComponent: univ.Boolean

class BitStringPayloadDecoder(AbstractSimplePayloadDecoder):
    protoComponent: univ.BitString
    supportConstructedForm: bool
    def valueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Callable[..., Incomplete] | None = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ): ...
    def indefLenValueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Callable[..., Incomplete] | None = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ): ...

class OctetStringPayloadDecoder(AbstractSimplePayloadDecoder):
    protoComponent: univ.OctetString
    supportConstructedForm: bool
    def valueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Callable[..., Incomplete] | None = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ): ...
    def indefLenValueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Callable[..., Incomplete] | None = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ): ...

class NullPayloadDecoder(AbstractSimplePayloadDecoder):
    protoComponent: univ.Null
    def valueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Unused = None,
        substrateFun: Unused = None,
        **options,
    ): ...

class ObjectIdentifierPayloadDecoder(AbstractSimplePayloadDecoder):
    protoComponent: univ.ObjectIdentifier
    def valueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Unused = None,
        substrateFun: Unused = None,
        **options,
    ): ...

class RealPayloadDecoder(AbstractSimplePayloadDecoder):
    protoComponent: univ.Real
    def valueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Unused = None,
        substrateFun: Unused = None,
        **options,
    ): ...

class AbstractConstructedPayloadDecoder(AbstractPayloadDecoder, metaclass=ABCMeta):
    protoComponent: base.ConstructedAsn1Type | None

class ConstructedPayloadDecoderBase(AbstractConstructedPayloadDecoder):
    protoRecordComponent: univ.SequenceAndSetBase | None
    protoSequenceComponent: univ.SequenceOfAndSetOfBase | None
    def valueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Callable[..., Incomplete] | None = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ): ...
    def indefLenValueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Callable[..., Incomplete] | None = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ): ...

class SequenceOrSequenceOfPayloadDecoder(ConstructedPayloadDecoderBase):
    protoRecordComponent: univ.Sequence
    protoSequenceComponent: univ.SequenceOf

class SequencePayloadDecoder(SequenceOrSequenceOfPayloadDecoder):
    protoComponent: univ.Sequence

class SequenceOfPayloadDecoder(SequenceOrSequenceOfPayloadDecoder):
    protoComponent: univ.SequenceOf

class SetOrSetOfPayloadDecoder(ConstructedPayloadDecoderBase):
    protoRecordComponent: univ.Set
    protoSequenceComponent: univ.SetOf

class SetPayloadDecoder(SetOrSetOfPayloadDecoder):
    protoComponent: univ.Set

class SetOfPayloadDecoder(SetOrSetOfPayloadDecoder):
    protoComponent: univ.SetOf

class ChoicePayloadDecoder(AbstractConstructedPayloadDecoder):
    protoComponent: univ.Choice
    def valueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state=None,
        decodeFun: Callable[..., Incomplete] | None = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ): ...
    def indefLenValueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state=None,
        decodeFun: Callable[..., Incomplete] | None = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ): ...

class AnyPayloadDecoder(AbstractSimplePayloadDecoder):
    protoComponent: univ.Any
    def valueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Unused = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ): ...
    def indefLenValueDecoder(
        self,
        substrate,
        asn1Spec,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Callable[..., Incomplete] | None = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ): ...

class UTF8StringPayloadDecoder(OctetStringPayloadDecoder):
    protoComponent: char.UTF8String

class NumericStringPayloadDecoder(OctetStringPayloadDecoder):
    protoComponent: char.NumericString

class PrintableStringPayloadDecoder(OctetStringPayloadDecoder):
    protoComponent: char.PrintableString

class TeletexStringPayloadDecoder(OctetStringPayloadDecoder):
    protoComponent: char.TeletexString

class VideotexStringPayloadDecoder(OctetStringPayloadDecoder):
    protoComponent: char.VideotexString

class IA5StringPayloadDecoder(OctetStringPayloadDecoder):
    protoComponent: char.IA5String

class GraphicStringPayloadDecoder(OctetStringPayloadDecoder):
    protoComponent: char.GraphicString

class VisibleStringPayloadDecoder(OctetStringPayloadDecoder):
    protoComponent: char.VisibleString

class GeneralStringPayloadDecoder(OctetStringPayloadDecoder):
    protoComponent: char.GeneralString

class UniversalStringPayloadDecoder(OctetStringPayloadDecoder):
    protoComponent: char.UniversalString

class BMPStringPayloadDecoder(OctetStringPayloadDecoder):
    protoComponent: char.BMPString

class ObjectDescriptorPayloadDecoder(OctetStringPayloadDecoder):
    protoComponent: useful.ObjectDescriptor

class GeneralizedTimePayloadDecoder(OctetStringPayloadDecoder):
    protoComponent: useful.GeneralizedTime

class UTCTimePayloadDecoder(OctetStringPayloadDecoder):
    protoComponent: useful.UTCTime

TAG_MAP: dict[TagSet, AbstractPayloadDecoder]
TYPE_MAP: dict[int, AbstractPayloadDecoder]
# deprecated aliases
tagMap = TAG_MAP
typeMap = TYPE_MAP

class SingleItemDecoder:
    defaultErrorState: int
    defaultRawDecoder: AnyPayloadDecoder
    supportIndefLength: bool
    TAG_MAP: dict[TagSet, AbstractPayloadDecoder]
    TYPE_MAP: dict[int, AbstractPayloadDecoder]
    def __init__(self, tagMap=..., typeMap=..., **ignored: Unused) -> None: ...
    def __call__(
        self,
        substrate,
        asn1Spec: Asn1Type | None = None,
        tagSet: TagSet | None = None,
        length: int | None = None,
        state=0,
        decodeFun: Unused = None,
        substrateFun: Callable[..., Incomplete] | None = None,
        **options,
    ): ...

decode: Decoder

class StreamingDecoder:
    """Create an iterator that turns BER/CER/DER byte stream into ASN.1 objects.

    On each iteration, consume whatever BER/CER/DER serialization is
    available in the `substrate` stream-like object and turns it into
    one or more, possibly nested, ASN.1 objects.

    Parameters
    ----------
    substrate: :py:class:`file`, :py:class:`io.BytesIO`
        BER/CER/DER serialization in form of a byte stream

    Keyword Args
    ------------
    asn1Spec: :py:class:`~pyasn1.type.base.PyAsn1Item`
        A pyasn1 type object to act as a template guiding the decoder.
        Depending on the ASN.1 structure being decoded, `asn1Spec` may
        or may not be required. One of the reasons why `asn1Spec` may
        me required is that ASN.1 structure is encoded in the *IMPLICIT*
        tagging mode.

    Yields
    ------
    : :py:class:`~pyasn1.type.base.PyAsn1Item`, :py:class:`~pyasn1.error.SubstrateUnderrunError`
        Decoded ASN.1 object (possibly, nested) or
        :py:class:`~pyasn1.error.SubstrateUnderrunError` object indicating
        insufficient BER/CER/DER serialization on input to fully recover ASN.1
        objects from it.

        In the latter case the caller is advised to ensure some more data in
        the input stream, then call the iterator again. The decoder will resume
        the decoding process using the newly arrived data.

        The `context` property of :py:class:`~pyasn1.error.SubstrateUnderrunError`
        object might hold a reference to the partially populated ASN.1 object
        being reconstructed.

    Raises
    ------
    ~pyasn1.error.PyAsn1Error, ~pyasn1.error.EndOfStreamError
        `PyAsn1Error` on deserialization error, `EndOfStreamError` on
         premature stream closure.

    Examples
    --------
    Decode BER serialisation without ASN.1 schema

    .. code-block:: pycon

        >>> stream = io.BytesIO(
        ...    b'0      \x02\x01\x01\x02\x01\x02\x02\x01\x03')
        >>>
        >>> for asn1Object in StreamingDecoder(stream):
        ...     print(asn1Object)
        >>>
        SequenceOf:
         1 2 3

    Decode BER serialisation with ASN.1 schema

    .. code-block:: pycon

        >>> stream = io.BytesIO(
        ...    b'0      \x02\x01\x01\x02\x01\x02\x02\x01\x03')
        >>>
        >>> schema = SequenceOf(componentType=Integer())
        >>>
        >>> decoder = StreamingDecoder(stream, asn1Spec=schema)
        >>> for asn1Object in decoder:
        ...     print(asn1Object)
        >>>
        SequenceOf:
         1 2 3
    """

    SINGLE_ITEM_DECODER: type[SingleItemDecoder]

    def __init__(self, substrate, asn1Spec=None, *, tagMap=..., typeMap=..., **ignored: Unused) -> None: ...
    def __iter__(self): ...

class Decoder:
    """Create a BER decoder object.

    Parse BER/CER/DER octet-stream into one, possibly nested, ASN.1 object.
    """

    STREAMING_DECODER: type[StreamingDecoder]

    @classmethod
    def __call__(cls, substrate, asn1Spec=None, *, tagMap=..., typeMap=..., **ignored: Unused):
        """Turns BER/CER/DER octet stream into an ASN.1 object.

        Takes BER/CER/DER octet-stream in form of :py:class:`bytes`
        and decode it into an ASN.1 object
        (e.g. :py:class:`~pyasn1.type.base.PyAsn1Item` derivative) which
        may be a scalar or an arbitrary nested structure.

        Parameters
        ----------
        substrate: :py:class:`bytes`
            BER/CER/DER octet-stream to parse

        Keyword Args
        ------------
        asn1Spec: :py:class:`~pyasn1.type.base.PyAsn1Item`
            A pyasn1 type object (:py:class:`~pyasn1.type.base.PyAsn1Item`
            derivative) to act as a template guiding the decoder.
            Depending on the ASN.1 structure being decoded, `asn1Spec` may or
            may not be required. Most common reason for it to require is that
            ASN.1 structure is encoded in *IMPLICIT* tagging mode.

        substrateFun: :py:class:`Union[
                Callable[[pyasn1.type.base.PyAsn1Item, bytes, int],
                         Tuple[pyasn1.type.base.PyAsn1Item, bytes]],
                Callable[[pyasn1.type.base.PyAsn1Item, io.BytesIO, int, dict],
                         Generator[Union[pyasn1.type.base.PyAsn1Item,
                                         pyasn1.error.SubstrateUnderrunError],
                                   None, None]]
            ]`
            User callback meant to generalize special use cases like non-recursive or
            partial decoding. A 3-arg non-streaming variant is supported for backwards
            compatiblilty in addition to the newer 4-arg streaming variant.
            The callback will receive the uninitialized object recovered from substrate
            as 1st argument, the uninterpreted payload as 2nd argument, and the length
            of the uninterpreted payload as 3rd argument. The streaming variant will
            additionally receive the decode(..., **options) kwargs as 4th argument.
            The non-streaming variant shall return an object that will be propagated
            as decode() return value as 1st item, and the remainig payload for further
            decode passes as 2nd item.
            The streaming variant shall yield an object that will be propagated as
            decode() return value, and leave the remaining payload in the stream.

        Returns
        -------
        : :py:class:`tuple`
            A tuple of :py:class:`~pyasn1.type.base.PyAsn1Item` object
            recovered from BER/CER/DER substrate and the unprocessed trailing
            portion of the `substrate` (may be empty)

        Raises
        ------
        : :py:class:`~pyasn1.error.PyAsn1Error`
            :py:class:`~pyasn1.error.SubstrateUnderrunError` on insufficient
            input or :py:class:`~pyasn1.error.PyAsn1Error` on decoding error.

        Examples
        --------
        Decode BER/CER/DER serialisation without ASN.1 schema

        .. code-block:: pycon

           >>> s, unprocessed = decode(b'0      \x02\x01\x01\x02\x01\x02\x02\x01\x03')
           >>> str(s)
           SequenceOf:
            1 2 3

        Decode BER/CER/DER serialisation with ASN.1 schema

        .. code-block:: pycon

           >>> seq = SequenceOf(componentType=Integer())
           >>> s, unprocessed = decode(
                b'0     \x02\x01\x01\x02\x01\x02\x02\x01\x03', asn1Spec=seq)
           >>> str(s)
           SequenceOf:
            1 2 3

        """
