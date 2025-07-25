"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""

from typing import Any
from typing_extensions import TypeAlias

_Image: TypeAlias = Any  # actually PIL.Image, but not worth adding a dependency

def shift_hue(image: _Image, hue: float) -> _Image:
    """
    Shifts the hue of an image in HSV format.
    :param image: PIL Image to perform operation on
    :param hue: value between 0 and 2.0
    """

def make_transparent(image: _Image) -> _Image:
    """Turn all black pixels in an image into transparent ones"""
