"""Provide basic warnings used by setuptools modules.

Using custom classes (other than ``UserWarning``) allow users to set
``PYTHONWARNINGS`` filters to run tests and prepare for upcoming changes in
setuptools.
"""

from typing_extensions import TypeAlias

_DueDate: TypeAlias = tuple[int, int, int]  # time tuple

class SetuptoolsWarning(UserWarning):
    """Base class in ``setuptools`` warning hierarchy."""

    @classmethod
    def emit(
        cls,
        summary: str | None = None,
        details: str | None = None,
        due_date: _DueDate | None = None,
        see_docs: str | None = None,
        see_url: str | None = None,
        stacklevel: int = 2,
        **kwargs,
    ) -> None:
        """Private: reserved for ``setuptools`` internal use only"""

class InformationOnly(SetuptoolsWarning):
    """Currently there is no clear way of displaying messages to the users
    that use the setuptools backend directly via ``pip``.
    The only thing that might work is a warning, although it is not the
    most appropriate tool for the job...

    See pypa/packaging-problems#558.
    """

class SetuptoolsDeprecationWarning(SetuptoolsWarning):
    """
    Base class for warning deprecations in ``setuptools``

    This class is not derived from ``DeprecationWarning``, and as such is
    visible by default.
    """
