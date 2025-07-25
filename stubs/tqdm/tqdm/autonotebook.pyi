"""
Automatically choose between `tqdm.notebook` and `tqdm.std`.

Usage:
>>> from tqdm.autonotebook import trange, tqdm
>>> for i in trange(10):
...     ...
"""

from .std import tqdm as tqdm, trange as trange

__all__ = ["tqdm", "trange"]
