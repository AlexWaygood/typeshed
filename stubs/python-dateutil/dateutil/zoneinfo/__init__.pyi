from _typeshed import Incomplete
from collections.abc import Callable
from io import BytesIO
from tarfile import _Fileobj
from typing import Final, TypeVar, overload
from typing_extensions import Self, TypeAlias, deprecated

from dateutil.tz import tzfile as _tzfile

_T = TypeVar("_T")
_MetadataType: TypeAlias = dict[str, Incomplete]

__all__ = ["get_zonefile_instance", "gettz", "gettz_db_metadata"]

ZONEFILENAME: Final[str]
METADATA_FN: Final[str]

class tzfile(_tzfile):
    def __reduce__(self) -> tuple[Callable[[str], Self], tuple[str, ...]]: ...

def getzoneinfofile_stream() -> BytesIO | None: ...

class ZoneInfoFile:
    zones: dict[str, _tzfile]
    metadata: _MetadataType | None
    def __init__(self, zonefile_stream: _Fileobj | None = None) -> None: ...
    @overload
    def get(self, name: str, default: None = None) -> _tzfile | None:
        """
        Wrapper for :func:`ZoneInfoFile.zones.get`. This is a convenience method
        for retrieving zones from the zone dictionary.

        :param name:
            The name of the zone to retrieve. (Generally IANA zone names)

        :param default:
            The value to return in the event of a missing key.

        .. versionadded:: 2.6.0

        """

    @overload
    def get(self, name: str, default: _tzfile) -> _tzfile: ...
    @overload
    def get(self, name: str, default: _T) -> _tzfile | _T: ...

def get_zonefile_instance(new_instance: bool = False) -> ZoneInfoFile:
    """
    This is a convenience function which provides a :class:`ZoneInfoFile`
    instance using the data provided by the ``dateutil`` package. By default, it
    caches a single instance of the ZoneInfoFile object and returns that.

    :param new_instance:
        If ``True``, a new instance of :class:`ZoneInfoFile` is instantiated and
        used as the cached instance for the next call. Otherwise, new instances
        are created only as necessary.

    :return:
        Returns a :class:`ZoneInfoFile` object.

    .. versionadded:: 2.6
    """

@deprecated(
    "zoneinfo.gettz() will be removed in future versions, to use the dateutil-provided "
    "zoneinfo files, instantiate a ZoneInfoFile object and use ZoneInfoFile.zones.get() instead."
)
def gettz(name: str) -> _tzfile:
    """
    This retrieves a time zone from the local zoneinfo tarball that is packaged
    with dateutil.

    :param name:
        An IANA-style time zone name, as found in the zoneinfo file.

    :return:
        Returns a :class:`dateutil.tz.tzfile` time zone object.

    .. warning::
        It is generally inadvisable to use this function, and it is only
        provided for API compatibility with earlier versions. This is *not*
        equivalent to ``dateutil.tz.gettz()``, which selects an appropriate
        time zone based on the inputs, favoring system zoneinfo. This is ONLY
        for accessing the dateutil-specific zoneinfo (which may be out of
        date compared to the system zoneinfo).

    .. deprecated:: 2.6
        If you need to use a specific zoneinfofile over the system zoneinfo,
        instantiate a :class:`dateutil.zoneinfo.ZoneInfoFile` object and call
        :func:`dateutil.zoneinfo.ZoneInfoFile.get(name)` instead.

        Use :func:`get_zonefile_instance` to retrieve an instance of the
        dateutil-provided zoneinfo.
    """

@deprecated(
    "zoneinfo.gettz_db_metadata() will be removed in future versions, to use the "
    "dateutil-provided zoneinfo files, ZoneInfoFile object and query the 'metadata' attribute instead."
)
def gettz_db_metadata() -> _MetadataType:
    """Get the zonefile metadata

    See `zonefile_metadata`_

    :returns:
        A dictionary with the database metadata

    .. deprecated:: 2.6
        See deprecation warning in :func:`zoneinfo.gettz`. To get metadata,
        query the attribute ``zoneinfo.ZoneInfoFile.metadata``.
    """
