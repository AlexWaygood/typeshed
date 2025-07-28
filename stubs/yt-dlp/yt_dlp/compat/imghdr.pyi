from _typeshed import FileDescriptorOrPath

def what(file: FileDescriptorOrPath | None = None, h: bytes | None = None) -> str | None:
    """Detect format of image (Currently supports jpeg, png, webp, gif only)
    Ref: https://github.com/python/cpython/blob/3.11/Lib/imghdr.py
    Ref: https://www.w3.org/Graphics/JPEG/itu-t81.pdf
    """
