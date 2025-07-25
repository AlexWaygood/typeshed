import re
from typing import Final, overload

from aws_xray_sdk.core.models.trace_header import TraceHeader

first_cap_re: Final[re.Pattern[str]]
all_cap_re: Final[re.Pattern[str]]
UNKNOWN_HOSTNAME: str = "UNKNOWN HOST"

def inject_trace_header(headers, entity) -> None:
    """
    Extract trace id, entity id and sampling decision
    from the input entity and inject these information
    to headers.

    :param dict headers: http headers to inject
    :param Entity entity: trace entity that the trace header
        value generated from.
    """

def calculate_sampling_decision(trace_header, recorder, sampling_req):
    """
    Return 1 or the matched rule name if should sample and 0 if should not.
    The sampling decision coming from ``trace_header`` always has
    the highest precedence. If the ``trace_header`` doesn't contain
    sampling decision then it checks if sampling is enabled or not
    in the recorder. If not enbaled it returns 1. Otherwise it uses user
    defined sampling rules to decide.
    """

def construct_xray_header(headers) -> TraceHeader:
    """
    Construct a ``TraceHeader`` object from dictionary headers
    of the incoming request. This method should always return
    a ``TraceHeader`` object regardless of tracing header's presence
    in the incoming request.
    """

def calculate_segment_name(host_name, recorder):
    """
    Returns the segment name based on recorder configuration and
    input host name. This is a helper generally used in web framework
    middleware where a host name is available from incoming request's headers.
    """

def prepare_response_header(origin_header, segment) -> str:
    """
    Prepare a trace header to be inserted into response
    based on original header and the request segment.
    """

def to_snake_case(name: str) -> str:
    """
    Convert the input string to snake-cased string.
    """

def strip_url(url):
    """
    Will generate a valid url string for use as a segment name
    :param url: url to strip
    :return: validated url string
    """

@overload
def get_hostname(url: str | None) -> str: ...
@overload
def get_hostname(url: bytes | bytearray | None) -> str | bytes: ...
def unwrap(obj: object, attr: str) -> None:
    """
    Will unwrap a `wrapt` attribute
    :param obj: base object
    :param attr: attribute on `obj` to unwrap
    """
