from dataclasses import dataclass

from seaborn._marks.base import (
    MappableBool,
    MappableColor,
    MappableFloat,
    MappableString,
    MappableStyle,
    Mark,
    document_properties,
)

class DotBase(Mark): ...

@document_properties
@dataclass
class Dot(DotBase):
    """
    A mark suitable for dot plots or less-dense scatterplots.

        This mark defines the following properties:
            |marker|, |pointsize|, |stroke|, |color|, |alpha|, |fill|,
            |edgecolor|, |edgealpha|, |edgewidth|, |edgestyle|

    See also
    --------
    Dots : A dot mark defined by strokes to better handle overplotting.

    Examples
    --------
    .. include:: ../docstrings/objects.Dot.rst

    """

    marker: MappableString = ...
    pointsize: MappableFloat = ...
    stroke: MappableFloat = ...
    color: MappableColor = ...
    alpha: MappableFloat = ...
    fill: MappableBool = ...
    edgecolor: MappableColor = ...
    edgealpha: MappableFloat = ...
    edgewidth: MappableFloat = ...
    edgestyle: MappableStyle = ...

@document_properties
@dataclass
class Dots(DotBase):
    """
    A dot mark defined by strokes to better handle overplotting.

        This mark defines the following properties:
            |marker|, |pointsize|, |stroke|, |color|, |alpha|, |fill|,
            |fillcolor|, |fillalpha|

    See also
    --------
    Dot : A mark suitable for dot plots or less-dense scatterplots.

    Examples
    --------
    .. include:: ../docstrings/objects.Dots.rst

    """

    marker: MappableString = ...
    pointsize: MappableFloat = ...
    stroke: MappableFloat = ...
    color: MappableColor = ...
    alpha: MappableFloat = ...
    fill: MappableBool = ...
    fillcolor: MappableColor = ...
    fillalpha: MappableFloat = ...
