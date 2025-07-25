""" """

from typing import Any

class EntryState:
    """Contains data on the status of the entry. Does not pollute the Entry __dict__."""

    dn: Any
    status: Any
    attributes: Any
    raw_attributes: Any
    response: Any
    cursor: Any
    origin: Any
    read_time: Any
    changes: Any
    definition: Any
    def __init__(self, dn, cursor) -> None: ...
    def set_status(self, status) -> None: ...
    @property
    def entry_raw_attributes(self): ...

class EntryBase:
    """The Entry object contains a single LDAP entry.
    Attributes can be accessed either by sequence, by assignment
    or as dictionary keys. Keys are not case sensitive.

    The Entry object is read only

    - The DN is retrieved by entry_dn
    - The cursor reference is in _cursor
    - Raw attributes values are retrieved with _raw_attributes and the _raw_attribute() methods
    """

    def __init__(self, dn, cursor) -> None: ...
    def __iter__(self): ...
    def __contains__(self, item): ...
    def __getattr__(self, item: str): ...
    def __setattr__(self, item: str, value) -> None: ...
    def __getitem__(self, item): ...
    def __eq__(self, other): ...
    def __lt__(self, other): ...
    @property
    def entry_dn(self): ...
    @property
    def entry_cursor(self): ...
    @property
    def entry_status(self): ...
    @property
    def entry_definition(self): ...
    @property
    def entry_raw_attributes(self): ...
    def entry_raw_attribute(self, name):
        """

        :param name: name of the attribute
        :return: raw (unencoded) value of the attribute, None if attribute is not found
        """

    @property
    def entry_mandatory_attributes(self): ...
    @property
    def entry_attributes(self): ...
    @property
    def entry_attributes_as_dict(self): ...
    @property
    def entry_read_time(self): ...
    def entry_to_json(
        self,
        raw: bool = False,
        indent: int = 4,
        sort: bool = True,
        stream=None,
        checked_attributes: bool = True,
        include_empty: bool = True,
    ): ...
    def entry_to_ldif(self, all_base64: bool = False, line_separator=None, sort_order=None, stream=None): ...

class Entry(EntryBase):
    """The Entry object contains a single LDAP entry.
    Attributes can be accessed either by sequence, by assignment
    or as dictionary keys. Keys are not case sensitive.

    The Entry object is read only

    - The DN is retrieved by entry_dn
    - The Reader reference is in _cursor()
    - Raw attributes values are retrieved by the _ra_attributes and
      _raw_attribute() methods

    """

    def entry_writable(
        self, object_def=None, writer_cursor=None, attributes=None, custom_validator=None, auxiliary_class=None
    ): ...

class WritableEntry(EntryBase):
    def __setitem__(self, key, value) -> None: ...
    def __setattr__(self, item: str, value) -> None: ...
    def __getattr__(self, item: str): ...
    @property
    def entry_virtual_attributes(self): ...
    def entry_commit_changes(self, refresh: bool = True, controls=None, clear_history: bool = True): ...
    def entry_discard_changes(self) -> None: ...
    def entry_delete(self) -> None: ...
    def entry_refresh(self, tries: int = 4, seconds: int = 2):
        """

        Refreshes the entry from the LDAP Server
        """

    def entry_move(self, destination_dn) -> None: ...
    def entry_rename(self, new_name) -> None: ...
    @property
    def entry_changes(self): ...
