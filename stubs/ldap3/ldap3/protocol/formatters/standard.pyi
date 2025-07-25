""" """

from typing import Any

standard_formatter: Any

def find_attribute_helpers(attr_type, name, custom_formatter):
    """
    Tries to format following the OIDs info and format_helper specification.
    Search for attribute oid, then attribute name (can be multiple), then attribute syntax
    Precedence is:
    1. attribute name
    2. attribute oid(from schema)
    3. attribute names (from oid_info)
    4. attribute syntax (from schema)
    Custom formatters can be defined in Server object and have precedence over the standard_formatters
    If no formatter is found the raw_value is returned as bytes.
    Attributes defined as SINGLE_VALUE in schema are returned as a single object, otherwise are returned as a list of object
    Formatter functions can return any kind of object
    return a tuple (formatter, validator)
    """

def format_attribute_values(schema, name, values, custom_formatter): ...
def find_attribute_validator(schema, name, custom_validator): ...
