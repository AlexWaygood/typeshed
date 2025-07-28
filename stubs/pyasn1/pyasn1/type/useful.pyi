import datetime

from pyasn1.type import char
from pyasn1.type.tag import TagSet

__all__ = ["ObjectDescriptor", "GeneralizedTime", "UTCTime"]

class ObjectDescriptor(char.GraphicString):
    """Creates |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.SimpleAsn1Type`,
    its objects are immutable and duck-type :class:`bytes`.
    When used in octet-stream context, |ASN.1| type assumes
    "|encoding|" encoding.

    Keyword Args
    ------------
    value: :class:`str`, :class:`bytes` or |ASN.1| object
        :class:`str`, alternatively :class:`bytes`
        representing octet-stream of serialised unicode string
        (note `encoding` parameter) or |ASN.1| class instance.
        If `value` is not given, schema object will be created.

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s). Constraints
        verification for |ASN.1| type occurs automatically on object
        instantiation.

    encoding: :py:class:`str`
        Unicode codec ID to encode/decode
        :class:`str` the payload when |ASN.1| object is used
        in octet-stream context.

    Raises
    ------
    ~pyasn1.error.ValueConstraintError, ~pyasn1.error.PyAsn1Error
        On constraint violation or bad initializer.
    """

    tagSet: TagSet
    typeId: int

class TimeMixIn:
    class FixedOffset(datetime.tzinfo):
        """Fixed offset in minutes east from UTC."""

        def __init__(self, offset: int = 0, name: str = "UTC") -> None: ...
        def utcoffset(self, dt): ...
        def tzname(self, dt): ...
        def dst(self, dt): ...

    UTC: FixedOffset
    @property
    def asDateTime(self):
        """Create :py:class:`datetime.datetime` object from a |ASN.1| object.

        Returns
        -------
        :
            new instance of :py:class:`datetime.datetime` object
        """

    @classmethod
    def fromDateTime(cls, dt):
        """Create |ASN.1| object from a :py:class:`datetime.datetime` object.

        Parameters
        ----------
        dt: :py:class:`datetime.datetime` object
            The `datetime.datetime` object to initialize the |ASN.1| object
            from

        Returns
        -------
        :
            new instance of |ASN.1| value
        """

class GeneralizedTime(char.VisibleString, TimeMixIn):
    """Creates |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.SimpleAsn1Type`,
    its objects are immutable and duck-type :class:`bytes`.
    When used in octet-stream context, |ASN.1| type assumes
    "|encoding|" encoding.

    Keyword Args
    ------------
    value: :class:`str`, :class:`bytes` or |ASN.1| object
        :class:`str`, alternatively :class:`bytes`
        representing octet-stream of serialised unicode string
        (note `encoding` parameter) or |ASN.1| class instance.
        If `value` is not given, schema object will be created.

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s). Constraints
        verification for |ASN.1| type occurs automatically on object
        instantiation.

    encoding: :py:class:`str`
        Unicode codec ID to encode/decode
        :class:`str` the payload when |ASN.1| object is used
        in octet-stream context.

    Raises
    ------
    ~pyasn1.error.ValueConstraintError, ~pyasn1.error.PyAsn1Error
        On constraint violation or bad initializer.
    """

    tagSet: TagSet
    typeId: int

class UTCTime(char.VisibleString, TimeMixIn):
    """Creates |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.SimpleAsn1Type`,
    its objects are immutable and duck-type :class:`bytes`.
    When used in octet-stream context, |ASN.1| type assumes
    "|encoding|" encoding.

    Keyword Args
    ------------
    value: :class:`str`, :class:`bytes` or |ASN.1| object
        :class:`str`, alternatively :class:`bytes`
        representing octet-stream of serialised unicode string
        (note `encoding` parameter) or |ASN.1| class instance.
        If `value` is not given, schema object will be created.

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s). Constraints
        verification for |ASN.1| type occurs automatically on object
        instantiation.

    encoding: :py:class:`str`
        Unicode codec ID to encode/decode
        :class:`str` the payload when |ASN.1| object is used
        in octet-stream context.

    Raises
    ------
    ~pyasn1.error.ValueConstraintError, ~pyasn1.error.PyAsn1Error
        On constraint violation or bad initializer.
    """

    tagSet: TagSet
    typeId: int
