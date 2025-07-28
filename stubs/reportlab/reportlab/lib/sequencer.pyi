"""A Sequencer class counts things. It aids numbering and formatting lists."""

__all__ = ["Sequencer", "getSequencer", "setSequencer"]

class _Counter:
    """Private class used by Sequencer.  Each counter
    knows its format, and the IDs of anything it
    resets, as well as its value. Starts at zero
    and increments just before you get the new value,
    so that it is still 'Chapter 5' and not 'Chapter 6'
    when you print 'Figure 5.1'
    """

    def __init__(self) -> None: ...
    def setFormatter(self, formatFunc) -> None: ...
    def reset(self, value=None) -> None: ...
    def next(self): ...
    __next__ = next
    def nextf(self):
        """Returns next value formatted"""

    def thisf(self): ...
    def chain(self, otherCounter) -> None: ...

class Sequencer:
    """Something to make it easy to number paragraphs, sections,
    images and anything else.  The features include registering
    new string formats for sequences, and 'chains' whereby
    some counters are reset when their parents.
    It keeps track of a number of
    'counters', which are created on request:
    Usage::

        >>> seq = layout.Sequencer()
        >>> seq.next('Bullets')
        1
        >>> seq.next('Bullets')
        2
        >>> seq.next('Bullets')
        3
        >>> seq.reset('Bullets')
        >>> seq.next('Bullets')
        1
        >>> seq.next('Figures')
        1
        >>>
    """

    def __init__(self) -> None: ...
    def __next__(self):
        """Retrieves the numeric value for the given counter, then
        increments it by one.  New counters start at one.
        """

    def next(self, counter=None): ...
    def thisf(self, counter=None): ...
    def nextf(self, counter=None):
        """Retrieves the numeric value for the given counter, then
        increments it by one.  New counters start at one.
        """

    def setDefaultCounter(self, default=None) -> None:
        """Changes the key used for the default"""

    def registerFormat(self, format, func) -> None:
        """Registers a new formatting function.  The funtion
        must take a number as argument and return a string;
        fmt is a short menmonic string used to access it.
        """

    def setFormat(self, counter, format) -> None:
        """Specifies that the given counter should use
        the given format henceforth.
        """

    def reset(self, counter=None, base: int = 0) -> None: ...
    def chain(self, parent, child) -> None: ...
    def __getitem__(self, key):
        """Allows compact notation to support the format function.
        s['key'] gets current value, s['key+'] increments.
        """

    def format(self, template):
        """The crowning jewels - formats multi-level lists."""

    def dump(self) -> None:
        """Write current state to stdout for diagnostics"""

def getSequencer(): ...
def setSequencer(seq): ...
