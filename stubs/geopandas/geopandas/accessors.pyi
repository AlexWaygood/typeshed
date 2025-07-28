"""Accessors for accessing GeoPandas functionality via pandas extension dtypes."""

from typing import Any

import pandas as pd

class GeoSeriesAccessor:
    """Series.geo accessor to expose GeoSeries methods on pandas Series.

    Parameters
    ----------
    series : pandas.Series
        A Series with geometry dtype.
    """

    def __init__(self, series: pd.Series[Any]) -> None: ...  # Cannot use pd.Series[BaseGeometry]
    def __getattr__(self, name: str) -> Any: ...  # Delegate all attributes to the GeoSeries
