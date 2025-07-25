from collections.abc import Callable, Iterable
from typing import Protocol, type_check_only

from ..base import _ConvertibleToGeoSeries
from ..geodataframe import GeoDataFrame

@type_check_only
class _GeoCoder(Protocol):
    # Represents a geopy.geocoders.base.GeoCoder subclass without actually depending on geopy
    def geocode(self, query: str, /): ...
    def reverse(self, coords, /, exactly_one: bool = ...): ...

# TODO: Use something like `provider: Callable[P, _GeoCoder], **kwargs: P.kwargs` in the functions
# below if this ever becomes a thing
def geocode(strings: Iterable[str], provider: str | Callable[..., _GeoCoder] | None = None, **kwargs) -> GeoDataFrame:
    """
    Geocode a set of strings and get a GeoDataFrame of the resulting points.

    Parameters
    ----------
    strings : list or Series of addresses to geocode
    provider : str or geopy.geocoder
        Specifies geocoding service to use. If none is provided,
        will use 'photon' (see the Photon's terms of service at:
        https://photon.komoot.io).

        Either the string name used by geopy (as specified in
        geopy.geocoders.SERVICE_TO_GEOCODER) or a geopy Geocoder instance
        (e.g., geopy.geocoders.Photon) may be used.

        Some providers require additional arguments such as access keys
        See each geocoder's specific parameters in geopy.geocoders

    Notes
    -----
    Ensure proper use of the results by consulting the Terms of Service for
    your provider.

    Geocoding requires geopy. Install it using 'pip install geopy'. See also
    https://github.com/geopy/geopy

    Examples
    --------
    >>> df = geopandas.tools.geocode(  # doctest: +SKIP
    ...         ["boston, ma", "1600 pennsylvania ave. washington, dc"]
    ...     )
    >>> df  # doctest: +SKIP
                        geometry                                            address
    0  POINT (-71.05863 42.35899)                          Boston, MA, United States
    1  POINT (-77.03651 38.89766)  1600 Pennsylvania Ave NW, Washington, DC 20006...
    """

def reverse_geocode(
    points: _ConvertibleToGeoSeries, provider: str | Callable[..., _GeoCoder] | None = None, **kwargs
) -> GeoDataFrame:
    """
    Reverse geocode a set of points and get a GeoDataFrame of the resulting
    addresses.

    The points

    Parameters
    ----------
    points : list or Series of Shapely Point objects.
        x coordinate is longitude
        y coordinate is latitude
    provider : str or geopy.geocoder (opt)
        Specifies geocoding service to use. If none is provided,
        will use 'photon' (see the Photon's terms of service at:
        https://photon.komoot.io).

        Either the string name used by geopy (as specified in
        geopy.geocoders.SERVICE_TO_GEOCODER) or a geopy Geocoder instance
        (e.g., geopy.geocoders.Photon) may be used.

        Some providers require additional arguments such as access keys
        See each geocoder's specific parameters in geopy.geocoders

    Notes
    -----
    Ensure proper use of the results by consulting the Terms of Service for
    your provider.

    Reverse geocoding requires geopy. Install it using 'pip install geopy'.
    See also https://github.com/geopy/geopy

    Examples
    --------
    >>> from shapely.geometry import Point
    >>> df = geopandas.tools.reverse_geocode(  # doctest: +SKIP
    ...     [Point(-71.0594869, 42.3584697), Point(-77.0365305, 38.8977332)]
    ... )
    >>> df  # doctest: +SKIP
                         geometry                                            address
    0  POINT (-71.05941 42.35837)       29 Court Sq, Boston, MA 02108, United States
    1  POINT (-77.03641 38.89766)  1600 Pennsylvania Ave NW, Washington, DC 20006...
    """
