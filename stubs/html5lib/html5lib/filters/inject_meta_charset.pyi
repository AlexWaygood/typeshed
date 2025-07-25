from . import base

class Filter(base.Filter):
    """Injects ``<meta charset=ENCODING>`` tag into head of document"""

    encoding: str | None
    def __init__(self, source, encoding: str | None) -> None:
        """Creates a Filter

        :arg source: the source token stream

        :arg encoding: the encoding to set

        """

    def __iter__(self): ...
