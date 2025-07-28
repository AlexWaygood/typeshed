"""Simplified split-apply-combine paradigm on dataframes for internal use."""

from _typeshed import Incomplete
from collections.abc import Callable, Hashable, Mapping
from typing_extensions import Concatenate, ParamSpec, TypeAlias

from numpy import ufunc
from pandas import DataFrame

# pandas._typing.AggFuncTypeFrame is partially Unknown
_AggFuncTypeBase: TypeAlias = Callable[..., Incomplete] | str | ufunc
_AggFuncTypeDictFrame: TypeAlias = Mapping[Hashable, _AggFuncTypeBase | list[_AggFuncTypeBase]]
_AggFuncTypeFrame: TypeAlias = _AggFuncTypeBase | list[_AggFuncTypeBase] | _AggFuncTypeDictFrame

_P = ParamSpec("_P")

class GroupBy:
    """
    Interface for Pandas GroupBy operations allowing specified group order.

    Writing our own class to do this has a few advantages:
    - It constrains the interface between Plot and Stat/Move objects
    - It allows control over the row order of the GroupBy result, which is
      important when using in the context of some Move operations (dodge, stack, ...)
    - It simplifies some complexities regarding the return type and Index contents
      one encounters with Pandas, especially for DataFrame -> DataFrame applies
    - It increases future flexibility regarding alternate DataFrame libraries

    """

    order: dict[str, list[Incomplete] | None]
    def __init__(self, order: list[str] | dict[str, list[Incomplete] | None]) -> None:
        """
        Initialize the GroupBy from grouping variables and optional level orders.

        Parameters
        ----------
        order
            List of variable names or dict mapping names to desired level orders.
            Level order values can be None to use default ordering rules. The
            variables can include names that are not expected to appear in the
            data; these will be dropped before the groups are defined.

        """
    # Signature based on pandas.core.groupby.generic.DataFrameGroupBy.aggregate
    # args and kwargs possible values depend on func which itself can be
    # an attribute name, a mapping, a callable, or lead to a jitted numba function
    def agg(
        self,
        data: DataFrame,
        func: _AggFuncTypeFrame = ...,
        *args,
        engine: str | None = None,
        engine_kwargs: dict[str, bool] | None = None,
        **kwargs,
    ) -> DataFrame:
        """
        Reduce each group to a single row in the output.

        The output will have a row for each unique combination of the grouping
        variable levels with null values for the aggregated variable(s) where
        those combinations do not appear in the dataset.

        """

    def apply(
        self, data: DataFrame, func: Callable[Concatenate[DataFrame, _P], DataFrame], *args: _P.args, **kwargs: _P.kwargs
    ) -> DataFrame:
        """Apply a DataFrame -> DataFrame mapping to each group."""
