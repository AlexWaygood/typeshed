from typing import Final

DEFAULT_ROW_HEIGHT: Final[float]
BASE_COL_WIDTH: Final = 8
DEFAULT_COLUMN_WIDTH: Final = 13
DEFAULT_LEFT_MARGIN: Final[float]
DEFAULT_TOP_MARGIN: Final[float]
DEFAULT_HEADER: Final[float]

def inch_to_dxa(value):
    """1 inch = 72 * 20 dxa"""

def dxa_to_inch(value): ...
def dxa_to_cm(value): ...
def cm_to_dxa(value): ...
def pixels_to_EMU(value):
    """1 pixel = 9525 EMUs"""

def EMU_to_pixels(value): ...
def cm_to_EMU(value):
    """1 cm = 360000 EMUs"""

def EMU_to_cm(value): ...
def inch_to_EMU(value):
    """1 inch = 914400 EMUs"""

def EMU_to_inch(value): ...
def pixels_to_points(value, dpi: int = 96):
    """96 dpi, 72i"""

def points_to_pixels(value, dpi: int = 96): ...
def degrees_to_angle(value):
    """1 degree = 60000 angles"""

def angle_to_degrees(value): ...
def short_color(color):
    """format a color to its short size"""
