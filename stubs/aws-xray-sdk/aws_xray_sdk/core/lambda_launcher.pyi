from logging import Logger

from .context import Context

log: Logger
LAMBDA_TRACE_HEADER_KEY: str
LAMBDA_TASK_ROOT_KEY: str
TOUCH_FILE_DIR: str
TOUCH_FILE_PATH: str

def check_in_lambda():
    """
    Return None if SDK is not loaded in AWS Lambda worker.
    Otherwise drop a touch file and return a lambda context.
    """

class LambdaContext(Context):
    """
    Lambda service will generate a segment for each function invocation which
    cannot be mutated. The context doesn't keep any manually created segment
    but instead every time ``get_trace_entity()`` gets called it refresh the
    segment based on environment variables set by Lambda worker.
    """

    def __init__(self) -> None: ...
    def put_segment(self, segment) -> None:
        """
        No-op.
        """

    def end_segment(self, end_time=None) -> None:
        """
        No-op.
        """

    def put_subsegment(self, subsegment) -> None:
        """
        Refresh the segment every time this function is invoked to prevent
        a new subsegment from being attached to a leaked segment/subsegment.
        """

    def get_trace_entity(self): ...
    @property
    def context_missing(self) -> None: ...
    @context_missing.setter
    def context_missing(self, value) -> None: ...
    def handle_context_missing(self) -> None:
        """
        No-op.
        """
