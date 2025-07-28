from collections.abc import Iterator
from typing import Any

from matplotlib.axes import Axes
from matplotlib.figure import Figure, SubFigure
from seaborn._core.plot import FacetSpec, PairSpec

class Subplots:
    """
    Interface for creating and using matplotlib subplots based on seaborn parameters.

    Parameters
    ----------
    subplot_spec : dict
        Keyword args for :meth:`matplotlib.figure.Figure.subplots`.
    facet_spec : dict
        Parameters that control subplot faceting.
    pair_spec : dict
        Parameters that control subplot pairing.
    data : PlotData
        Data used to define figure setup.

    """

    subplot_spec: dict[str, Any]
    def __init__(self, subplot_spec: dict[str, Any], facet_spec: FacetSpec, pair_spec: PairSpec) -> None: ...
    def init_figure(
        self,
        pair_spec: PairSpec,
        pyplot: bool = False,
        figure_kws: dict[str, Any] | None = None,
        target: Axes | Figure | SubFigure | None = None,
    ) -> Figure:
        """Initialize matplotlib objects and add seaborn-relevant metadata."""

    def __iter__(self) -> Iterator[dict[str, Any]]:
        """Yield each subplot dictionary with Axes object and metadata."""

    def __len__(self) -> int:
        """Return the number of subplots in this figure."""
