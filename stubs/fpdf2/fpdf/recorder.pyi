"""
A wrapper class to allow rewinding/replaying changes made to a FPDF instance.

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

from typing import Any

class FPDFRecorder:
    """
    The class is aimed to be used as wrapper around fpdf.FPDF:

        pdf = FPDF()
        recorder = FPDFRecorder(pdf)

    Its aim is dual:
      * allow to **rewind** to the state of the FPDF instance passed to its constructor,
        reverting all changes made to its internal state
      * allow to **replay** again all the methods calls performed
        on the recorder instance between its creation and the last call to rewind()

    Note that method can be called on a FPDFRecorder instance using its .pdf attribute
    so that they are not recorded & replayed later, on a call to .replay().

    Note that using this class means to duplicate the FPDF `bytearray` buffer:
    when generating large PDFs, doubling memory usage may be troublesome.
    """

    pdf: Any
    accept_page_break: bool
    def __init__(self, pdf, accept_page_break: bool = True) -> None: ...
    def __getattr__(self, name: str): ...
    def rewind(self) -> None: ...
    def replay(self) -> None: ...

class CallRecorder:
    def __init__(self, func, calls) -> None: ...
    def __call__(self, *args, **kwargs): ...
