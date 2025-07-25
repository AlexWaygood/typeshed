"""Contains the logic for all of the default options for Flake8."""

from argparse import ArgumentParser

from ..options.manager import OptionManager

def stage1_arg_parser() -> ArgumentParser:
    """Register the preliminary options on our OptionManager.

    The preliminary options include:

    - ``-v``/``--verbose``
    - ``--output-file``
    - ``--append-config``
    - ``--config``
    - ``--isolated``
    - ``--enable-extensions``
    """

class JobsArgument:
    """Type callback for the --jobs argument."""

    is_auto: bool
    n_jobs: int
    def __init__(self, arg: str) -> None:
        """Parse and validate the --jobs argument.

        :param arg: The argument passed by argparse for validation
        """

def register_default_options(option_manager: OptionManager) -> None:
    """Register the default options on our OptionManager.

    The default options include:

    - ``-q``/``--quiet``
    - ``--color``
    - ``--count``
    - ``--exclude``
    - ``--extend-exclude``
    - ``--filename``
    - ``--format``
    - ``--hang-closing``
    - ``--ignore``
    - ``--extend-ignore``
    - ``--per-file-ignores``
    - ``--max-line-length``
    - ``--max-doc-length``
    - ``--indent-size``
    - ``--select``
    - ``--extend-select``
    - ``--disable-noqa``
    - ``--show-source``
    - ``--statistics``
    - ``--exit-zero``
    - ``-j``/``--jobs``
    - ``--tee``
    - ``--benchmark``
    - ``--bug-report``
    """
