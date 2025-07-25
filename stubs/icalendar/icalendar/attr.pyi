"""Attributes of Components and properties."""

rdates_property: property
exdates_property: property
rrules_property: property

def multi_language_text_property(main_prop: str, compatibility_prop: str, doc: str) -> property:
    """This creates a text property.

    This property can be defined several times with different ``LANGUAGE`` parameters.

    Args:
        main_prop (str): The property to set and get, such as ``NAME``
        compatibility_prop (str): An old property used before, such as ``X-WR-CALNAME``
        doc (str): The documentation string
    """

def single_int_property(prop: str, default: int, doc: str) -> property:
    """Create a property for an int value that exists only once.

    Args:
        prop: The name of the property
        default: The default value
        doc: The documentation string
    """

def single_utc_property(name: str, docs: str) -> property:
    """Create a property to access a value of datetime in UTC timezone.

    Args:
        name: name of the property
        docs: documentation string
    """

def single_string_property(name: str, docs: str, other_name: str | None = None) -> property:
    """Create a property to access a single string value."""

color_property: property
sequence_property: property
categories_property: property
uid_property: property

__all__ = [
    "categories_property",
    "color_property",
    "exdates_property",
    "multi_language_text_property",
    "rdates_property",
    "rrules_property",
    "sequence_property",
    "single_int_property",
    "single_utc_property",
    "uid_property",
]
