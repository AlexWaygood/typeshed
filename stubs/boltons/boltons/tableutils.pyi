"""If there is one recurring theme in ``boltons``, it is that Python
has excellent datastructures that constitute a good foundation for
most quick manipulations, as well as building applications. However,
Python usage has grown much faster than builtin data structure
power. Python has a growing need for more advanced general-purpose
data structures which behave intuitively.

The :class:`Table` class is one example. When handed one- or
two-dimensional data, it can provide useful, if basic, text and HTML
renditions of small to medium sized data. It also heuristically
handles recursive data of various formats (lists, dicts, namedtuples,
objects).

For more advanced :class:`Table`-style manipulation check out the
`pandas`_ DataFrame.

.. _pandas: http://pandas.pydata.org/

"""

from _typeshed import Incomplete

class UnsupportedData(TypeError): ...

class InputType:
    def __init__(self, *a, **kw) -> None: ...
    def get_entry_seq(self, data_seq, headers): ...

class DictInputType(InputType):
    def check_type(self, obj): ...
    def guess_headers(self, obj): ...
    def get_entry(self, obj, headers): ...
    def get_entry_seq(self, obj, headers): ...

class ObjectInputType(InputType):
    def check_type(self, obj): ...
    def guess_headers(self, obj): ...
    def get_entry(self, obj, headers): ...

class ListInputType(InputType):
    def check_type(self, obj): ...
    def guess_headers(self, obj) -> None: ...
    def get_entry(self, obj, headers): ...
    def get_entry_seq(self, obj_seq, headers): ...

class TupleInputType(InputType):
    def check_type(self, obj): ...
    def guess_headers(self, obj) -> None: ...
    def get_entry(self, obj, headers): ...
    def get_entry_seq(self, obj_seq, headers): ...

class NamedTupleInputType(InputType):
    def check_type(self, obj): ...
    def guess_headers(self, obj): ...
    def get_entry(self, obj, headers): ...
    def get_entry_seq(self, obj_seq, headers): ...

class Table:
    """
    This Table class is meant to be simple, low-overhead, and extensible. Its
    most common use would be for translation between in-memory data
    structures and serialization formats, such as HTML and console-ready text.

    As such, it stores data in list-of-lists format, and *does not* copy
    lists passed in. It also reserves the right to modify those lists in a
    "filling" process, whereby short lists are extended to the width of
    the table (usually determined by number of headers). This greatly
    reduces overhead and processing/validation that would have to occur
    otherwise.

    General description of headers behavior:

    Headers describe the columns, but are not part of the data, however,
    if the *headers* argument is omitted, Table tries to infer header
    names from the data. It is possible to have a table with no headers,
    just pass in ``headers=None``.

    Supported inputs:

    * :class:`list` of :class:`list` objects
    * :class:`dict` (list/single)
    * :class:`object` (list/single)
    * :class:`collections.namedtuple` (list/single)
    * TODO: DB API cursor?
    * TODO: json

    Supported outputs:

    * HTML
    * Pretty text (also usable as GF Markdown)
    * TODO: CSV
    * TODO: json
    * TODO: json lines

    To minimize resident size, the Table data is stored as a list of lists.
    """

    headers: Incomplete
    metadata: Incomplete
    def __init__(self, data=None, headers=..., metadata=None) -> None: ...
    def extend(self, data) -> None:
        """
        Append the given data to the end of the Table.
        """

    @classmethod
    def from_dict(cls, data, headers=..., max_depth: int = 1, metadata=None):
        """Create a Table from a :class:`dict`. Operates the same as
        :meth:`from_data`, but forces interpretation of the data as a
        Mapping.
        """

    @classmethod
    def from_list(cls, data, headers=..., max_depth: int = 1, metadata=None):
        """Create a Table from a :class:`list`. Operates the same as
        :meth:`from_data`, but forces the interpretation of the data
        as a Sequence.
        """

    @classmethod
    def from_object(cls, data, headers=..., max_depth: int = 1, metadata=None):
        """Create a Table from an :class:`object`. Operates the same as
        :meth:`from_data`, but forces the interpretation of the data
        as an object. May be useful for some :class:`dict` and
        :class:`list` subtypes.
        """

    @classmethod
    def from_data(cls, data, headers=..., max_depth: int = 1, **kwargs):
        """Create a Table from any supported data, heuristically
        selecting how to represent the data in Table format.

        Args:
            data (object): Any object or iterable with data to be
                imported to the Table.

            headers (iterable): An iterable of headers to be matched
                to the data. If not explicitly passed, headers will be
                guessed for certain datatypes.

            max_depth (int): The level to which nested Tables should
                be created (default: 1).

            _data_type (InputType subclass): For advanced use cases,
                do not guess the type of the input data, use this data
                type instead.
        """

    def __len__(self): ...
    def __getitem__(self, idx): ...
    def to_html(
        self,
        orientation=None,
        wrapped: bool = True,
        with_headers: bool = True,
        with_newlines: bool = True,
        with_metadata: bool = False,
        max_depth: int = 1,
    ):
        """Render this Table to HTML. Configure the structure of Table
        HTML by subclassing and overriding ``_html_*`` class
        attributes.

        Args:
            orientation (str): one of 'auto', 'horizontal', or
                'vertical' (or the first letter of any of
                those). Default 'auto'.
            wrapped (bool): whether or not to include the wrapping
                '<table></table>' tags. Default ``True``, set to
                ``False`` if appending multiple Table outputs or an
                otherwise customized HTML wrapping tag is needed.
            with_newlines (bool): Set to ``True`` if output should
                include added newlines to make the HTML more
                readable. Default ``False``.
            with_metadata (bool/str): Set to ``True`` if output should
                be preceded with a Table of preset metadata, if it
                exists. Set to special value ``'bottom'`` if the
                metadata Table HTML should come *after* the main HTML output.
            max_depth (int): Indicate how deeply to nest HTML tables
                before simply reverting to :func:`repr`-ing the nested
                data.

        Returns:
            A text string of the HTML of the rendered table.

        """

    def get_cell_html(self, value):
        """Called on each value in an HTML table. By default it simply escapes
        the HTML. Override this method to add additional conditions
        and behaviors, but take care to ensure the final output is
        HTML escaped.
        """

    def to_text(self, with_headers: bool = True, maxlen=None):
        """Get the Table's textual representation. Only works well
        for Tables with non-recursive data.

        Args:
            with_headers (bool): Whether to include a header row at the top.
            maxlen (int): Max length of data in each cell.
        """

__all__ = ["Table"]
