"""Shapely errors."""

from .lib import GEOSException as GEOSException, ShapelyError as ShapelyError

def setup_signal_checks(interval: int = 10000) -> None:
    """Enable Python signal checks in the ufunc inner loops.

    Doing so allows termination (using CTRL+C) of operations on large arrays of
    vectors.

    Parameters
    ----------
    interval : int, default 10000
        Check for interrupts every x iterations. The higher the number, the
        slower shapely will respond to a signal. However, at low values there
        will be a negative effect on performance. The default of 10000 does not
        have any measureable effects on performance.

    Notes
    -----
    For more information on signals consult the Python docs:

    https://docs.python.org/3/library/signal.html

    """

class UnsupportedGEOSVersionError(ShapelyError):
    """Raised when the GEOS library version does not support a certain operation."""

class DimensionError(ShapelyError):
    """An error in the number of coordinate dimensions."""

class TopologicalError(ShapelyError):
    """A geometry is invalid or topologically incorrect."""

class ShapelyDeprecationWarning(FutureWarning):
    """Warning for features that will be removed or changed in a future release."""

class EmptyPartError(ShapelyError):
    """An error signifying an empty part was encountered when creating a multi-part."""

class GeometryTypeError(ShapelyError):
    """An error raised when the geometry has an unrecognized or inappropriate type."""

# deprecated aliases
ReadingError = ShapelyError
WKBReadingError = ShapelyError
WKTReadingError = ShapelyError
PredicateError = ShapelyError
InvalidGeometryError = ShapelyError
