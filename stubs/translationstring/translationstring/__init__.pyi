from collections.abc import Callable
from gettext import NullTranslations
from typing import Any, Protocol
from typing_extensions import Self

class _TranslationStringFactory(Protocol):
    def __call__(
        self,
        msgid: str | TranslationString,
        mapping: dict[str, Any] | None = ...,
        default: str | None = ...,
        context: str | None = ...,
    ) -> TranslationString: ...

class _ChameleonTranslate(Protocol):
    def __call__(
        self,
        msgid: str | TranslationString,
        mapping: dict[str, Any] | None = ...,
        context: str | None = ...,
        target_language: str | None = ...,
        default: str | None = ...,
    ) -> TranslationString: ...

class _TranslatorPolicy(Protocol):
    def __call__(self, translations: NullTranslations, tstring: str, domain: str | None, context: str | None) -> str: ...

class _Translator(Protocol):
    def __call__(
        self,
        tstring: str | TranslationString,
        domain: str | None = None,
        mapping: dict[str, Any] | None = None,
        context: str | None = None,
    ) -> str: ...

class _PluralizerPolicy(Protocol):
    def __call__(
        self, translations: NullTranslations, singular: str, plural: str, n: int, domain: str | None, context: str | None
    ) -> str: ...

class _Pluralizer(Protocol):
    def __call__(
        self,
        singular: str | TranslationString,
        plural: str | TranslationString,
        n: int,
        domain: str | None = None,
        mapping: dict[str, Any] | None = None,
        context: str | None = None,
    ) -> str: ...

class TranslationString(str):
    """
    The constructor for a :term:`translation string`.  A translation
    string is a Unicode-like object that has some extra metadata.

    This constructor accepts one required argument named ``msgid``.
    ``msgid`` must be the :term:`message identifier` for the
    translation string.  It must be a ``unicode`` object or a ``str``
    object encoded in the default system encoding.

    Optional keyword arguments to this object's constructor include
    ``domain``, ``default``, and ``mapping``.

    ``domain`` represents the :term:`translation domain`.  By default,
    the translation domain is ``None``, indicating that this
    translation string is associated with the default translation
    domain (usually ``messages``).

    ``default`` represents an explicit *default text* for this
    translation string.  Default text appears when the translation
    string cannot be translated.  Usually, the ``msgid`` of a
    translation string serves double duty as its default text.
    However, using this option you can provide a different default
    text for this translation string.  This feature is useful when the
    default of a translation string is too complicated or too long to
    be used as a message identifier. If ``default`` is provided, it
    must be a ``unicode`` object or a ``str`` object encoded in the
    default system encoding (usually means ASCII).  If ``default`` is
    ``None`` (its default value), the ``msgid`` value used by this
    translation string will be assumed to be the value of ``default``.

    ``mapping``, if supplied, must be a dictionary-like object which
    represents the replacement values for any :term:`translation
    string` *replacement marker* instances found within the ``msgid``
    (or ``default``) value of this translation string.

    ``context`` represents the :term:`translation context`.  By default,
    the translation context is ``None``.

    After a translation string is constructed, it behaves like most
    other ``unicode`` objects; its ``msgid`` value will be displayed
    when it is treated like a ``unicode`` object.  Only when its
    ``ugettext`` method is called will it be translated.

    Its default value is available as the ``default`` attribute of the
    object, its :term:`translation domain` is available as the
    ``domain`` attribute, and the ``mapping`` is available as the
    ``mapping`` attribute.  The object otherwise behaves much like a
    Unicode string.
    """

    domain: str | None
    context: str | None
    default: str
    mapping: dict[str, Any] | None
    def __new__(
        self,
        msgid: str | Self,
        domain: str | None = None,
        default: str | None = None,
        mapping: dict[str, Any] | None = None,
        context: str | None = None,
    ) -> Self: ...
    def __mod__(self, options: dict[str, Any]) -> TranslationString:  # type: ignore[override]
        """Create a new TranslationString instance with an updated mapping.
        This makes it possible to use the standard python %-style string
        formatting with translatable strings. Only dictionary
        arguments are supported.
        """

    def interpolate(self, translated: str | None = None) -> str:
        """Interpolate the value ``translated`` which is assumed to
        be a Unicode object containing zero or more *replacement
        markers* (``$foo`` or ``${bar}``) using the ``mapping``
        dictionary attached to this instance.  If the ``mapping``
        dictionary is empty or ``None``, no interpolation is
        performed.

        If ``translated`` is ``None``, interpolation will be performed
        against the ``default`` value.
        """

    def __reduce__(self) -> tuple[type[Self], tuple[str, str | None, str, dict[str, Any], str | None]]: ...

def TranslationStringFactory(factory_domain: str) -> _TranslationStringFactory:
    """Create a factory which will generate translation strings
    without requiring that each call to the factory be passed a
    ``domain`` value.  A single argument is passed to this class'
    constructor: ``domain``.  This value will be used as the
    ``domain`` values of :class:`translationstring.TranslationString`
    objects generated by the ``__call__`` of this class.  The
    ``msgid``, ``mapping``, and ``default`` values provided to the
    ``__call__`` method of an instance of this class have the meaning
    as described by the constructor of the
    :class:`translationstring.TranslationString`
    """

def ChameleonTranslate(translator: Callable[[TranslationString], str] | None) -> _ChameleonTranslate:
    """
    When necessary, use the result of calling this function as a
    Chameleon template 'translate' function (e.g. the ``translate``
    argument to the ``chameleon.zpt.template.PageTemplate``
    constructor) to allow our translation machinery to drive template
    translation.  A single required argument ``translator`` is
    passsed.  The ``translator`` provided should be a callable which
    accepts a single argument ``translation_string`` ( a
    :class:`translationstring.TranslationString` instance) which
    returns a ``unicode`` object as a translation.  ``translator`` may
    also optionally be ``None``, in which case no translation is
    performed (the ``msgid`` or ``default`` value is returned
    untranslated).
    """

def ugettext_policy(translations: NullTranslations, tstring: str, domain: str | None, context: str | None) -> str:
    """A translator policy function which unconditionally uses the
    ``ugettext`` API on the translations object.
    """

def dugettext_policy(translations: NullTranslations, tstring: str, domain: str | None, context: str | None) -> str:
    """A translator policy function which assumes the use of a
    :class:`babel.support.Translations` translations object, which
    supports the dugettext API; fall back to ugettext.
    """

def Translator(translations: NullTranslations | None = None, policy: _TranslatorPolicy | None = None) -> _Translator:
    """
    Return a translator object based on the ``translations`` and
    ``policy`` provided.  ``translations`` should be an object
    supporting *at least* the Python :class:`gettext.NullTranslations`
    API but ideally the :class:`babel.support.Translations` API, which
    has support for domain lookups like dugettext.

    ``policy`` should be a callable which accepts three arguments:
    ``translations``, ``tstring`` and ``domain``.  It must perform the
    actual translation lookup.  If ``policy`` is ``None``, the
    :func:`translationstring.dugettext_policy` policy will be used.

    The callable returned accepts three arguments: ``tstring``
    (required), ``domain`` (optional) and ``mapping`` (optional).
    When called, it will translate the ``tstring`` translation string
    to a ``unicode`` object using the ``translations`` provided.  If
    ``translations`` is ``None``, the result of interpolation of the
    default value is returned.  The optional ``domain`` argument can
    be used to specify or override the domain of the ``tstring``
    (useful when ``tstring`` is a normal string rather than a
    translation string).  The optional ``mapping`` argument can
    specify or override the ``tstring`` interpolation mapping, useful
    when the ``tstring`` argument is a simple string instead of a
    translation string.
    """

def ungettext_policy(
    translations: NullTranslations, singular: str, plural: str, n: int, domain: str | None, context: str | None
) -> str:
    """A pluralizer policy function which unconditionally uses the
    ``ungettext`` API on the translations object.
    """

def dungettext_policy(
    translations: NullTranslations, singular: str, plural: str, n: int, domain: str | None, context: str | None
) -> str:
    """A pluralizer policy function which assumes the use of the
    :class:`babel.support.Translations` class, which supports the
    dungettext API; falls back to ungettext.
    """

def Pluralizer(translations: NullTranslations | None = None, policy: _PluralizerPolicy | None = None) -> _Pluralizer:
    """
    Return a pluralizer object based on the ``translations`` and
    ``policy`` provided.  ``translations`` should be an object
    supporting *at least* the Python :class:`gettext.NullTranslations`
    API but ideally the :class:`babel.support.Translations` API, which
    has support for domain lookups like dugettext.

    ``policy`` should be a callable which accepts five arguments:
    ``translations``, ``singular`` and ``plural``, ``n`` and
    ``domain``.  It must perform the actual pluralization lookup.  If
    ``policy`` is ``None``, the
    :func:`translationstring.dungettext_policy` policy will be used.

    The object returned will be a callable which has the following
    signature::

        def pluralizer(singular, plural, n, domain=None, mapping=None):
            ...

    The ``singular`` and ``plural`` objects passed may be translation
    strings or unicode strings.  ``n`` represents the number of
    elements.  ``domain`` is the translation domain to use to do the
    pluralization, and ``mapping`` is the interpolation mapping that
    should be used on the result.  Note that if the objects passed are
    translation strings, their domains and mappings are ignored.  The
    domain and mapping arguments must be used instead.  If the ``domain`` is
    not supplied, a default domain is used (usually ``messages``).
    """
