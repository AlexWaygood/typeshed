"""Testing functionality for geopandas objects."""

from typing import Literal

from .array import GeometryArray
from .base import GeoPandasBase
from .geodataframe import GeoDataFrame
from .geoseries import GeoSeries

def geom_equals(this: GeoPandasBase | GeometryArray, that: GeoPandasBase | GeometryArray) -> bool:
    """
    Test for geometric equality. Empty or missing geometries are considered
    equal.

    Parameters
    ----------
    this, that : arrays of Geo objects (or anything that has an `is_empty`
                 attribute)

    Returns
    -------
    bool
        True if all geometries in left equal geometries in right
    """

def geom_almost_equals(this: GeoPandasBase | GeometryArray, that: GeoPandasBase | GeometryArray) -> bool:
    """
    Test for 'almost' geometric equality. Empty or missing geometries
    considered equal.

    This method allows small difference in the coordinates, but this
    requires coordinates be in the same order for all components of a geometry.

    Parameters
    ----------
    this, that : arrays of Geo objects (or anything that has an `is_empty`
                 property)

    Returns
    -------
    bool
        True if all geometries in left almost equal geometries in right
    """

def assert_geoseries_equal(
    left: GeoSeries,
    right: GeoSeries,
    check_dtype: bool = True,
    check_index_type: bool = False,
    check_series_type: bool = True,
    check_less_precise: bool = False,
    check_geom_type: bool = False,
    check_crs: bool = True,
    normalize: bool = False,
) -> None:
    """
    Test util for checking that two GeoSeries are equal.

    Parameters
    ----------
    left, right : two GeoSeries
    check_dtype : bool, default False
        If True, check geo dtype [only included so it's a drop-in replacement
        for assert_series_equal].
    check_index_type : bool, default False
        Check that index types are equal.
    check_series_type : bool, default True
        Check that both are same type (*and* are GeoSeries). If False,
        will attempt to convert both into GeoSeries.
    check_less_precise : bool, default False
        If True, use geom_equals_exact with relative error of 0.5e-6.
        If False, use geom_equals.
    check_geom_type : bool, default False
        If True, check that all the geom types are equal.
    check_crs: bool, default True
        If `check_series_type` is True, then also check that the
        crs matches.
    normalize: bool, default False
        If True, normalize the geometries before comparing equality.
        Typically useful with ``check_less_precise=True``, which uses
        ``geom_equals_exact`` and requires exact coordinate order.
    """

def assert_geodataframe_equal(
    left: GeoDataFrame,
    right: GeoDataFrame,
    check_dtype: bool = True,
    check_index_type: bool | Literal["equiv"] = "equiv",
    check_column_type: bool | Literal["equiv"] = "equiv",
    check_frame_type: bool = True,
    check_like: bool = False,
    check_less_precise: bool = False,
    check_geom_type: bool = False,
    check_crs: bool = True,
    normalize: bool = False,
) -> None:
    """Check that two GeoDataFrames are equal.

    Parameters
    ----------
    left, right : two GeoDataFrames
    check_dtype : bool, default True
        Whether to check the DataFrame dtype is identical.
    check_index_type, check_column_type : bool, default 'equiv'
        Check that index types are equal.
    check_frame_type : bool, default True
        Check that both are same type (*and* are GeoDataFrames). If False,
        will attempt to convert both into GeoDataFrame.
    check_like : bool, default False
        If true, ignore the order of rows & columns
    check_less_precise : bool, default False
        If True, use geom_equals_exact. if False, use geom_equals.
    check_geom_type : bool, default False
        If True, check that all the geom types are equal.
    check_crs: bool, default True
        If `check_frame_type` is True, then also check that the
        crs matches.
    normalize: bool, default False
        If True, normalize the geometries before comparing equality.
        Typically useful with ``check_less_precise=True``, which uses
        ``geom_equals_exact`` and requires exact coordinate order.
    """
