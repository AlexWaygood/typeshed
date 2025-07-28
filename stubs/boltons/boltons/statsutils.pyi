"""``statsutils`` provides tools aimed primarily at descriptive
statistics for data analysis, such as :func:`mean` (average),
:func:`median`, :func:`variance`, and many others,

The :class:`Stats` type provides all the main functionality of the
``statsutils`` module. A :class:`Stats` object wraps a given dataset,
providing all statistical measures as property attributes. These
attributes cache their results, which allows efficient computation of
multiple measures, as many measures rely on other measures. For
example, relative standard deviation (:attr:`Stats.rel_std_dev`)
relies on both the mean and standard deviation. The Stats object
caches those results so no rework is done.

The :class:`Stats` type's attributes have module-level counterparts for
convenience when the computation reuse advantages do not apply.

>>> stats = Stats(range(42))
>>> stats.mean
20.5
>>> mean(range(42))
20.5

Statistics is a large field, and ``statsutils`` is focused on a few
basic techniques that are useful in software. The following is a brief
introduction to those techniques. For a more in-depth introduction,
`Statistics for Software
<https://www.paypal-engineering.com/2016/04/11/statistics-for-software/>`_,
an article I wrote on the topic. It introduces key terminology vital
to effective usage of statistics.

Statistical moments
-------------------

Python programmers are probably familiar with the concept of the
*mean* or *average*, which gives a rough quantitiative middle value by
which a sample can be can be generalized. However, the mean is just
the first of four `moment`_-based measures by which a sample or
distribution can be measured.

The four `Standardized moments`_ are:

  1. `Mean`_ - :func:`mean` - theoretical middle value
  2. `Variance`_ - :func:`variance` - width of value dispersion
  3. `Skewness`_ - :func:`skewness` - symmetry of distribution
  4. `Kurtosis`_ - :func:`kurtosis` - "peakiness" or "long-tailed"-ness

For more information check out `the Moment article on Wikipedia`_.

.. _moment: https://en.wikipedia.org/wiki/Moment_(mathematics)
.. _Standardized moments: https://en.wikipedia.org/wiki/Standardized_moment
.. _Mean: https://en.wikipedia.org/wiki/Mean
.. _Variance: https://en.wikipedia.org/wiki/Variance
.. _Skewness: https://en.wikipedia.org/wiki/Skewness
.. _Kurtosis: https://en.wikipedia.org/wiki/Kurtosis
.. _the Moment article on Wikipedia: https://en.wikipedia.org/wiki/Moment_(mathematics)

Keep in mind that while these moments can give a bit more insight into
the shape and distribution of data, they do not guarantee a complete
picture. Wildly different datasets can have the same values for all
four moments, so generalize wisely.

Robust statistics
-----------------

Moment-based statistics are notorious for being easily skewed by
outliers. The whole field of robust statistics aims to mitigate this
dilemma. ``statsutils`` also includes several robust statistical methods:

  * `Median`_ - The middle value of a sorted dataset
  * `Trimean`_ - Another robust measure of the data's central tendency
  * `Median Absolute Deviation`_ (MAD) - A robust measure of
    variability, a natural counterpart to :func:`variance`.
  * `Trimming`_ - Reducing a dataset to only the middle majority of
    data is a simple way of making other estimators more robust.

.. _Median: https://en.wikipedia.org/wiki/Median
.. _Trimean: https://en.wikipedia.org/wiki/Trimean
.. _Median Absolute Deviation: https://en.wikipedia.org/wiki/Median_absolute_deviation
.. _Trimming: https://en.wikipedia.org/wiki/Trimmed_estimator


Online and Offline Statistics
-----------------------------

Unrelated to computer networking, `online`_ statistics involve
calculating statistics in a `streaming`_ fashion, without all the data
being available. The :class:`Stats` type is meant for the more
traditional offline statistics when all the data is available. For
pure-Python online statistics accumulators, look at the `Lithoxyl`_
system instrumentation package.

.. _Online: https://en.wikipedia.org/wiki/Online_algorithm
.. _streaming: https://en.wikipedia.org/wiki/Streaming_algorithm
.. _Lithoxyl: https://github.com/mahmoud/lithoxyl

"""

from _typeshed import ConvertibleToFloat, Incomplete
from collections.abc import Callable, Iterable, Iterator
from typing import Any, Literal, overload
from typing_extensions import Self

class _StatsProperty:
    name: str
    func: Callable[..., Any]
    internal_name: str
    __doc__: str | None
    def __init__(self, name: str, func: Callable[..., Any]) -> None: ...
    @overload
    def __get__(self, obj: None, objtype: object = None) -> Self: ...
    @overload
    def __get__(self, obj: Stats, objtype: object = None) -> float: ...

class Stats:
    """The ``Stats`` type is used to represent a group of unordered
    statistical datapoints for calculations such as mean, median, and
    variance.

    Args:

        data (list): List or other iterable containing numeric values.
        default (float): A value to be returned when a given
            statistical measure is not defined. 0.0 by default, but
            ``float('nan')`` is appropriate for stricter applications.
        use_copy (bool): By default Stats objects copy the initial
            data into a new list to avoid issues with
            modifications. Pass ``False`` to disable this behavior.
        is_sorted (bool): Presorted data can skip an extra sorting
            step for a little speed boost. Defaults to False.

    """

    data: list[float]
    default: float
    @overload
    def __init__(self, data: list[float], default: float = 0.0, *, use_copy: Literal[False], is_sorted: bool = False) -> None: ...
    @overload
    def __init__(self, data: list[float], default: float, use_copy: Literal[False], is_sorted: bool = False) -> None: ...
    @overload
    def __init__(
        self, data: Iterable[float], default: float = 0.0, use_copy: Literal[True] = True, is_sorted: bool = False
    ) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[float]: ...
    def clear_cache(self) -> None:
        """``Stats`` objects automatically cache intermediary calculations
        that can be reused. For instance, accessing the ``std_dev``
        attribute after the ``variance`` attribute will be
        significantly faster for medium-to-large datasets.

        If you modify the object by adding additional data points,
        call this function to have the cached statistics recomputed.

        """
    count: _StatsProperty
    mean: _StatsProperty
    max: _StatsProperty
    min: _StatsProperty
    median: _StatsProperty
    iqr: _StatsProperty
    trimean: _StatsProperty
    variance: _StatsProperty
    std_dev: _StatsProperty
    median_abs_dev: _StatsProperty
    mad: _StatsProperty
    rel_std_dev: _StatsProperty
    skewness: _StatsProperty
    kurtosis: _StatsProperty
    pearson_type: _StatsProperty
    def get_quantile(self, q: ConvertibleToFloat) -> float:
        """Get a quantile from the dataset. Quantiles are floating point
        values between ``0.0`` and ``1.0``, with ``0.0`` representing
        the minimum value in the dataset and ``1.0`` representing the
        maximum. ``0.5`` represents the median:

        >>> Stats(range(100)).get_quantile(0.5)
        49.5
        """

    def get_zscore(self, value: float) -> float:
        """Get the z-score for *value* in the group. If the standard deviation
        is 0, 0 inf or -inf will be returned to indicate whether the value is
        equal to, greater than or below the group's mean.
        """

    def trim_relative(self, amount: float = 0.15) -> None:
        """A utility function used to cut a proportion of values off each end
        of a list of values. This has the effect of limiting the
        effect of outliers.

        Args:
            amount (float): A value between 0.0 and 0.5 to trim off of
                each side of the data.

        .. note:

            This operation modifies the data in-place. It does not
            make or return a copy.

        """

    def get_histogram_counts(self, bins: int | list[float] | None = None, **kw) -> list[tuple[float, int]]:
        """Produces a list of ``(bin, count)`` pairs comprising a histogram of
        the Stats object's data, using fixed-width bins. See
        :meth:`Stats.format_histogram` for more details.

        Args:
            bins (int): maximum number of bins, or list of
                floating-point bin boundaries. Defaults to the output of
                Freedman's algorithm.
            bin_digits (int): Number of digits used to round down the
                bin boundaries. Defaults to 1.

        The output of this method can be stored and/or modified, and
        then passed to :func:`statsutils.format_histogram_counts` to
        achieve the same text formatting as the
        :meth:`~Stats.format_histogram` method. This can be useful for
        snapshotting over time.
        """

    def format_histogram(self, bins: int | list[float] | None = None, **kw) -> str:
        """Produces a textual histogram of the data, using fixed-width bins,
        allowing for simple visualization, even in console environments.

        >>> data = list(range(20)) + list(range(5, 15)) + [10]
        >>> print(Stats(data).format_histogram(width=30))
         0.0:  5 #########
         4.4:  8 ###############
         8.9: 11 ####################
        13.3:  5 #########
        17.8:  2 ####

        In this histogram, five values are between 0.0 and 4.4, eight
        are between 4.4 and 8.9, and two values lie between 17.8 and
        the max.

        You can specify the number of bins, or provide a list of
        bin boundaries themselves. If no bins are provided, as in the
        example above, `Freedman's algorithm`_ for bin selection is
        used.

        Args:
            bins (int): Maximum number of bins for the
                histogram. Also accepts a list of floating-point
                bin boundaries. If the minimum boundary is still
                greater than the minimum value in the data, that
                boundary will be implicitly added. Defaults to the bin
                boundaries returned by `Freedman's algorithm`_.
            bin_digits (int): Number of digits to round each bin
                to. Note that bins are always rounded down to avoid
                clipping any data. Defaults to 1.
            width (int): integer number of columns in the longest line
               in the histogram. Defaults to console width on Python
               3.3+, or 80 if that is not available.
            format_bin (callable): Called on each bin to create a
               label for the final output. Use this function to add
               units, such as "ms" for milliseconds.

        Should you want something more programmatically reusable, see
        the :meth:`~Stats.get_histogram_counts` method, the output of
        is used by format_histogram. The :meth:`~Stats.describe`
        method is another useful summarization method, albeit less
        visual.

        .. _Freedman's algorithm: https://en.wikipedia.org/wiki/Freedman%E2%80%93Diaconis_rule
        """

    def describe(
        self, quantiles: Iterable[float] | None = None, format: str | None = None
    ) -> dict[str, float] | list[tuple[str, float]] | str:
        """Provides standard summary statistics for the data in the Stats
        object, in one of several convenient formats.

        Args:
            quantiles (list): A list of numeric values to use as
                quantiles in the resulting summary. All values must be
                0.0-1.0, with 0.5 representing the median. Defaults to
                ``[0.25, 0.5, 0.75]``, representing the standard
                quartiles.
            format (str): Controls the return type of the function,
                with one of three valid values: ``"dict"`` gives back
                a :class:`dict` with the appropriate keys and
                values. ``"list"`` is a list of key-value pairs in an
                order suitable to pass to an OrderedDict or HTML
                table. ``"text"`` converts the values to text suitable
                for printing, as seen below.

        Here is the information returned by a default ``describe``, as
        presented in the ``"text"`` format:

        >>> stats = Stats(range(1, 8))
        >>> print(stats.describe(format='text'))
        count:    7
        mean:     4.0
        std_dev:  2.0
        mad:      2.0
        min:      1
        0.25:     2.5
        0.5:      4
        0.75:     5.5
        max:      7

        For more advanced descriptive statistics, check out my blog
        post on the topic `Statistics for Software
        <https://www.paypal-engineering.com/2016/04/11/statistics-for-software/>`_.

        """

def describe(
    data: Iterable[float], quantiles: Iterable[float] | None = None, format: str | None = None
) -> dict[str, float] | list[tuple[str, float]] | str:
    """A convenience function to get standard summary statistics useful
    for describing most data. See :meth:`Stats.describe` for more
    details.

    >>> print(describe(range(7), format='text'))
    count:    7
    mean:     3.0
    std_dev:  2.0
    mad:      2.0
    min:      0
    0.25:     1.5
    0.5:      3
    0.75:     4.5
    max:      6

    See :meth:`Stats.format_histogram` for another very useful
    summarization that uses textual visualization.
    """

mean: Incomplete
median: Incomplete
iqr: Incomplete
trimean: Incomplete
variance: Incomplete
std_dev: Incomplete
median_abs_dev: Incomplete
rel_std_dev: Incomplete
skewness: Incomplete
kurtosis: Incomplete
pearson_type: Incomplete

def format_histogram_counts(
    bin_counts: list[float], width: int | None = None, format_bin: Callable[..., Any] | None = None
) -> str:
    """The formatting logic behind :meth:`Stats.format_histogram`, which
    takes the output of :meth:`Stats.get_histogram_counts`, and passes
    them to this function.

    Args:
        bin_counts (list): A list of bin values to counts.
        width (int): Number of character columns in the text output,
            defaults to 80 or console width in Python 3.3+.
        format_bin (callable): Used to convert bin values into string
            labels.
    """
