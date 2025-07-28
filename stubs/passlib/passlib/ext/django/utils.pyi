"""passlib.ext.django.utils - helper functions used by this plugin"""

from typing import Any

__all__ = ["DJANGO_VERSION", "MIN_DJANGO_VERSION", "get_preset_config", "quirks"]

DJANGO_VERSION: tuple[Any, ...]
MIN_DJANGO_VERSION: tuple[int, int]

class quirks:
    none_causes_check_password_error: Any
    empty_is_usable_password: Any
    invalid_is_usable_password: Any

def get_preset_config(name):
    """Returns configuration string for one of the preset strings
    supported by the ``PASSLIB_CONFIG`` setting.
    Currently supported presets:

    * ``"passlib-default"`` - default config used by this release of passlib.
    * ``"django-default"`` - config matching currently installed django version.
    * ``"django-latest"`` - config matching newest django version (currently same as ``"django-1.6"``).
    * ``"django-1.0"`` - config used by stock Django 1.0 - 1.3 installs
    * ``"django-1.4"`` - config used by stock Django 1.4 installs
    * ``"django-1.6"`` - config used by stock Django 1.6 installs
    """

class DjangoTranslator:
    """
    Object which helps translate passlib hasher objects / names
    to and from django hasher objects / names.

    These methods are wrapped in a class so that results can be cached,
    but with the ability to have independant caches, since django hasher
    names may / may not correspond to the same instance (or even class).
    """

    context: Any
    def __init__(self, context=None, **kwds) -> None: ...
    def reset_hashers(self) -> None: ...
    def passlib_to_django_name(self, passlib_name):
        """
        Convert passlib hasher / name to Django hasher name.
        """

    def passlib_to_django(self, passlib_hasher, cached: bool = True):
        """
        Convert passlib hasher / name to Django hasher.

        :param passlib_hasher:
            passlib hasher / name

        :returns:
            django hasher instance
        """

    def django_to_passlib_name(self, django_name):
        """
        Convert Django hasher / name to Passlib hasher name.
        """

    def django_to_passlib(self, django_name, cached: bool = True):
        """
        Convert Django hasher / name to Passlib hasher / name.
        If present, CryptContext will be checked instead of main registry.

        :param django_name:
            Django hasher class or algorithm name.
            "default" allowed if context provided.

        :raises ValueError:
            if can't resolve hasher.

        :returns:
            passlib hasher or name
        """

    def resolve_django_hasher(self, django_name, cached: bool = True):
        """
        Take in a django algorithm name, return django hasher.
        """

class DjangoContextAdapter(DjangoTranslator):
    """
    Object which tries to adapt a Passlib CryptContext object,
    using a Django-hasher compatible API.

    When installed in django, :mod:`!passlib.ext.django` will create
    an instance of this class, and then monkeypatch the appropriate
    methods into :mod:`!django.contrib.auth` and other appropriate places.
    """

    context: Any
    is_password_usable: Any
    enabled: bool
    patched: bool
    log: Any
    def __init__(self, context=None, get_user_category=None, **kwds) -> None: ...
    def reset_hashers(self) -> None:
        """
        Wrapper to manually reset django's hasher lookup cache
        """

    def get_hashers(self):
        """
        Passlib replacement for get_hashers() --
        Return list of available django hasher classes
        """

    def get_hasher(self, algorithm: str = "default"):
        """
        Passlib replacement for get_hasher() --
        Return django hasher by name
        """

    def identify_hasher(self, encoded):
        """
        Passlib replacement for identify_hasher() --
        Identify django hasher based on hash.
        """

    def make_password(self, password, salt=None, hasher: str = "default"):
        """
        Passlib replacement for make_password()
        """

    def check_password(self, password, encoded, setter=None, preferred: str = "default"):
        """
        Passlib replacement for check_password()
        """

    def user_check_password(self, user, password):
        """
        Passlib replacement for User.check_password()
        """

    def user_set_password(self, user, password) -> None:
        """
        Passlib replacement for User.set_password()
        """

    def get_user_category(self, user):
        """
        Helper for hashing passwords per-user --
        figure out the CryptContext category for specified Django user object.
        .. note::
            This may be overridden via PASSLIB_GET_CATEGORY django setting
        """
    HASHERS_PATH: str
    MODELS_PATH: str
    USER_CLASS_PATH: Any
    FORMS_PATH: str
    patch_locations: Any
    def install_patch(self):
        """
        Install monkeypatch to replace django hasher framework.
        """

    def remove_patch(self):
        """
        Remove monkeypatch from django hasher framework.
        As precaution in case there are lingering refs to context,
        context object will be wiped.

        .. warning::
            This may cause problems if any other Django modules have imported
            their own copies of the patched functions, though the patched
            code has been designed to throw an error as soon as possible in
            this case.
        """

    def load_model(self) -> None:
        """
        Load configuration from django, and install patch.
        """

class ProxyProperty:
    """helper that proxies another attribute"""

    attr: Any
    def __init__(self, attr) -> None: ...
    def __get__(self, obj, cls): ...
    def __set__(self, obj, value) -> None: ...
    def __delete__(self, obj) -> None: ...
