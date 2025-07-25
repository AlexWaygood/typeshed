def configure() -> None:
    """
    Configure logging to emit warning and above to stderr
    and everything else to stdout. This behavior is provided
    for compatibility with distutils.log but may change in
    the future.
    """

def set_threshold(level: int) -> int: ...
