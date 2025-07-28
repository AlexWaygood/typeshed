"""
The standard library :mod:`time` module, but :func:`sleep` is
gevent-aware.

.. versionadded:: 1.3a2
"""

from gevent.hub import sleep as sleep

__all__ = ["sleep"]
