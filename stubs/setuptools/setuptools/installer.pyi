from importlib import metadata
from typing import Any
from typing_extensions import deprecated

@deprecated(
    """
    `setuptools.installer` and `fetch_build_eggs` are deprecated.
    Requirements should be satisfied by a PEP 517 installer.
    If you are using pip, you can try `pip install --use-pep517`.
    """
)
def fetch_build_egg(dist, req) -> metadata.Distribution | metadata.PathDistribution:
    """Fetch an egg needed for building.

    Use pip/wheel to fetch/build a wheel.
    """

# Returns packaging.requirements.Requirement
# But since this module is deprecated, we avoid declaring a dependency on packaging
def strip_marker(req) -> Any:
    """
    Return a new requirement without the environment marker to avoid
    calling pip with something like `babel; extra == "i18n"`, which
    would always be ignored.
    """
