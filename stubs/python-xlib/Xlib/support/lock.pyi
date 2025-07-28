from collections.abc import Callable

class _DummyLock:
    acquire: Callable[..., None]
    release: Callable[..., None]
    locked: Callable[..., None]

def allocate_lock() -> _DummyLock:
    """Create a new lock object. See help(type(threading.Lock())) for
    information about locks.
    """
