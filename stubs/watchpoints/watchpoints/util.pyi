import ast
from collections.abc import Iterable
from types import FrameType

def getline(frame: FrameType) -> str:
    """
    get the current logic line from the frame
    """

def getargnodes(frame: FrameType) -> Iterable[tuple[ast.expr, str]]:
    """
    get the list of arguments of the current line function
    """
