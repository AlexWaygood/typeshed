"""Implementation of the StyleGuide used by Flake8."""

import argparse
import enum
from _typeshed import Incomplete
from collections.abc import Generator, Sequence

from .formatting.base import BaseFormatter
from .statistics import Statistics

__all__ = ("StyleGuide",)

class Selected(enum.Enum):
    """Enum representing an explicitly or implicitly selected code."""

    Explicitly = "explicitly selected"
    Implicitly = "implicitly selected"

class Ignored(enum.Enum):
    """Enum representing an explicitly or implicitly ignored code."""

    Explicitly = "explicitly ignored"
    Implicitly = "implicitly ignored"

class Decision(enum.Enum):
    """Enum representing whether a code should be ignored or selected."""

    Ignored = "ignored error"
    Selected = "selected error"

class DecisionEngine:
    """A class for managing the decision process around violations.

    This contains the logic for whether a violation should be reported or
    ignored.
    """

    cache: Incomplete
    selected_explicitly: Incomplete
    ignored_explicitly: Incomplete
    selected: Incomplete
    ignored: Incomplete
    def __init__(self, options: argparse.Namespace) -> None:
        """Initialize the engine."""

    def was_selected(self, code: str) -> Selected | Ignored:
        """Determine if the code has been selected by the user.

        :param code: The code for the check that has been run.
        :returns:
            Selected.Implicitly if the selected list is empty,
            Selected.Explicitly if the selected list is not empty and a match
            was found,
            Ignored.Implicitly if the selected list is not empty but no match
            was found.
        """

    def was_ignored(self, code: str) -> Selected | Ignored:
        """Determine if the code has been ignored by the user.

        :param code:
            The code for the check that has been run.
        :returns:
            Selected.Implicitly if the ignored list is empty,
            Ignored.Explicitly if the ignored list is not empty and a match was
            found,
            Selected.Implicitly if the ignored list is not empty but no match
            was found.
        """

    def make_decision(self, code: str) -> Decision:
        """Decide if code should be ignored or selected."""

    def decision_for(self, code: str) -> Decision:
        """Return the decision for a specific code.

        This method caches the decisions for codes to avoid retracing the same
        logic over and over again. We only care about the select and ignore
        rules as specified by the user in their configuration files and
        command-line flags.

        This method does not look at whether the specific line is being
        ignored in the file itself.

        :param code: The code for the check that has been run.
        """

class StyleGuideManager:
    """Manage multiple style guides for a single run."""

    options: Incomplete
    formatter: Incomplete
    stats: Incomplete
    decider: Incomplete
    style_guides: Incomplete
    default_style_guide: Incomplete
    style_guide_for: Incomplete
    def __init__(self, options: argparse.Namespace, formatter: BaseFormatter, decider: DecisionEngine | None = None) -> None:
        """Initialize our StyleGuide.

        .. todo:: Add parameter documentation.
        """

    def populate_style_guides_with(self, options: argparse.Namespace) -> Generator[StyleGuide, None, None]:
        """Generate style guides from the per-file-ignores option.

        :param options:
            The original options parsed from the CLI and config file.
        :returns:
            A copy of the default style guide with overridden values.
        """

    def processing_file(self, filename: str) -> Generator[StyleGuide, None, None]:
        """Record the fact that we're processing the file's results."""

    def handle_error(
        self, code: str, filename: str, line_number: int, column_number: int, text: str, physical_line: str | None = None
    ) -> int:
        """Handle an error reported by a check.

        :param code:
            The error code found, e.g., E123.
        :param filename:
            The file in which the error was found.
        :param line_number:
            The line number (where counting starts at 1) at which the error
            occurs.
        :param column_number:
            The column number (where counting starts at 1) at which the error
            occurs.
        :param text:
            The text of the error message.
        :param physical_line:
            The actual physical line causing the error.
        :returns:
            1 if the error was reported. 0 if it was ignored. This is to allow
            for counting of the number of errors found that were not ignored.
        """

class StyleGuide:
    """Manage a Flake8 user's style guide."""

    options: Incomplete
    formatter: Incomplete
    stats: Incomplete
    decider: Incomplete
    filename: Incomplete
    def __init__(
        self,
        options: argparse.Namespace,
        formatter: BaseFormatter,
        stats: Statistics,
        filename: str | None = None,
        decider: DecisionEngine | None = None,
    ) -> None:
        """Initialize our StyleGuide.

        .. todo:: Add parameter documentation.
        """

    def copy(self, filename: str | None = None, extend_ignore_with: Sequence[str] | None = None) -> StyleGuide:
        """Create a copy of this style guide with different values."""

    def processing_file(self, filename: str) -> Generator[StyleGuide, None, None]:
        """Record the fact that we're processing the file's results."""

    def applies_to(self, filename: str) -> bool:
        """Check if this StyleGuide applies to the file.

        :param filename:
            The name of the file with violations that we're potentially
            applying this StyleGuide to.
        :returns:
            True if this applies, False otherwise
        """

    def should_report_error(self, code: str) -> Decision:
        """Determine if the error code should be reported or ignored.

        This method only cares about the select and ignore rules as specified
        by the user in their configuration files and command-line flags.

        This method does not look at whether the specific line is being
        ignored in the file itself.

        :param code:
            The code for the check that has been run.
        """

    def handle_error(
        self, code: str, filename: str, line_number: int, column_number: int, text: str, physical_line: str | None = None
    ) -> int:
        """Handle an error reported by a check.

        :param code:
            The error code found, e.g., E123.
        :param filename:
            The file in which the error was found.
        :param line_number:
            The line number (where counting starts at 1) at which the error
            occurs.
        :param column_number:
            The column number (where counting starts at 1) at which the error
            occurs.
        :param text:
            The text of the error message.
        :param physical_line:
            The actual physical line causing the error.
        :returns:
            1 if the error was reported. 0 if it was ignored. This is to allow
            for counting of the number of errors found that were not ignored.
        """
