from _typeshed import Incomplete
from typing import ClassVar

class Behavior:
    """
    Behavior (validation, encoding, and transformations) for vobjects.

    Abstract class to describe vobject options, requirements and encodings.

    Behaviors are used for root components like VCALENDAR, for subcomponents
    like VEVENT, and for individual lines in components.

    Behavior subclasses are not meant to be instantiated, all methods should
    be classmethods.

    @cvar name:
        The uppercase name of the object described by the class, or a generic
        name if the class defines behavior for many objects.
    @cvar description:
        A brief excerpt from the RFC explaining the function of the component or
        line.
    @cvar versionString:
        The string associated with the component, for instance, 2.0 if there's a
        line like VERSION:2.0, an empty string otherwise.
    @cvar knownChildren:
        A dictionary with uppercased component/property names as keys and a
        tuple (min, max, id) as value, where id is the id used by
        L{registerBehavior}, min and max are the limits on how many of this child
        must occur.  None is used to denote no max or no id.
    @cvar quotedPrintable:
        A boolean describing whether the object should be encoded and decoded
        using quoted printable line folding and character escaping.
    @cvar defaultBehavior:
        Behavior to apply to ContentLine children when no behavior is found.
    @cvar hasNative:
        A boolean describing whether the object can be transformed into a more
        Pythonic object.
    @cvar isComponent:
        A boolean, True if the object should be a Component.
    @cvar sortFirst:
        The lower-case list of children which should come first when sorting.
    @cvar allowGroup:
        Whether or not vCard style group prefixes are allowed.
    """

    name: str
    description: str
    versionString: str
    knownChildren: ClassVar[dict[str, tuple[int, int | None, int | None]]]
    quotedPrintable: bool
    defaultBehavior: Incomplete
    hasNative: bool
    isComponent: bool
    allowGroup: bool
    forceUTC: bool
    sortFirst: Incomplete
    @classmethod
    def validate(cls, obj, raiseException: bool = False, complainUnrecognized: bool = False) -> bool:
        """Check if the object satisfies this behavior's requirements.

        @param obj:
            The L{ContentLine<base.ContentLine>} or
            L{Component<base.Component>} to be validated.
        @param raiseException:
            If True, raise a L{base.ValidateError} on validation failure.
            Otherwise return a boolean.
        @param complainUnrecognized:
            If True, fail to validate if an uncrecognized parameter or child is
            found.  Otherwise log the lack of recognition.

        """

    @classmethod
    def lineValidate(cls, line, raiseException, complainUnrecognized):
        """Examine a line's parameters and values, return True if valid."""

    @classmethod
    def decode(cls, line) -> None: ...
    @classmethod
    def encode(cls, line) -> None: ...
    @classmethod
    def transformToNative(cls, obj):
        """
        Turn a ContentLine or Component into a Python-native representation.

        If appropriate, turn dates or datetime strings into Python objects.
        Components containing VTIMEZONEs turn into VtimezoneComponents.

        """

    @classmethod
    def transformFromNative(cls, obj) -> None:
        """
        Inverse of transformToNative.
        """

    @classmethod
    def generateImplicitParameters(cls, obj) -> None:
        """Generate any required information that don't yet exist."""

    @classmethod
    def serialize(cls, obj, buf, lineLength, validate: bool = True, *args, **kwargs):
        """
        Set implicit parameters, do encoding, return unicode string.

        If validate is True, raise VObjectError if the line doesn't validate
        after implicit parameters are generated.

        Default is to call base.defaultSerialize.

        """

    @classmethod
    def valueRepr(cls, line):
        """return the representation of the given content line value"""
