"""
Provide the Reporter class.
"""

from _typeshed import SupportsWrite

from .messages import Message

class Reporter:
    """
    Formats the results of pyflakes checks to users.
    """

    def __init__(self, warningStream: SupportsWrite[str], errorStream: SupportsWrite[str]) -> None:
        """
        Construct a L{Reporter}.

        @param warningStream: A file-like object where warnings will be
            written to.  The stream's C{write} method must accept unicode.
            C{sys.stdout} is a good value.
        @param errorStream: A file-like object where error output will be
            written to.  The stream's C{write} method must accept unicode.
            C{sys.stderr} is a good value.
        """

    def unexpectedError(self, filename: str, msg: str) -> None:
        """
        An unexpected error occurred trying to process C{filename}.

        @param filename: The path to a file that we could not process.
        @ptype filename: C{unicode}
        @param msg: A message explaining the problem.
        @ptype msg: C{unicode}
        """

    def syntaxError(self, filename: str, msg: str, lineno: int, offset: int | None, text: str | None) -> None:
        """
        There was a syntax error in C{filename}.

        @param filename: The path to the file with the syntax error.
        @ptype filename: C{unicode}
        @param msg: An explanation of the syntax error.
        @ptype msg: C{unicode}
        @param lineno: The line number where the syntax error occurred.
        @ptype lineno: C{int}
        @param offset: The column on which the syntax error occurred, or None.
        @ptype offset: C{int}
        @param text: The source code containing the syntax error.
        @ptype text: C{unicode}
        """

    def flake(self, message: Message) -> None:
        """
        pyflakes found something wrong with the code.

        @param: A L{pyflakes.messages.Message}.
        """
