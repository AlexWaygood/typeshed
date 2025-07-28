"""
Cooperative ``subprocess`` module.

.. caution:: On POSIX platforms, this module is not usable from native
   threads other than the main thread; attempting to do so will raise
   a :exc:`TypeError`. This module depends on libev's fork watchers.
   On POSIX systems, fork watchers are implemented using signals, and
   the thread to which process-directed signals are delivered `is not
   defined`_. Because each native thread has its own gevent/libev
   loop, this means that a fork watcher registered with one loop
   (thread) may never see the signal about a child it spawned if the
   signal is sent to a different thread.

.. note:: The interface of this module is intended to match that of
   the standard library :mod:`subprocess` module (with many backwards
   compatible extensions from Python 3 backported to Python 2). There
   are some small differences between the Python 2 and Python 3
   versions of that module (the Python 2 ``TimeoutExpired`` exception,
   notably, extends ``Timeout`` and there is no ``SubprocessError``) and between the
   POSIX and Windows versions. The HTML documentation here can only
   describe one version; for definitive documentation, see the
   standard library or the source code.

.. _is not defined: http://www.linuxprogrammingblog.com/all-about-linux-signals?page=11

Be sure to see important notes in :func:`gevent.monkey.patch_subprocess`.
"""

from subprocess import *

# this is another module we decide to just punt on and trust that gevent's implementation
# at the very least satisfies the stdlib interface.
