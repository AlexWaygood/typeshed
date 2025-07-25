"""
Virginia module

You may or may want not to treat the Day before Thanksgiving as a non-working
day by implementing the following class:

.. code::

    from workalenda.usa import Virginia as VirginiaBase

    class Virginia(VirginiaBase):
        include_thanksgiving_wednesday = False

"""

from typing import ClassVar

from .core import UnitedStates

class Virginia(UnitedStates):
    """Virginia"""

    include_christmas_eve: ClassVar[bool]
    include_thanksgiving_friday: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    presidents_day_label: ClassVar[str]
    include_thanksgiving_wednesday: ClassVar[bool]
    def get_variable_days(self, year): ...
