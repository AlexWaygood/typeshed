from collections.abc import Collection
from typing import Any

import pandas as pd
from shapely import Geometry
from shapely.geometry.base import BaseGeometry

from ..geoseries import GeoSeries

def collect(
    x: Collection[Geometry] | GeoSeries | pd.Series[Any] | Geometry, multi: bool = False  # Cannot use pd.Series[BaseGeometry]
) -> BaseGeometry:
    """Collect single part geometries into their Multi* counterpart.

    Parameters
    ----------
    x : an iterable or Series of Shapely geometries, a GeoSeries, or
        a single Shapely geometry
    multi : boolean, default False
        if True, force returned geometries to be Multi* even if they
        only have one component.

    """
