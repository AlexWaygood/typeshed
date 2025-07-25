"""
Components for parsing variable assignments and internally representing plot data.
"""

from _typeshed import Incomplete
from collections.abc import Mapping
from typing import TypeVar, overload

from pandas import DataFrame
from pandas.core.interchange.dataframe_protocol import DataFrame as DataFrameProtocol
from seaborn._core.typing import DataSource, VariableSpec

_T = TypeVar("_T", Mapping[Incomplete, Incomplete], None)

class PlotData:
    """
    Data table with plot variable schema and mapping to original names.

    Contains logic for parsing variable specification arguments and updating
    the table with layer-specific data and/or mappings.

    Parameters
    ----------
    data
        Input data where variable names map to vector values.
    variables
        Keys are names of plot variables (x, y, ...) each value is one of:

        - name of a column (or index level, or dictionary entry) in `data`
        - vector in any format that can construct a :class:`pandas.DataFrame`

    Attributes
    ----------
    frame
        Data table with column names having defined plot variables.
    names
        Dictionary mapping plot variable names to names in source data structure(s).
    ids
        Dictionary mapping plot variable names to unique data source identifiers.

    """

    frame: DataFrame
    frames: dict[tuple[str, str], DataFrame]
    names: dict[str, str | None]
    ids: dict[str, str | int]
    source_data: DataSource
    source_vars: dict[str, VariableSpec]
    def __init__(self, data: DataSource, variables: dict[str, VariableSpec]) -> None: ...
    def __contains__(self, key: str) -> bool:
        """Boolean check on whether a variable is defined in this dataset."""

    def join(self, data: DataSource, variables: dict[str, VariableSpec] | None) -> PlotData:
        """Add, replace, or drop variables and return as a new dataset."""

@overload
def handle_data_source(data: _T) -> _T:
    """Convert the data source object to a common union representation."""

@overload
def handle_data_source(data: DataFrameProtocol) -> DataFrame: ...
def convert_dataframe_to_pandas(data: object) -> DataFrame:
    """Use the DataFrame exchange protocol, or fail gracefully."""
