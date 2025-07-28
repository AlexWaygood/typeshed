from dataclasses import dataclass

from seaborn._marks.base import MappableBool, MappableColor, MappableFloat, MappableStyle, Mark, document_properties

class AreaBase: ...

@document_properties
@dataclass
class Area(AreaBase, Mark):
    """
    A fill mark drawn from a baseline to data values.

        This mark defines the following properties:
            |color|, |alpha|, |fill|, |edgecolor|, |edgealpha|, |edgewidth|,
            |edgestyle|, |baseline|

    See also
    --------
    Band : A fill mark representing an interval between values.

    Examples
    --------
    .. include:: ../docstrings/objects.Area.rst

    """

    color: MappableColor = ...
    alpha: MappableFloat = ...
    fill: MappableBool = ...
    edgecolor: MappableColor = ...
    edgealpha: MappableFloat = ...
    edgewidth: MappableFloat = ...
    edgestyle: MappableStyle = ...
    baseline: MappableFloat = ...

@document_properties
@dataclass
class Band(AreaBase, Mark):
    """
    A fill mark representing an interval between values.

        This mark defines the following properties:
            |color|, |alpha|, |fill|, |edgecolor|, |edgealpha|, |edgewidth|,
            |edgestyle|

    See also
    --------
    Area : A fill mark drawn from a baseline to data values.

    Examples
    --------
    .. include:: ../docstrings/objects.Band.rst

    """

    color: MappableColor = ...
    alpha: MappableFloat = ...
    fill: MappableBool = ...
    edgecolor: MappableColor = ...
    edgealpha: MappableFloat = ...
    edgewidth: MappableFloat = ...
    edgestyle: MappableFloat = ...
