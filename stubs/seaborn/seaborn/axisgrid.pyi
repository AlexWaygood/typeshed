import os
from _typeshed import Incomplete
from collections.abc import Callable, Generator, Iterable, Mapping
from typing import IO, Any, Literal, TypeVar
from typing_extensions import Concatenate, ParamSpec, Self, TypeAlias, deprecated

import numpy as np
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent, RendererBase
from matplotlib.colors import Colormap
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.gridspec import SubplotSpec
from matplotlib.legend import Legend
from matplotlib.patches import Patch
from matplotlib.path import Path as mpl_Path
from matplotlib.patheffects import AbstractPathEffect
from matplotlib.scale import ScaleBase
from matplotlib.text import Text
from matplotlib.transforms import Bbox, BboxBase, Transform, TransformedPath
from matplotlib.typing import ColorType, LineStyleType, MarkerType
from numpy.typing import ArrayLike, NDArray
from pandas import DataFrame, Series

from ._core.typing import ColumnName, DataSource, NormSpec, SupportsDataFrame
from .palettes import _RGBColorPalette
from .utils import _DataSourceWideForm, _Palette, _Vector

__all__ = ["FacetGrid", "PairGrid", "JointGrid", "pairplot", "jointplot"]

_P = ParamSpec("_P")
_R = TypeVar("_R")

_LiteralFont: TypeAlias = Literal["xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"]

class _BaseGrid:
    """Base class for grids of subplots."""

    def set(
        self,
        *,
        # Keywords follow `matplotlib.axes.Axes.set`. Each keyword <KW> corresponds to a `set_<KW>` method
        adjustable: Literal["box", "datalim"] = ...,
        agg_filter: Callable[[ArrayLike, float], tuple[NDArray[np.floating[Any]], float, float]] | None = ...,
        alpha: float | None = ...,
        anchor: str | tuple[float, float] = ...,
        animated: bool = ...,
        aspect: float | Literal["auto", "equal"] = ...,
        autoscale_on: bool = ...,
        autoscalex_on: bool = ...,
        autoscaley_on: bool = ...,
        axes_locator: Callable[[Axes, RendererBase], Bbox] = ...,
        axisbelow: bool | Literal["line"] = ...,
        box_aspect: float | None = ...,
        clip_box: BboxBase | None = ...,
        clip_on: bool = ...,
        clip_path: Patch | mpl_Path | TransformedPath | None = ...,
        facecolor: ColorType | None = ...,
        frame_on: bool = ...,
        gid: str | None = ...,
        in_layout: bool = ...,
        label: object = ...,
        mouseover: bool = ...,
        navigate: bool = ...,
        path_effects: list[AbstractPathEffect] = ...,
        picker: bool | float | Callable[[Artist, MouseEvent], tuple[bool, dict[Any, Any]]] | None = ...,
        position: Bbox | tuple[float, float, float, float] = ...,
        prop_cycle=...,  # TODO: use cycler.Cycler when cycler gets typed
        rasterization_zorder: float | None = ...,
        rasterized: bool = ...,
        sketch_params: float | None = ...,
        snap: bool | None = ...,
        subplotspec: SubplotSpec = ...,
        title: str = ...,
        transform: Transform | None = ...,
        url: str | None = ...,
        visible: bool = ...,
        xbound: float | None | tuple[float | None, float | None] = ...,
        xlabel: str = ...,
        xlim: float | None | tuple[float | None, float | None] = ...,
        xmargin: float = ...,
        xscale: str | ScaleBase = ...,
        xticklabels: Iterable[str | Text] = ...,
        xticks: ArrayLike = ...,
        ybound: float | None | tuple[float | None, float | None] = ...,
        ylabel: str = ...,
        ylim: float | None | tuple[float | None, float | None] = ...,
        ymargin: float = ...,
        yscale: str | ScaleBase = ...,
        yticklabels: Iterable[str | Text] = ...,
        yticks: ArrayLike = ...,
        zorder: float = ...,
        **kwargs: Any,
    ) -> Self:
        """Set attributes on each subplot Axes."""

    @property
    @deprecated("Attribute `fig` is deprecated in favor of `figure`")
    def fig(self) -> Figure:
        """DEPRECATED: prefer the `figure` property."""

    @property
    def figure(self) -> Figure:
        """Access the :class:`matplotlib.figure.Figure` object underlying the grid."""

    def apply(self, func: Callable[Concatenate[Self, _P], object], *args: _P.args, **kwargs: _P.kwargs) -> Self:
        """
        Pass the grid to a user-supplied function and return self.

        The `func` must accept an object of this type for its first
        positional argument. Additional arguments are passed through.
        The return value of `func` is ignored; this method returns self.
        See the `pipe` method if you want the return value.

        Added in v0.12.0.

        """

    def pipe(self, func: Callable[Concatenate[Self, _P], _R], *args: _P.args, **kwargs: _P.kwargs) -> _R:
        """
        Pass the grid to a user-supplied function and return its value.

        The `func` must accept an object of this type for its first
        positional argument. Additional arguments are passed through.
        The return value of `func` becomes the return value of this method.
        See the `apply` method if you want to return self instead.

        Added in v0.12.0.

        """

    def savefig(
        self,
        # Signature follows `matplotlib.figure.Figure.savefig`
        fname: str | os.PathLike[Any] | IO[Any],
        *,
        transparent: bool | None = None,
        dpi: float | Literal["figure"] | None = 96,
        facecolor: ColorType | Literal["auto"] | None = "auto",
        edgecolor: ColorType | Literal["auto"] | None = "auto",
        orientation: Literal["landscape", "portrait"] = "portrait",
        format: str | None = None,
        bbox_inches: Literal["tight"] | Bbox | None = "tight",
        pad_inches: float | Literal["layout"] | None = None,
        backend: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Save an image of the plot.

        This wraps :meth:`matplotlib.figure.Figure.savefig`, using bbox_inches="tight"
        by default. Parameters are passed through to the matplotlib function.

        """

class Grid(_BaseGrid):
    """A grid that can have multiple subplots and an external legend."""

    def __init__(self) -> None: ...
    def tight_layout(
        self,
        *,
        # Keywords follow `matplotlib.figure.Figure.tight_layout`
        pad: float = 1.08,
        h_pad: float | None = None,
        w_pad: float | None = None,
        rect: tuple[float, float, float, float] | None = None,
    ) -> Self:
        """Call fig.tight_layout within rect that exclude the legend."""

    def add_legend(
        self,
        # Cannot use precise key type with union for legend_data because of invariant Mapping keys
        legend_data: Mapping[Any, Artist] | None = None,
        title: str | None = None,
        label_order: list[str] | None = None,
        adjust_subtitles: bool = False,
        *,
        # Keywords follow `matplotlib.legend.Legend`
        loc: str | int | tuple[float, float] | None = None,
        numpoints: int | None = None,
        markerscale: float | None = None,
        markerfirst: bool = True,
        reverse: bool = False,
        scatterpoints: int | None = None,
        scatteryoffsets: Iterable[float] | None = None,
        prop: FontProperties | dict[str, Any] | None = None,
        fontsize: int | _LiteralFont | None = None,
        labelcolor: str | Iterable[str] | None = None,
        borderpad: float | None = None,
        labelspacing: float | None = None,
        handlelength: float | None = None,
        handleheight: float | None = None,
        handletextpad: float | None = None,
        borderaxespad: float | None = None,
        columnspacing: float | None = None,
        ncols: int = 1,
        mode: Literal["expand"] | None = None,
        fancybox: bool | None = None,
        shadow: bool | dict[str, int] | dict[str, float] | None = None,
        title_fontsize: int | _LiteralFont | None = None,
        framealpha: float | None = None,
        edgecolor: ColorType | None = None,
        facecolor: ColorType | None = None,
        bbox_to_anchor: BboxBase | tuple[float, float] | tuple[float, float, float, float] | None = None,
        bbox_transform: Transform | None = None,
        frameon: bool | None = None,
        handler_map: None = None,
        title_fontproperties: FontProperties | None = None,
        alignment: Literal["center", "left", "right"] = "center",
        ncol: int = 1,
        draggable: bool = False,
    ) -> Self:
        """Draw a legend, maybe placing it outside axes and resizing the figure.

        Parameters
        ----------
        legend_data : dict
            Dictionary mapping label names (or two-element tuples where the
            second element is a label name) to matplotlib artist handles. The
            default reads from ``self._legend_data``.
        title : string
            Title for the legend. The default reads from ``self._hue_var``.
        label_order : list of labels
            The order that the legend entries should appear in. The default
            reads from ``self.hue_names``.
        adjust_subtitles : bool
            If True, modify entries with invisible artists to left-align
            the labels and set the font size to that of a title.
        kwargs : key, value pairings
            Other keyword arguments are passed to the underlying legend methods
            on the Figure or Axes object.

        Returns
        -------
        self : Grid instance
            Returns self for easy chaining.

        """

    @property
    def legend(self) -> Legend | None:
        """The :class:`matplotlib.legend.Legend` object, if present."""

    def tick_params(
        self,
        axis: Literal["x", "y", "both"] = "both",
        *,
        # Keywords follow `matplotlib.axes.Axes.tick_params`
        which: Literal["major", "minor", "both"] = "major",
        reset: bool = False,
        direction: Literal["in", "out", "inout"] = ...,
        length: float = ...,
        width: float = ...,
        color: ColorType = ...,
        pad: float = ...,
        labelsize: float | str = ...,
        labelcolor: ColorType = ...,
        labelfontfamily: str = ...,
        colors: ColorType = ...,
        zorder: float = ...,
        bottom: bool = ...,
        top: bool = ...,
        left: bool = ...,
        right: bool = ...,
        labelbottom: bool = ...,
        labeltop: bool = ...,
        labelleft: bool = ...,
        labelright: bool = ...,
        labelrotation: float = ...,
        grid_color: ColorType = ...,
        grid_alpha: float = ...,
        grid_linewidth: float = ...,
        grid_linestyle: str = ...,
        **kwargs: Any,
    ) -> Self:
        """Modify the ticks, tick labels, and gridlines.

        Parameters
        ----------
        axis : {'x', 'y', 'both'}
            The axis on which to apply the formatting.
        kwargs : keyword arguments
            Additional keyword arguments to pass to
            :meth:`matplotlib.axes.Axes.tick_params`.

        Returns
        -------
        self : Grid instance
            Returns self for easy chaining.

        """

class FacetGrid(Grid):
    """Multi-plot grid for plotting conditional relationships."""

    data: DataFrame
    row_names: list[Any]
    col_names: list[Any]
    hue_names: list[Any] | None
    hue_kws: dict[str, Any]
    def __init__(
        self,
        data: DataFrame | SupportsDataFrame,
        *,
        row: str | None = None,
        col: str | None = None,
        hue: str | None = None,
        col_wrap: int | None = None,
        sharex: bool | Literal["col", "row"] = True,
        sharey: bool | Literal["col", "row"] = True,
        height: float = 3,
        aspect: float = 1,
        palette: _Palette | None = None,
        row_order: Iterable[Any] | None = None,
        col_order: Iterable[Any] | None = None,
        hue_order: Iterable[Any] | None = None,
        hue_kws: dict[str, Any] | None = None,
        dropna: bool = False,
        legend_out: bool = True,
        despine: bool = True,
        margin_titles: bool = False,
        xlim: tuple[float, float] | None = None,
        ylim: tuple[float, float] | None = None,
        subplot_kws: dict[str, Any] | None = None,
        gridspec_kws: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the matplotlib figure and FacetGrid object.

        This class maps a dataset onto multiple axes arrayed in a grid of rows
        and columns that correspond to *levels* of variables in the dataset.
        The plots it produces are often called "lattice", "trellis", or
        "small-multiple" graphics.

        It can also represent levels of a third variable with the ``hue``
        parameter, which plots different subsets of data in different colors.
        This uses color to resolve elements on a third dimension, but only
        draws subsets on top of each other and will not tailor the ``hue``
        parameter for the specific visualization the way that axes-level
        functions that accept ``hue`` will.

        The basic workflow is to initialize the :class:`FacetGrid` object with
        the dataset and the variables that are used to structure the grid. Then
        one or more plotting functions can be applied to each subset by calling
        :meth:`FacetGrid.map` or :meth:`FacetGrid.map_dataframe`. Finally, the
        plot can be tweaked with other methods to do things like change the
        axis labels, use different ticks, or add a legend. See the detailed
        code examples below for more information.

        .. warning::

            When using seaborn functions that infer semantic mappings from a
            dataset, care must be taken to synchronize those mappings across
            facets (e.g., by defining the ``hue`` mapping with a palette dict or
            setting the data type of the variables to ``category``). In most cases,
            it will be better to use a figure-level function (e.g. :func:`relplot`
            or :func:`catplot`) than to use :class:`FacetGrid` directly.

        See the :ref:`tutorial <grid_tutorial>` for more information.

        Parameters
        ----------
        data : DataFrame
            Tidy ("long-form") dataframe where each column is a variable and each
            row is an observation.
        row, col, hue : strings
            Variables that define subsets of the data, which will be drawn on
            separate facets in the grid. See the ``{var}_order`` parameters to
            control the order of levels of this variable.
        col_wrap : int
            "Wrap" the column variable at this width, so that the column facets
            span multiple rows. Incompatible with a ``row`` facet.
        share{x,y} : bool, 'col', or 'row' optional
            If true, the facets will share y axes across columns and/or x axes
            across rows.
        height : scalar
            Height (in inches) of each facet. See also: ``aspect``.
        aspect : scalar
            Aspect ratio of each facet, so that ``aspect * height`` gives the width
            of each facet in inches.
        palette : palette name, list, or dict
            Colors to use for the different levels of the ``hue`` variable. Should
            be something that can be interpreted by :func:`color_palette`, or a
            dictionary mapping hue levels to matplotlib colors.
        {row,col,hue}_order : lists
            Order for the levels of the faceting variables. By default, this
            will be the order that the levels appear in ``data`` or, if the
            variables are pandas categoricals, the category order.
        hue_kws : dictionary of param -> list of values mapping
            Other keyword arguments to insert into the plotting call to let
            other plot attributes vary across levels of the hue variable (e.g.
            the markers in a scatterplot).
        legend_out : bool
            If ``True``, the figure size will be extended, and the legend will be
            drawn outside the plot on the center right.
        despine : boolean
            Remove the top and right spines from the plots.
        margin_titles : bool
            If ``True``, the titles for the row variable are drawn to the right of
            the last column. This option is experimental and may not work in all
            cases.
        {x, y}lim: tuples
            Limits for each of the axes on each facet (only relevant when
            share{x, y} is True).
        subplot_kws : dict
            Dictionary of keyword arguments passed to matplotlib subplot(s)
            methods.
        gridspec_kws : dict
            Dictionary of keyword arguments passed to
            :class:`matplotlib.gridspec.GridSpec`
            (via :meth:`matplotlib.figure.Figure.subplots`).
            Ignored if ``col_wrap`` is not ``None``.

        See Also
        --------
        PairGrid : Subplot grid for plotting pairwise relationships
        relplot : Combine a relational plot and a :class:`FacetGrid`
        displot : Combine a distribution plot and a :class:`FacetGrid`
        catplot : Combine a categorical plot and a :class:`FacetGrid`
        lmplot : Combine a regression plot and a :class:`FacetGrid`

        Examples
        --------

        .. note::

            These examples use seaborn functions to demonstrate some of the
            advanced features of the class, but in most cases you will want
            to use figue-level functions (e.g. :func:`displot`, :func:`relplot`)
            to make the plots shown here.

        .. include:: ../docstrings/FacetGrid.rst

        """

    def facet_data(self) -> Generator[tuple[tuple[int, int, int], DataFrame], None, None]:
        """Generator for name indices and data subsets for each facet.

        Yields
        ------
        (i, j, k), data_ijk : tuple of ints, DataFrame
            The ints provide an index into the {row, col, hue}_names attribute,
            and the dataframe contains a subset of the full data corresponding
            to each facet. The generator yields subsets that correspond with
            the self.axes.flat iterator, or self.axes[i, j] when `col_wrap`
            is None.

        """

    def map(self, func: Callable[..., object], *args: str, **kwargs: Any) -> Self:
        """Apply a plotting function to each facet's subset of the data.

        Parameters
        ----------
        func : callable
            A plotting function that takes data and keyword arguments. It
            must plot to the currently active matplotlib Axes and take a
            `color` keyword argument. If faceting on the `hue` dimension,
            it must also take a `label` keyword argument.
        args : strings
            Column names in self.data that identify variables with data to
            plot. The data for each variable is passed to `func` in the
            order the variables are specified in the call.
        kwargs : keyword arguments
            All keyword arguments are passed to the plotting function.

        Returns
        -------
        self : object
            Returns self.

        """

    def map_dataframe(self, func: Callable[..., object], *args: str, **kwargs: Any) -> Self:
        """Like ``.map`` but passes args as strings and inserts data in kwargs.

        This method is suitable for plotting with functions that accept a
        long-form DataFrame as a `data` keyword argument and access the
        data in that DataFrame using string variable names.

        Parameters
        ----------
        func : callable
            A plotting function that takes data and keyword arguments. Unlike
            the `map` method, a function used here must "understand" Pandas
            objects. It also must plot to the currently active matplotlib Axes
            and take a `color` keyword argument. If faceting on the `hue`
            dimension, it must also take a `label` keyword argument.
        args : strings
            Column names in self.data that identify variables with data to
            plot. The data for each variable is passed to `func` in the
            order the variables are specified in the call.
        kwargs : keyword arguments
            All keyword arguments are passed to the plotting function.

        Returns
        -------
        self : object
            Returns self.

        """

    def facet_axis(self, row_i: int, col_j: int, modify_state: bool = True) -> Axes:
        """Make the axis identified by these indices active and return it."""
    # `despine` should be kept roughly in line with `seaborn.utils.despine`
    def despine(
        self,
        *,
        ax: Axes | None = None,
        top: bool = True,
        right: bool = True,
        left: bool = False,
        bottom: bool = False,
        offset: int | Mapping[str, int] | None = None,
        trim: bool = False,
    ) -> Self:
        """Remove axis spines from the facets."""

    def set_axis_labels(
        self, x_var: str | None = None, y_var: str | None = None, clear_inner: bool = True, **kwargs: Any
    ) -> Self:
        """Set axis labels on the left column and bottom row of the grid."""

    def set_xlabels(self, label: str | None = None, clear_inner: bool = True, **kwargs: Any) -> Self:
        """Label the x axis on the bottom row of the grid."""

    def set_ylabels(self, label: str | None = None, clear_inner: bool = True, **kwargs: Any) -> Self:
        """Label the y axis on the left column of the grid."""

    def set_xticklabels(self, labels: Iterable[str | Text] | None = None, step: int | None = None, **kwargs: Any) -> Self:
        """Set x axis tick labels of the grid."""

    def set_yticklabels(self, labels: Iterable[str | Text] | None = None, **kwargs: Any) -> Self:
        """Set y axis tick labels on the left column of the grid."""

    def set_titles(
        self, template: str | None = None, row_template: str | None = None, col_template: str | None = None, **kwargs: Any
    ) -> Self:
        """Draw titles either above each facet or on the grid margins.

        Parameters
        ----------
        template : string
            Template for all titles with the formatting keys {col_var} and
            {col_name} (if using a `col` faceting variable) and/or {row_var}
            and {row_name} (if using a `row` faceting variable).
        row_template:
            Template for the row variable when titles are drawn on the grid
            margins. Must have {row_var} and {row_name} formatting keys.
        col_template:
            Template for the column variable when titles are drawn on the grid
            margins. Must have {col_var} and {col_name} formatting keys.

        Returns
        -------
        self: object
            Returns self.

        """

    def refline(
        self,
        *,
        x: float | None = None,
        y: float | None = None,
        color: ColorType = ".5",
        linestyle: LineStyleType = "--",
        **line_kws: Any,
    ) -> Self:
        """Add a reference line(s) to each facet.

        Parameters
        ----------
        x, y : numeric
            Value(s) to draw the line(s) at.
        color : :mod:`matplotlib color <matplotlib.colors>`
            Specifies the color of the reference line(s). Pass ``color=None`` to
            use ``hue`` mapping.
        linestyle : str
            Specifies the style of the reference line(s).
        line_kws : key, value mappings
            Other keyword arguments are passed to :meth:`matplotlib.axes.Axes.axvline`
            when ``x`` is not None and :meth:`matplotlib.axes.Axes.axhline` when ``y``
            is not None.

        Returns
        -------
        :class:`FacetGrid` instance
            Returns ``self`` for easy method chaining.

        """

    @property
    def axes(self) -> NDArray[Incomplete]:  # array of `Axes`
        """An array of the :class:`matplotlib.axes.Axes` objects in the grid."""

    @property
    def ax(self) -> Axes:
        """The :class:`matplotlib.axes.Axes` when no faceting variables are assigned."""

    @property
    def axes_dict(self) -> dict[Any, Axes]:
        """A mapping of facet names to corresponding :class:`matplotlib.axes.Axes`.

        If only one of ``row`` or ``col`` is assigned, each key is a string
        representing a level of that variable. If both facet dimensions are
        assigned, each key is a ``({row_level}, {col_level})`` tuple.

        """

class PairGrid(Grid):
    """Subplot grid for plotting pairwise relationships in a dataset.

    This object maps each variable in a dataset onto a column and row in a
    grid of multiple axes. Different axes-level plotting functions can be
    used to draw bivariate plots in the upper and lower triangles, and the
    marginal distribution of each variable can be shown on the diagonal.

    Several different common plots can be generated in a single line using
    :func:`pairplot`. Use :class:`PairGrid` when you need more flexibility.

    See the :ref:`tutorial <grid_tutorial>` for more information.

    """

    x_vars: list[str]
    y_vars: list[str]
    square_grid: bool
    axes: NDArray[Incomplete]  # two-dimensional array of `Axes`
    data: DataFrame
    diag_sharey: bool
    diag_vars: list[str] | None
    diag_axes: list[Axes] | None
    hue_names: list[str]
    hue_vals: Series[Any]
    hue_kws: dict[str, Any]
    palette: _RGBColorPalette
    def __init__(
        self,
        data: DataFrame | SupportsDataFrame,
        *,
        hue: str | None = None,
        vars: Iterable[str] | None = None,
        x_vars: Iterable[str] | str | None = None,
        y_vars: Iterable[str] | str | None = None,
        hue_order: Iterable[str] | None = None,
        palette: _Palette | None = None,
        hue_kws: dict[str, Any] | None = None,
        corner: bool = False,
        diag_sharey: bool = True,
        height: float = 2.5,
        aspect: float = 1,
        layout_pad: float = 0.5,
        despine: bool = True,
        dropna: bool = False,
    ) -> None:
        """Initialize the plot figure and PairGrid object.

        Parameters
        ----------
        data : DataFrame
            Tidy (long-form) dataframe where each column is a variable and
            each row is an observation.
        hue : string (variable name)
            Variable in ``data`` to map plot aspects to different colors. This
            variable will be excluded from the default x and y variables.
        vars : list of variable names
            Variables within ``data`` to use, otherwise use every column with
            a numeric datatype.
        {x, y}_vars : lists of variable names
            Variables within ``data`` to use separately for the rows and
            columns of the figure; i.e. to make a non-square plot.
        hue_order : list of strings
            Order for the levels of the hue variable in the palette
        palette : dict or seaborn color palette
            Set of colors for mapping the ``hue`` variable. If a dict, keys
            should be values  in the ``hue`` variable.
        hue_kws : dictionary of param -> list of values mapping
            Other keyword arguments to insert into the plotting call to let
            other plot attributes vary across levels of the hue variable (e.g.
            the markers in a scatterplot).
        corner : bool
            If True, don't add axes to the upper (off-diagonal) triangle of the
            grid, making this a "corner" plot.
        height : scalar
            Height (in inches) of each facet.
        aspect : scalar
            Aspect * height gives the width (in inches) of each facet.
        layout_pad : scalar
            Padding between axes; passed to ``fig.tight_layout``.
        despine : boolean
            Remove the top and right spines from the plots.
        dropna : boolean
            Drop missing values from the data before plotting.

        See Also
        --------
        pairplot : Easily drawing common uses of :class:`PairGrid`.
        FacetGrid : Subplot grid for plotting conditional relationships.

        Examples
        --------

        .. include:: ../docstrings/PairGrid.rst

        """

    def map(self, func: Callable[..., object], **kwargs: Any) -> Self:
        """Plot with the same function in every subplot.

        Parameters
        ----------
        func : callable plotting function
            Must take x, y arrays as positional arguments and draw onto the
            "currently active" matplotlib Axes. Also needs to accept kwargs
            called ``color`` and  ``label``.

        """

    def map_lower(self, func: Callable[..., object], **kwargs: Any) -> Self:
        """Plot with a bivariate function on the lower diagonal subplots.

        Parameters
        ----------
        func : callable plotting function
            Must take x, y arrays as positional arguments and draw onto the
            "currently active" matplotlib Axes. Also needs to accept kwargs
            called ``color`` and  ``label``.

        """

    def map_upper(self, func: Callable[..., object], **kwargs: Any) -> Self:
        """Plot with a bivariate function on the upper diagonal subplots.

        Parameters
        ----------
        func : callable plotting function
            Must take x, y arrays as positional arguments and draw onto the
            "currently active" matplotlib Axes. Also needs to accept kwargs
            called ``color`` and  ``label``.

        """

    def map_offdiag(self, func: Callable[..., object], **kwargs: Any) -> Self:
        """Plot with a bivariate function on the off-diagonal subplots.

        Parameters
        ----------
        func : callable plotting function
            Must take x, y arrays as positional arguments and draw onto the
            "currently active" matplotlib Axes. Also needs to accept kwargs
            called ``color`` and  ``label``.

        """

    def map_diag(self, func: Callable[..., object], **kwargs: Any) -> Self:
        """Plot with a univariate function on each diagonal subplot.

        Parameters
        ----------
        func : callable plotting function
            Must take an x array as a positional argument and draw onto the
            "currently active" matplotlib Axes. Also needs to accept kwargs
            called ``color`` and  ``label``.

        """

class JointGrid(_BaseGrid):
    """Grid for drawing a bivariate plot with marginal univariate plots.

    Many plots can be drawn by using the figure-level interface :func:`jointplot`.
    Use this class directly when you need more flexibility.

    """

    ax_joint: Axes
    ax_marg_x: Axes
    ax_marg_y: Axes
    x: Series[Any]
    y: Series[Any]
    hue: Series[Any]
    def __init__(
        self,
        data: DataSource | _DataSourceWideForm | None = None,
        *,
        x: ColumnName | _Vector | None = None,
        y: ColumnName | _Vector | None = None,
        hue: ColumnName | _Vector | None = None,
        height: float = 6,
        ratio: float = 5,
        space: float = 0.2,
        palette: _Palette | Colormap | None = None,
        hue_order: Iterable[ColumnName] | None = None,
        hue_norm: NormSpec = None,
        dropna: bool = False,
        xlim: float | tuple[float, float] | None = None,
        ylim: float | tuple[float, float] | None = None,
        marginal_ticks: bool = False,
    ) -> None:
        """Set up the grid of subplots and store data internally for easy plotting.

        Parameters
        ----------
        data : :class:`pandas.DataFrame`, :class:`numpy.ndarray`, mapping, or sequence
            Input data structure. Either a long-form collection of vectors that can be
            assigned to named variables or a wide-form dataset that will be internally
            reshaped.
        x, y : vectors or keys in ``data``
            Variables that specify positions on the x and y axes.
        height : number
            Size of each side of the figure in inches (it will be square).
        ratio : number
            Ratio of joint axes height to marginal axes height.
        space : number
            Space between the joint and marginal axes
        dropna : bool
            If True, remove missing observations before plotting.
        {x, y}lim : pairs of numbers
            Set axis limits to these values before plotting.
        marginal_ticks : bool
            If False, suppress ticks on the count/density axis of the marginal plots.
        hue : vector or key in ``data``
            Semantic variable that is mapped to determine the color of plot elements.
            Note: unlike in :class:`FacetGrid` or :class:`PairGrid`, the axes-level
            functions must support ``hue`` to use it in :class:`JointGrid`.
        palette : string, list, dict, or :class:`matplotlib.colors.Colormap`
            Method for choosing the colors to use when mapping the ``hue`` semantic.
            String values are passed to :func:`color_palette`. List or dict values
            imply categorical mapping, while a colormap object implies numeric mapping.
        hue_order : vector of strings
            Specify the order of processing and plotting for categorical levels of the
            ``hue`` semantic.
        hue_norm : tuple or :class:`matplotlib.colors.Normalize`
            Either a pair of values that set the normalization range in data units
            or an object that will map from data units into a [0, 1] interval. Usage
            implies numeric mapping.

        See Also
        --------
        jointplot : Draw a bivariate plot with univariate marginal distributions.
        PairGrid : Set up a figure with joint and marginal views on multiple variables.
        jointplot : Draw multiple bivariate plots with univariate marginal distributions.

        Examples
        --------

        .. include:: ../docstrings/JointGrid.rst

        """

    def plot(self, joint_func: Callable[..., object], marginal_func: Callable[..., object], **kwargs: Any) -> Self:
        """Draw the plot by passing functions for joint and marginal axes.

        This method passes the ``kwargs`` dictionary to both functions. If you
        need more control, call :meth:`JointGrid.plot_joint` and
        :meth:`JointGrid.plot_marginals` directly with specific parameters.

        Parameters
        ----------
        joint_func, marginal_func : callables
            Functions to draw the bivariate and univariate plots. See methods
            referenced above for information about the required characteristics
            of these functions.
        kwargs
            Additional keyword arguments are passed to both functions.

        Returns
        -------
        :class:`JointGrid` instance
            Returns ``self`` for easy method chaining.

        """

    def plot_joint(self, func: Callable[..., object], **kwargs: Any) -> Self:
        """Draw a bivariate plot on the joint axes of the grid.

        Parameters
        ----------
        func : plotting callable
            If a seaborn function, it should accept ``x`` and ``y``. Otherwise,
            it must accept ``x`` and ``y`` vectors of data as the first two
            positional arguments, and it must plot on the "current" axes.
            If ``hue`` was defined in the class constructor, the function must
            accept ``hue`` as a parameter.
        kwargs
            Keyword argument are passed to the plotting function.

        Returns
        -------
        :class:`JointGrid` instance
            Returns ``self`` for easy method chaining.

        """

    def plot_marginals(self, func: Callable[..., object], **kwargs: Any) -> Self:
        """Draw univariate plots on each marginal axes.

        Parameters
        ----------
        func : plotting callable
            If a seaborn function, it should  accept ``x`` and ``y`` and plot
            when only one of them is defined. Otherwise, it must accept a vector
            of data as the first positional argument and determine its orientation
            using the ``vertical`` parameter, and it must plot on the "current" axes.
            If ``hue`` was defined in the class constructor, it must accept ``hue``
            as a parameter.
        kwargs
            Keyword argument are passed to the plotting function.

        Returns
        -------
        :class:`JointGrid` instance
            Returns ``self`` for easy method chaining.

        """

    def refline(
        self,
        *,
        x: float | None = None,
        y: float | None = None,
        joint: bool = True,
        marginal: bool = True,
        color: ColorType = ".5",
        linestyle: LineStyleType = "--",
        **line_kws: Any,
    ) -> Self:
        """Add a reference line(s) to joint and/or marginal axes.

        Parameters
        ----------
        x, y : numeric
            Value(s) to draw the line(s) at.
        joint, marginal : bools
            Whether to add the reference line(s) to the joint/marginal axes.
        color : :mod:`matplotlib color <matplotlib.colors>`
            Specifies the color of the reference line(s).
        linestyle : str
            Specifies the style of the reference line(s).
        line_kws : key, value mappings
            Other keyword arguments are passed to :meth:`matplotlib.axes.Axes.axvline`
            when ``x`` is not None and :meth:`matplotlib.axes.Axes.axhline` when ``y``
            is not None.

        Returns
        -------
        :class:`JointGrid` instance
            Returns ``self`` for easy method chaining.

        """

    def set_axis_labels(self, xlabel: str = "", ylabel: str = "", **kwargs: Any) -> Self:
        """Set axis labels on the bivariate axes.

        Parameters
        ----------
        xlabel, ylabel : strings
            Label names for the x and y variables.
        kwargs : key, value mappings
            Other keyword arguments are passed to the following functions:

            - :meth:`matplotlib.axes.Axes.set_xlabel`
            - :meth:`matplotlib.axes.Axes.set_ylabel`

        Returns
        -------
        :class:`JointGrid` instance
            Returns ``self`` for easy method chaining.

        """

def pairplot(
    data: DataFrame,
    *,
    hue: str | None = None,
    hue_order: Iterable[str] | None = None,
    palette: _Palette | None = None,
    vars: Iterable[str] | None = None,
    x_vars: Iterable[str] | str | None = None,
    y_vars: Iterable[str] | str | None = None,
    kind: Literal["scatter", "kde", "hist", "reg"] = "scatter",
    diag_kind: Literal["auto", "hist", "kde"] | None = "auto",
    markers: MarkerType | list[MarkerType] | None = None,
    height: float = 2.5,
    aspect: float = 1,
    corner: bool = False,
    dropna: bool = False,
    plot_kws: dict[str, Any] | None = None,
    diag_kws: dict[str, Any] | None = None,
    grid_kws: dict[str, Any] | None = None,
    size: float | None = None,  # deprecated
) -> PairGrid:
    """Plot pairwise relationships in a dataset.

    By default, this function will create a grid of Axes such that each numeric
    variable in ``data`` will by shared across the y-axes across a single row and
    the x-axes across a single column. The diagonal plots are treated
    differently: a univariate distribution plot is drawn to show the marginal
    distribution of the data in each column.

    It is also possible to show a subset of variables or plot different
    variables on the rows and columns.

    This is a high-level interface for :class:`PairGrid` that is intended to
    make it easy to draw a few common styles. You should use :class:`PairGrid`
    directly if you need more flexibility.

    Parameters
    ----------
    data : `pandas.DataFrame`
        Tidy (long-form) dataframe where each column is a variable and
        each row is an observation.
    hue : name of variable in ``data``
        Variable in ``data`` to map plot aspects to different colors.
    hue_order : list of strings
        Order for the levels of the hue variable in the palette
    palette : dict or seaborn color palette
        Set of colors for mapping the ``hue`` variable. If a dict, keys
        should be values  in the ``hue`` variable.
    vars : list of variable names
        Variables within ``data`` to use, otherwise use every column with
        a numeric datatype.
    {x, y}_vars : lists of variable names
        Variables within ``data`` to use separately for the rows and
        columns of the figure; i.e. to make a non-square plot.
    kind : {'scatter', 'kde', 'hist', 'reg'}
        Kind of plot to make.
    diag_kind : {'auto', 'hist', 'kde', None}
        Kind of plot for the diagonal subplots. If 'auto', choose based on
        whether or not ``hue`` is used.
    markers : single matplotlib marker code or list
        Either the marker to use for all scatterplot points or a list of markers
        with a length the same as the number of levels in the hue variable so that
        differently colored points will also have different scatterplot
        markers.
    height : scalar
        Height (in inches) of each facet.
    aspect : scalar
        Aspect * height gives the width (in inches) of each facet.
    corner : bool
        If True, don't add axes to the upper (off-diagonal) triangle of the
        grid, making this a "corner" plot.
    dropna : boolean
        Drop missing values from the data before plotting.
    {plot, diag, grid}_kws : dicts
        Dictionaries of keyword arguments. ``plot_kws`` are passed to the
        bivariate plotting function, ``diag_kws`` are passed to the univariate
        plotting function, and ``grid_kws`` are passed to the :class:`PairGrid`
        constructor.

    Returns
    -------
    grid : :class:`PairGrid`
        Returns the underlying :class:`PairGrid` instance for further tweaking.

    See Also
    --------
    PairGrid : Subplot grid for more flexible plotting of pairwise relationships.
    JointGrid : Grid for plotting joint and marginal distributions of two variables.

    Examples
    --------

    .. include:: ../docstrings/pairplot.rst

    """

def jointplot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    kind: Literal["scatter", "kde", "hist", "hex", "reg", "resid"] = "scatter",
    height: float = 6,
    ratio: float = 5,
    space: float = 0.2,
    dropna: bool = False,
    xlim: float | tuple[float, float] | None = None,
    ylim: float | tuple[float, float] | None = None,
    color: ColorType | None = None,
    palette: _Palette | Colormap | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    hue_norm: NormSpec = None,
    marginal_ticks: bool = False,
    joint_kws: dict[str, Any] | None = None,
    marginal_kws: dict[str, Any] | None = None,
    **kwargs: Any,
) -> JointGrid:
    """Draw a plot of two variables with bivariate and univariate graphs.

    This function provides a convenient interface to the :class:`JointGrid`
    class, with several canned plot kinds. This is intended to be a fairly
    lightweight wrapper; if you need more flexibility, you should use
    :class:`JointGrid` directly.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`, :class:`numpy.ndarray`, mapping, or sequence
        Input data structure. Either a long-form collection of vectors that can be
        assigned to named variables or a wide-form dataset that will be internally
        reshaped.
    x, y : vectors or keys in ``data``
        Variables that specify positions on the x and y axes.
    hue : vector or key in ``data``
        Semantic variable that is mapped to determine the color of plot elements.
    kind : { "scatter" | "kde" | "hist" | "hex" | "reg" | "resid" }
        Kind of plot to draw. See the examples for references to the underlying functions.
    height : numeric
        Size of the figure (it will be square).
    ratio : numeric
        Ratio of joint axes height to marginal axes height.
    space : numeric
        Space between the joint and marginal axes
    dropna : bool
        If True, remove observations that are missing from ``x`` and ``y``.
    {x, y}lim : pairs of numbers
        Axis limits to set before plotting.
    color : :mod:`matplotlib color <matplotlib.colors>`
        Single color specification for when hue mapping is not used. Otherwise, the
        plot will try to hook into the matplotlib property cycle.
    palette : string, list, dict, or :class:`matplotlib.colors.Colormap`
        Method for choosing the colors to use when mapping the ``hue`` semantic.
        String values are passed to :func:`color_palette`. List or dict values
        imply categorical mapping, while a colormap object implies numeric mapping.
    hue_order : vector of strings
        Specify the order of processing and plotting for categorical levels of the
        ``hue`` semantic.
    hue_norm : tuple or :class:`matplotlib.colors.Normalize`
        Either a pair of values that set the normalization range in data units
        or an object that will map from data units into a [0, 1] interval. Usage
        implies numeric mapping.
    marginal_ticks : bool
        If False, suppress ticks on the count/density axis of the marginal plots.
    {joint, marginal}_kws : dicts
        Additional keyword arguments for the plot components.
    kwargs
        Additional keyword arguments are passed to the function used to
        draw the plot on the joint Axes, superseding items in the
        ``joint_kws`` dictionary.

    Returns
    -------
    :class:`JointGrid`
        An object managing multiple subplots that correspond to joint and marginal axes
        for plotting a bivariate relationship or distribution.

    See Also
    --------
    JointGrid : Set up a figure with joint and marginal views on bivariate data.
    PairGrid : Set up a figure with joint and marginal views on multiple variables.
    jointplot : Draw multiple bivariate plots with univariate marginal distributions.

    Examples
    --------

    .. include:: ../docstrings/jointplot.rst

    """
