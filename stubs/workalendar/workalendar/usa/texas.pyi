"""
Texas module
============

This module presents two classes to handle the way state holidays are managed
in Texas.

The :class:`TexasBase` class gathers all available holidays for Texas,
according to this document:
http://www.statutes.legis.state.tx.us/Docs/GV/htm/GV.662.htm

The :class:`Texas` class includes all national and state holidays, as described
in the said document. This should be the "default" Texas calendar class, to be
used in most cases.

But if state holidays are supposed to be observed by most of the workforces,
any employee can chose to skip one of these days and replace it by another.

If at some point you need to create a specific calendar class based on Texas
calendar, you can either use the :class:`TexasBase` class or directly the
:class:`Texas` class and overwrite/override the :method:`get_fixed_holidays()`
and/or :method:`get_variable_days()` to fit your needs.

Example:

.. code::

    class TexasCustom(TexasBase):
        # This will include the confederate heroes day
        texas_include_confederate_heroes = True

        FIXED_HOLIDAYS = TexasBase.FIXED_HOLIDAYS + (
            (7, 14, "Bastille Day!"),
        )

        def get_variable_days(self, year):
            days = super().get_variable_days(year)
            days.append(
                (self.get_nth_weekday_in_month(year, 1, 15), "Special Day")
            )
            return days

"""

from typing import ClassVar

from .core import UnitedStates

class TexasBase(UnitedStates):
    """Texas Base (w/o State holidays)"""

    include_columbus_day: ClassVar[bool]
    texas_include_confederate_heroes: ClassVar[bool]
    texas_include_independance_day: ClassVar[bool]
    texas_san_jacinto_day: ClassVar[bool]
    texas_emancipation_day: ClassVar[bool]
    texas_lyndon_johnson_day: ClassVar[bool]
    include_thanksgiving_friday: ClassVar[bool]
    include_christmas_eve: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    def get_fixed_holidays(self, year): ...

class Texas(TexasBase):
    """Texas"""

    texas_include_confederate_heroes: ClassVar[bool]
    texas_include_independance_day: ClassVar[bool]
    texas_san_jacinto_day: ClassVar[bool]
    texas_emancipation_day: ClassVar[bool]
    texas_lyndon_johnson_day: ClassVar[bool]
    include_thanksgiving_friday: ClassVar[bool]
    include_christmas_eve: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
