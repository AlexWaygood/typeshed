from typing import Final

httplib_client_module: Final = "http.client"
PATCH_FLAG: Final = "__xray_patched"

def add_ignored(subclass=None, hostname=None, urls=None) -> None: ...
def reset_ignored() -> None: ...
def http_response_processor(wrapped, instance, args, kwargs, return_value, exception, subsegment, stack) -> None: ...
def http_send_request_processor(wrapped, instance, args, kwargs, return_value, exception, subsegment, stack) -> None: ...
def http_read_processor(wrapped, instance, args, kwargs, return_value, exception, subsegment, stack) -> None: ...
def patch() -> None:
    """
    patch the built-in `urllib/httplib/httplib.client` methods for tracing.
    """

def unpatch() -> None:
    """
    Unpatch any previously patched modules.
    This operation is idempotent.
    """
