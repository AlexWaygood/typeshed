"""
Custom exceptions for the seaborn.objects interface.

This is very lightweight, but it's a separate module to avoid circular imports.

"""

class PlotSpecError(RuntimeError):
    """
    Error class raised from seaborn.objects.Plot for compile-time failures.

    In the declarative Plot interface, exceptions may not be triggered immediately
    by bad user input (and validation at input time may not be possible). This class
    is used to signal that indirect dependency. It should be raised in an exception
    chain when compile-time operations fail with an error message providing useful
    context (e.g., scaling errors could specify the variable that failed.)

    """
