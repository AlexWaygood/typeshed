from dataclasses import dataclass

from seaborn._marks.base import MappableBool, MappableColor, MappableFloat, MappableStyle, Mark, document_properties

class BarBase(Mark): ...

@document_properties
@dataclass
class Bar(BarBase):
    """
    A bar mark drawn between baseline and data values.

        This mark defines the following properties:
            |color|, |alpha|, |fill|, |edgecolor|, |edgealpha|, |edgewidth|,
            |edgestyle|, |width|, |baseline|

    See also
    --------
    Bars : A faster bar mark with defaults more suitable for histograms.

    Examples
    --------
    .. include:: ../docstrings/objects.Bar.rst

    """

    color: MappableColor = ...
    alpha: MappableFloat = ...
    fill: MappableBool = ...
    edgecolor: MappableColor = ...
    edgealpha: MappableFloat = ...
    edgewidth: MappableFloat = ...
    edgestyle: MappableStyle = ...
    width: MappableFloat = ...
    baseline: MappableFloat = ...

@document_properties
@dataclass
class Bars(BarBase):
    """
    A faster bar mark with defaults more suitable for histograms.

        This mark defines the following properties:
            |color|, |alpha|, |fill|, |edgecolor|, |edgealpha|, |edgewidth|,
            |edgestyle|, |width|, |baseline|

    See also
    --------
    Bar : A bar mark drawn between baseline and data values.

    Examples
    --------
    .. include:: ../docstrings/objects.Bars.rst

    """

    color: MappableColor = ...
    alpha: MappableFloat = ...
    fill: MappableBool = ...
    edgecolor: MappableColor = ...
    edgealpha: MappableFloat = ...
    edgewidth: MappableFloat = ...
    edgestyle: MappableStyle = ...
    width: MappableFloat = ...
    baseline: MappableFloat = ...
