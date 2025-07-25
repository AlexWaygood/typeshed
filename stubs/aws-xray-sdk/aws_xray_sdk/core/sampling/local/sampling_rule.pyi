from typing import ClassVar, TypedDict, type_check_only
from typing_extensions import NotRequired

from .reservoir import Reservoir

@type_check_only
class _Rule(TypedDict):
    description: NotRequired[str]
    host: NotRequired[str]
    service_name: NotRequired[str]
    http_method: NotRequired[str]
    url_path: NotRequired[str]
    fixed_target: NotRequired[int]
    rate: NotRequired[float]

class SamplingRule:
    """
    One SamolingRule represents one rule defined from local rule json file
    or from a dictionary. It can be either a custom rule or default rule.
    """

    FIXED_TARGET: ClassVar[str]
    RATE: ClassVar[str]
    HOST: ClassVar[str]
    METHOD: ClassVar[str]
    PATH: ClassVar[str]
    SERVICE_NAME: ClassVar[str]
    def __init__(self, rule_dict: _Rule, version: int = 2, default: bool = False) -> None:
        """
        :param dict rule_dict: The dictionary that defines a single rule.
        :param bool default: Indicates if this is the default rule. A default
            rule cannot have `host`, `http_method` or `url_path`.
        """

    def applies(self, host: str | None, method: str | None, path: str | None) -> bool:
        """
        Determines whether or not this sampling rule applies to
        the incoming request based on some of the request's parameters.
        Any None parameters provided will be considered an implicit match.
        """

    @property
    def fixed_target(self) -> int | None:
        """
        Defines fixed number of sampled segments per second.
        This doesn't count for sampling rate.
        """

    @property
    def rate(self) -> float | None:
        """
        A float number less than 1.0 defines the sampling rate.
        """

    @property
    def host(self) -> str | None:
        """
        The host name of the reqest to sample.
        """

    @property
    def method(self) -> str | None:
        """
        HTTP method of the request to sample.
        """

    @property
    def path(self) -> str | None:
        """
        The url path of the request to sample.
        """

    @property
    def reservoir(self) -> Reservoir:
        """
        Keeps track of used sampled targets within the second.
        """

    @property
    def version(self):
        """
        Keeps track of used sampled targets within the second.
        """
