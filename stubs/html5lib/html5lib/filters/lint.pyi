from . import base

spaceCharacters: str

class Filter(base.Filter):
    """Lints the token stream for errors

    If it finds any errors, it'll raise an ``AssertionError``.

    """

    require_matching_tags: bool
    def __init__(self, source, require_matching_tags: bool = True) -> None:
        """Creates a Filter

        :arg source: the source token stream

        :arg require_matching_tags: whether or not to require matching tags

        """

    def __iter__(self): ...
