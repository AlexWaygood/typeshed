from collections.abc import Iterable, Sequence
from typing import Any, NamedTuple

from consolemenu.screen import Screen
from consolemenu.validators.base import BaseValidator

class InputResult(NamedTuple):
    """InputResult(input_string, validation_result)"""

    input_string: str
    validation_result: bool

class PromptFormatter:
    """
    Class for formatting a text input prompt, to allow overriding the message as desired.

    Default answers will appear in [square brackets] and allow the user to return that answer by simply pressing
    the Enter button.

    If a 'Quit' option is desired, set `enable_quit` to True and provide a `quit_string` (default is 'q') and
    a `quit_message` (default is '(enter q to Quit)').

    """

    @staticmethod
    def format_prompt(
        prompt: str | None = None,
        default: str | None = None,
        enable_quit: bool = False,
        quit_string: str = "q",
        quit_message: str = "(enter q to Quit)",
    ) -> str:
        """
        Format the message presented to the user during input prompting.

        Args:
            prompt (str): The message to ask the user.
            default (str, optional): The default answer if user does not provide explicit input.
            enable_quit (bool, optional): Flag to determine whether a Quit option will be presented.
            quit_string (str, optional): The string the user must input to quit (default is 'q').
            quit_message (str, optional): The message to the user explaining how to Quit.

        Returns:
            str: The formatted prompt string.
        """

class PromptUtils:
    """
    Utility class with various routines for prompting for user input.
    """

    def __init__(self, screen: Screen, prompt_formatter: PromptFormatter | None = None) -> None:
        """
        Creates a new instance of ConsoleUtils with the specified console. If no console was
        specified, creates a new default console using the ConsoleFactory.

        Args:
            screen (:obj:`consolemenu.screen.Screen`): The Screen instance.
            prompt_formatter (:obj:`PromptFormatter`, optional): The instance of PromptFormatter for displaying
             the prompt.
        """

    @property
    def screen(self) -> Screen:
        """
        :obj:`consolemenu.screen.Screen`: The Screen instance.
        """

    def clear(self) -> None:
        """
        Clear the screen.
        """

    def confirm_answer(self, answer: str, message: str | None = None) -> bool:
        """
        Prompts the user to confirm a question with a yes/no prompt.
        If no message is specified, the default message is:  "You entered {}. Is this correct?"

        Args:
            answer (str): The answer to confirm.
            message (str, optional): Optional message if a different confirmation prompt is desired.

        Returns:
            bool: True if the user confirmed Yes, or False if user specified No.

        """

    def enter_to_continue(self, message: str | None = None) -> None:
        """
        A console prompt to ask the user to 'Press [Enter] to continue'.

        Args:
            message (str, optional): A message to display in place of the default.
        """

    def input(
        self,
        prompt: str | None = None,
        default: str | None = None,
        validators: Iterable[BaseValidator] | None = None,
        enable_quit: bool = False,
        quit_string: str = "q",
        quit_message: str = "(enter q to Quit)",
    ) -> InputResult:
        """
        Generic prompt the user for input.

        Args:
            prompt (str): The message to prompt the user.
            default (str, optional): The default value to suggest as an answer.
            validators (:obj:`BaseValidator`, optional): The list of validators to perform input validation.
            enable_quit (bool, optional): Specifies whether the user can cancel out of the input prompt.
            quit_string (str, optional): The string which the user must input in order to quit.
            quit_message (str, optional): The message to explain how to quit.

        Returns:
            InputResult: an InputResult tuple.

        """

    def input_password(self, message: str | None = None) -> str:
        """
        Prompt the user for a password or other confidential data.

        This is equivalent to the input() method, but does not echo inputted characters to the screen.

        Args:
            message (str): The prompt message.

        Returns:
            str: The password provided by the user.
        """

    def printf(self, *args: Any) -> None:
        """
        Prints the specified arguments to the screen.

        Args:
            *args: Variable length argument list.
        """

    def println(self, *args: Any) -> None:
        """
        Prints the specified arguments to the screen, followed by a newline character.

        Args:
            *args: Variable length argument list.
        """

    def prompt_and_confirm_password(self, message: str) -> str:
        """
        Prompt for a password using the given message, then prompt a second time for a confirmation
        password, and verify both provided passwords match. If the passwords do not match, an error
        is displayed, "Passwords do not match", and the user must input both passwords again.

        Args:
            message (str): The prompt message.

        Returns:
            str: The password.
        """

    def prompt_for_bilateral_choice(self, prompt: str, option1: str, option2: str) -> str:
        """
        Prompt the user for a response that must be one of the two supplied choices.

        NOTE: The user input verification is case-insensitive, but will return the original case provided
        by the given options.

        Args:
            prompt (str): The prompt to present the choices to the user.
            option1 (str): The first option.
            option2 (str): The second option.

        Returns:
            str: The choice selected by the user.

        """

    def prompt_for_trilateral_choice(self, prompt: str, option1: str, option2: str, option3: str) -> str:
        """
        Prompt the user for a response that must be one of the three supplied choices.

        NOTE: The user input verification is case-insensitive, but will return the original case provided
        by the given options.

        Args:
            prompt (str): The prompt to present the choices to the user.
            option1 (str): The first option.
            option2 (str): The second option.
            option3 (str): The third option.

        Returns:
            str: The choice selected by the user.
        """

    def prompt_for_yes_or_no(self, prompt: str) -> bool:
        """
        Prompts the user with the specified question, and expects a yes (y) or no (n)
        response, returning a boolean value representing the user's answer.

        Args:
            prompt (str): The prompt to display to the user.

        Returns:
            bool: True for yes, False for no.
        """

    def prompt_for_numbered_choice(self, choices: Sequence[str], title: str | None = None, prompt: str = ">") -> int:
        """
        Displays a numbered vertical list of choices from the provided list of strings.

        Args:
            choices (:obj:`list` of :obj:`str`): The list of choices to display.
            title (str, optional): Optional title to display above the numbered list.
            prompt (str): The prompt string. Default is ">".

        Returns:
            int: The index of selected choice.
        """

    def validate_input(self, input_string: str, validators: BaseValidator) -> bool:
        """
        Validate the given input string against the specified list of validators.

        Args:
            input_string (str): The input string to verify.
            validators (:obj:`list` of :obj:`BaseValidator`): The list of validators.

        Returns:
            bool: The validation result. True if the input is valid; False otherwise.

        Raises:
            InvalidValidator: If the list of validators contains an invalid BaseValidator class.
        """

class UserQuit(Exception):
    """
    Exception raised when a user chooses to Quit from an input prompt.
    """
