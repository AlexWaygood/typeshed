"""
This file provides zest.releaser entrypoints using when releasing new
qrcode versions.
"""

def update_manpage(data: dict[str, str]) -> None:
    """
    Update the version in the manpage document.
    """
