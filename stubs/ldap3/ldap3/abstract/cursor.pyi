""" """

from typing import Any, NamedTuple

class Operation(NamedTuple):
    """Operation(request, result, response)"""

    request: Any
    result: Any
    response: Any

class Cursor:
    connection: Any
    get_operational_attributes: Any
    definition: Any
    attributes: Any
    controls: Any
    execution_time: Any
    entries: Any
    schema: Any
    def __init__(
        self,
        connection,
        object_def,
        get_operational_attributes: bool = False,
        attributes=None,
        controls=None,
        auxiliary_class=None,
    ) -> None: ...
    def __iter__(self): ...
    def __getitem__(self, item):
        """Return indexed item, if index is not found then try to sequentially search in DN of entries.
        If only one entry is found return it else raise a KeyError exception. The exception message
        includes the number of entries that matches, if less than 10 entries match then show the DNs
        in the exception message.
        """

    def __len__(self) -> int: ...
    def __bool__(self) -> bool: ...
    def match_dn(self, dn):
        """Return entries with text in DN"""

    def match(self, attributes, value):
        """Return entries with text in one of the specified attributes"""

    def remove(self, entry) -> None: ...
    @property
    def operations(self): ...
    @property
    def errors(self): ...
    @property
    def failed(self): ...

class Reader(Cursor):
    """Reader object to perform searches:

    :param connection: the LDAP connection object to use
    :type connection: LDAPConnection
    :param object_def: the ObjectDef of the LDAP object returned
    :type object_def: ObjectDef
    :param query: the simplified query (will be transformed in an LDAP filter)
    :type query: str
    :param base: starting base of the search
    :type base: str
    :param components_in_and: specify if assertions in the query must all be satisfied or not (AND/OR)
    :type components_in_and: bool
    :param sub_tree: specify if the search must be performed ad Single Level (False) or Whole SubTree (True)
    :type sub_tree: bool
    :param get_operational_attributes: specify if operational attributes are returned or not
    :type get_operational_attributes: bool
    :param controls: controls to be used in search
    :type controls: tuple

    """

    entry_class: Any
    attribute_class: Any
    entry_initial_status: Any
    sub_tree: Any
    base: Any
    dereference_aliases: Any
    validated_query: Any
    query_filter: Any
    def __init__(
        self,
        connection,
        object_def,
        base,
        query: str = "",
        components_in_and: bool = True,
        sub_tree: bool = True,
        get_operational_attributes: bool = False,
        attributes=None,
        controls=None,
        auxiliary_class=None,
    ) -> None: ...
    @property
    def query(self): ...
    @query.setter
    def query(self, value) -> None: ...
    @property
    def components_in_and(self): ...
    @components_in_and.setter
    def components_in_and(self, value) -> None: ...
    def clear(self) -> None:
        """Clear the Reader search parameters"""
    execution_time: Any
    entries: Any
    def reset(self) -> None:
        """Clear all the Reader parameters"""

    def search(self, attributes=None):
        """Perform the LDAP search

        :return: Entries found in search

        """

    def search_object(self, entry_dn=None, attributes=None):
        """Perform the LDAP search operation SINGLE_OBJECT scope

        :return: Entry found in search

        """

    def search_level(self, attributes=None):
        """Perform the LDAP search operation with SINGLE_LEVEL scope

        :return: Entries found in search

        """

    def search_subtree(self, attributes=None):
        """Perform the LDAP search operation WHOLE_SUBTREE scope

        :return: Entries found in search

        """

    def search_paged(self, paged_size, paged_criticality: bool = True, generator: bool = True, attributes=None):
        """Perform a paged search, can be called as an Iterator

        :param attributes: optional attributes to search
        :param paged_size: number of entries returned in each search
        :type paged_size: int
        :param paged_criticality: specify if server must not execute the search if it is not capable of paging searches
        :type paged_criticality: bool
        :param generator: if True the paged searches are executed while generating the entries,
                          if False all the paged searches are execute before returning the generator
        :type generator: bool
        :return: Entries found in search

        """

class Writer(Cursor):
    entry_class: Any
    attribute_class: Any
    entry_initial_status: Any
    @staticmethod
    def from_cursor(cursor, connection=None, object_def=None, custom_validator=None): ...
    @staticmethod
    def from_response(connection, object_def, response=None): ...
    dereference_aliases: Any
    def __init__(
        self,
        connection,
        object_def,
        get_operational_attributes: bool = False,
        attributes=None,
        controls=None,
        auxiliary_class=None,
    ) -> None: ...
    execution_time: Any
    def commit(self, refresh: bool = True): ...
    def discard(self) -> None: ...
    def new(self, dn): ...
    def refresh_entry(self, entry, tries: int = 4, seconds: int = 2): ...
