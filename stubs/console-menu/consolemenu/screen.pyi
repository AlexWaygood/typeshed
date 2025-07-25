from typing import Any

class Screen:
    """
    Class representing a console screen.
    """

    def __init__(self) -> None: ...
    @property
    def screen_height(self) -> int:
        """
        int: The screen height in rows.
        """

    @property
    def screen_width(self) -> int:
        """
        int: The screen width in columns.
        """

    @staticmethod
    def clear() -> None:
        """
        Clear the screen.
        """

    @staticmethod
    def flush() -> None:
        """
        Flush any buffered standard output to screen.
        """

    def input(self, prompt: str = "") -> str:
        """
        Prompt the end user for input.

        Args:
            prompt (:obj:`str`, optional): The message to display as the prompt.

        Returns:
            The input provided by the user.
        """

    @staticmethod
    def printf(*args: Any) -> None:
        """
        Print the specified arguments to the screen.

        Args:
            *args: Variable length argument list.
        """

    @staticmethod
    def println(*args: Any) -> None:
        """
        Print the specified arguments to the screen, including an appended newline character.

        Args:
            *args: Variable length argument list.
        """
