"""
A declarative, object-oriented interface for creating statistical graphics.

The seaborn.objects namespace contains a number of classes that can be composed
together to build a customized visualization.

The main object is :class:`Plot`, which is the starting point for all figures.
Pass :class:`Plot` a dataset and specify assignments from its variables to
roles in the plot. Build up the visualization by calling its methods.

There are four other general types of objects in this interface:

- :class:`Mark` subclasses, which create matplotlib artists for visualization
- :class:`Stat` subclasses, which apply statistical transforms before plotting
- :class:`Move` subclasses, which make further adjustments to reduce overplotting

These classes are passed to :meth:`Plot.add` to define a layer in the plot.
Each layer has a :class:`Mark` and optional :class:`Stat` and/or :class:`Move`.
Plots can have multiple layers.

The other general type of object is a :class:`Scale` subclass, which provide an
interface for controlling the mappings between data values and visual properties.
Pass :class:`Scale` objects to :meth:`Plot.scale`.

See the documentation for other :class:`Plot` methods to learn about the many
ways that a plot can be enhanced and customized.

"""

from seaborn._core.moves import Dodge as Dodge, Jitter as Jitter, Move as Move, Norm as Norm, Shift as Shift, Stack as Stack
from seaborn._core.plot import Plot as Plot
from seaborn._core.scales import (
    Boolean as Boolean,
    Continuous as Continuous,
    Nominal as Nominal,
    Scale as Scale,
    Temporal as Temporal,
)
from seaborn._marks.area import Area as Area, Band as Band
from seaborn._marks.bar import Bar as Bar, Bars as Bars
from seaborn._marks.base import Mark as Mark
from seaborn._marks.dot import Dot as Dot, Dots as Dots
from seaborn._marks.line import Dash as Dash, Line as Line, Lines as Lines, Path as Path, Paths as Paths, Range as Range
from seaborn._marks.text import Text as Text
from seaborn._stats.aggregation import Agg as Agg, Est as Est
from seaborn._stats.base import Stat as Stat
from seaborn._stats.counting import Count as Count, Hist as Hist
from seaborn._stats.density import KDE as KDE
from seaborn._stats.order import Perc as Perc
from seaborn._stats.regression import PolyFit as PolyFit
