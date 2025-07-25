from _typeshed import Incomplete
from logging import Logger
from typing import Final, Literal
from typing_extensions import Self, TypeAlias

_SampledTrue: TypeAlias = Literal[True, "1", 1]
_SampledFalse: TypeAlias = Literal[False, "0", 0]
_SampledUnknown: TypeAlias = Literal["?"]
_Sampled: TypeAlias = _SampledTrue | _SampledFalse | _SampledUnknown

log: Logger
ROOT: Final = "Root"
PARENT: Final = "Parent"
SAMPLE: Final = "Sampled"
SELF: Final = "Self"
HEADER_DELIMITER: Final = ";"

class TraceHeader:
    """
    The sampling decision and trace ID are added to HTTP requests in
    tracing headers named ``X-Amzn-Trace-Id``. The first X-Ray-integrated
    service that the request hits adds a tracing header, which is read
    by the X-Ray SDK and included in the response. Learn more about
    `Tracing Header <http://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html#xray-concepts-tracingheader>`_.
    """

    def __init__(
        self,
        root: str | None = None,
        parent: str | None = None,
        sampled: _Sampled | None = None,
        data: dict[str, Incomplete] | None = None,
    ) -> None:
        """
        :param str root: trace id
        :param str parent: parent id
        :param int sampled: 0 means not sampled, 1 means sampled
        :param dict data: arbitrary data fields
        """

    @classmethod
    def from_header_str(cls, header: str | None) -> Self:
        """
        Create a TraceHeader object from a tracing header string
        extracted from a http request headers.
        """

    def to_header_str(self) -> str:
        """
        Convert to a tracing header string that can be injected to
        outgoing http request headers.
        """

    @property
    def root(self) -> str | None:
        """
        Return trace id of the header
        """

    @property
    def parent(self) -> str | None:
        """
        Return the parent segment id in the header
        """

    @property
    def sampled(self) -> Literal[1, 0, "?"] | None:
        """
        Return the sampling decision in the header.
        It's 0 or 1 or '?'.
        """

    @property
    def data(self) -> dict[str, Incomplete]:
        """
        Return the arbitrary fields in the trace header.
        """
