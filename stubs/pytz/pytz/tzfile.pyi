"""
$Id: tzfile.py,v 1.8 2004/06/03 00:15:24 zenzen Exp $
"""

from typing import IO

from pytz.tzinfo import DstTzInfo

def build_tzinfo(zone: str, fp: IO[bytes]) -> DstTzInfo: ...
