from dataclasses import dataclass

from seaborn._marks.base import MappableColor, MappableFloat, MappableString, Mark, document_properties

@document_properties
@dataclass
class Text(Mark):
    """
    A textual mark to annotate or represent data values.

        This mark defines the following properties:
            |text|, |color|, |alpha|, |fontsize|, |halign|, |valign|, |offset|

    Examples
    --------
    .. include:: ../docstrings/objects.Text.rst

    """

    text: MappableString = ...
    color: MappableColor = ...
    alpha: MappableFloat = ...
    fontsize: MappableFloat = ...
    halign: MappableString = ...
    valign: MappableString = ...
    offset: MappableFloat = ...
