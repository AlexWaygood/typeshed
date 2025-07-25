from collections.abc import Container, Mapping

from pyasn1.type.base import Asn1Type

__all__ = ["TagMap"]

class TagMap:
    """Map *TagSet* objects to ASN.1 types

    Create an object mapping *TagSet* object to ASN.1 type.

    *TagMap* objects are immutable and duck-type read-only Python
    :class:`dict` objects holding *TagSet* objects as keys and ASN.1
    type objects as values.

    Parameters
    ----------
    presentTypes: :py:class:`dict`
        Map of :class:`~pyasn1.type.tag.TagSet` to ASN.1 objects considered
        as being unconditionally present in the *TagMap*.

    skipTypes: :py:class:`dict`
        A collection of :class:`~pyasn1.type.tag.TagSet` objects considered
        as absent in the *TagMap* even when *defaultType* is present.

    defaultType: ASN.1 type object
        An ASN.1 type object callee *TagMap* returns for any *TagSet* key not present
        in *presentTypes* (unless given key is present in *skipTypes*).
    """

    def __init__(
        self,
        presentTypes: Mapping[TagMap, Asn1Type] | None = None,
        skipTypes: Container[TagMap] | None = None,
        defaultType: Asn1Type | None = None,
    ) -> None: ...
    def __contains__(self, tagSet) -> bool: ...
    def __getitem__(self, tagSet): ...
    def __iter__(self): ...
    @property
    def presentTypes(self):
        """Return *TagSet* to ASN.1 type map present in callee *TagMap*"""

    @property
    def skipTypes(self):
        """Return *TagSet* collection unconditionally absent in callee *TagMap*"""

    @property
    def defaultType(self):
        """Return default ASN.1 type being returned for any missing *TagSet*"""

    def getPosMap(self): ...
    def getNegMap(self): ...
    def getDef(self): ...
