from dataclasses import dataclass

from seaborn._marks.base import MappableColor, MappableFloat, MappableString, Mark, document_properties

@document_properties
@dataclass
class Path(Mark):
    """
    A mark connecting data points in the order they appear.

        This mark defines the following properties:
            |color|, |alpha|, |linewidth|, |linestyle|, |marker|, |pointsize|,
            |fillcolor|, |edgecolor|, |edgewidth|

    See also
    --------
    Line : A mark connecting data points with sorting along the orientation axis.
    Paths : A faster but less-flexible mark for drawing many paths.

    Examples
    --------
    .. include:: ../docstrings/objects.Path.rst

    """

    color: MappableColor = ...
    alpha: MappableFloat = ...
    linewidth: MappableFloat = ...
    linestyle: MappableString = ...
    marker: MappableString = ...
    pointsize: MappableFloat = ...
    fillcolor: MappableColor = ...
    edgecolor: MappableColor = ...
    edgewidth: MappableFloat = ...

@document_properties
@dataclass
class Line(Path):
    """
    A mark connecting data points with sorting along the orientation axis.

        This mark defines the following properties:
            |color|, |alpha|, |linewidth|, |linestyle|, |marker|, |pointsize|,
            |fillcolor|, |edgecolor|, |edgewidth|

    See also
    --------
    Path : A mark connecting data points in the order they appear.
    Lines : A faster but less-flexible mark for drawing many lines.

    Examples
    --------
    .. include:: ../docstrings/objects.Line.rst

    """

@document_properties
@dataclass
class Paths(Mark):
    """
    A faster but less-flexible mark for drawing many paths.

        This mark defines the following properties:
            |color|, |alpha|, |linewidth|, |linestyle|

    See also
    --------
    Path : A mark connecting data points in the order they appear.

    Examples
    --------
    .. include:: ../docstrings/objects.Paths.rst

    """

    color: MappableColor = ...
    alpha: MappableFloat = ...
    linewidth: MappableFloat = ...
    linestyle: MappableString = ...
    def __post_init__(self) -> None: ...

@document_properties
@dataclass
class Lines(Paths):
    """
    A faster but less-flexible mark for drawing many lines.

        This mark defines the following properties:
            |color|, |alpha|, |linewidth|, |linestyle|

    See also
    --------
    Line : A mark connecting data points with sorting along the orientation axis.

    Examples
    --------
    .. include:: ../docstrings/objects.Lines.rst

    """

@document_properties
@dataclass
class Range(Paths):
    """
    An oriented line mark drawn between min/max values.

        This mark defines the following properties:
            |color|, |alpha|, |linewidth|, |linestyle|

    Examples
    --------
    .. include:: ../docstrings/objects.Range.rst

    """

@document_properties
@dataclass
class Dash(Paths):
    """
    A line mark drawn as an oriented segment for each datapoint.

        This mark defines the following properties:
            |color|, |alpha|, |linewidth|, |linestyle|, |width|

    Examples
    --------
    .. include:: ../docstrings/objects.Dash.rst

    """

    width: MappableFloat = ...
