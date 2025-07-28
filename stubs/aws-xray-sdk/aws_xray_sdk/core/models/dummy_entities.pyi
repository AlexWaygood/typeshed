from .segment import Segment
from .subsegment import Subsegment

class DummySegment(Segment):
    """
    A dummy segment is created when ``xray_recorder`` decide to not sample
    the segment based on sampling rules.
    Adding data to a dummy segment becomes a no-op except for
    subsegments. This is to reduce the memory footprint of the SDK.
    A dummy segment will not be sent to the X-Ray daemon. Manually creating
    dummy segments is not recommended.
    """

    def __init__(self, name: str = "dummy") -> None: ...

class DummySubsegment(Subsegment):
    """
    A dummy subsegment will be created when ``xray_recorder`` tries
    to create a subsegment under a not sampled segment. Adding data
    to a dummy subsegment becomes no-op. Dummy subsegment will not
    be sent to the X-Ray daemon.
    """

    def __init__(self, segment, name: str = "dummy") -> None: ...
