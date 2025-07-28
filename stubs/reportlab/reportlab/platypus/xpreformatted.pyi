"""A 'rich preformatted text' widget allowing internal markup"""

from reportlab.lib.styles import PropertySet
from reportlab.platypus.paragraph import Paragraph, ParaLines
from reportlab.platypus.paraparser import ParaFrag

class XPreformatted(Paragraph):
    def __init__(
        self,
        text: str,
        # NOTE: This should be a ParagraphStyle
        style: PropertySet,
        bulletText: str | None = None,
        frags: list[ParaFrag] | None = None,
        caseSensitive: int = 1,
        dedent: int = 0,
    ) -> None: ...
    def breakLinesCJK(self, width: float | list[float] | tuple[float, ...]) -> ParaLines | ParaFrag:
        """
        Returns a broken line structure. There are two cases

        A) For the simple case of a single formatting input fragment the output is
            A fragment specifier with
                - kind = 0
                - fontName, fontSize, leading, textColor
                - lines=  A list of lines

                    Each line has two items:

                    1. unused width in points
                    2. a list of words

        B) When there is more than one input formatting fragment the out put is
            A fragment specifier with
                - kind = 1
                - lines =  A list of fragments each having fields:

                    - extraspace (needed for justified)
                    - fontSize
                    - words=word list
                    - each word is itself a fragment with
                    - various settings

        This structure can be used to easily draw paragraphs with the various alignments.
        You can supply either a single width or a list of widths; the latter will have its
        last item repeated until necessary. A 2-element list is useful when there is a
        different first line indent; a longer list could be created to facilitate custom wraps
        around irregular objects.
        """

class PythonPreformatted(XPreformatted):
    """Used for syntax-colored Python code, otherwise like XPreformatted."""

    formats: dict[str, tuple[str, str]]
    def __init__(
        self,
        text: str,
        # NOTE: This should be a ParagraphStyle
        style: PropertySet,
        bulletText: str | None = None,
        dedent: int = 0,
        frags: list[ParaFrag] | None = None,
    ) -> None: ...
    def escapeHtml(self, text: str) -> str: ...
    def fontify(self, code: str) -> str:
        """Return a fontified version of some Python code."""

__all__ = ("XPreformatted", "PythonPreformatted")
