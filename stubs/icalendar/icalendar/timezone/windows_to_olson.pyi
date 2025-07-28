"""This module contains mappings from Windows timezone identifiers to
Olson timezone identifiers.

The data is taken from the unicode consortium [0], the proposal and rationale
for this mapping is also available at the unicode consortium [1].


[0] https://www.unicode.org/cldr/cldr-aux/charts/29/supplemental/zone_tzid.html
[1] https://cldr.unicode.org/development/development-process/design-proposals/extended-windows-olson-zid-mapping  # noqa
"""

from typing import Final

WINDOWS_TO_OLSON: Final[dict[str, str]]
