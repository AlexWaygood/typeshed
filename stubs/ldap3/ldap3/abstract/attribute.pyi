""" """

from typing import Any

class Attribute:
    """Attribute/values object, it includes the search result (after post_query transformation) of each attribute in an entry

    Attribute object is read only

    - values: contain the processed attribute values
    - raw_values': contain the unprocessed attribute values


    """

    key: Any
    definition: Any
    values: Any
    raw_values: Any
    response: Any
    entry: Any
    cursor: Any
    other_names: Any
    def __init__(self, attr_def, entry, cursor) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self): ...
    def __getitem__(self, item): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    @property
    def value(self):
        """
        :return: The single value or a list of values of the attribute.
        """

class OperationalAttribute(Attribute):
    """Operational attribute/values object. Include the search result of an
    operational attribute in an entry

    OperationalAttribute object is read only

    - values: contains the processed attribute values
    - raw_values: contains the unprocessed attribute values

    It may not have an AttrDef

    """

class WritableAttribute(Attribute):
    def __iadd__(self, other): ...
    def __isub__(self, other): ...
    def add(self, values) -> None: ...
    def set(self, values) -> None: ...
    def delete(self, values) -> None: ...
    def remove(self) -> None: ...
    def discard(self) -> None: ...
    @property
    def virtual(self): ...
    @property
    def changes(self): ...
