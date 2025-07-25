from typing import Any, TypedDict, type_check_only

import click

@type_check_only
class _FormData(TypedDict):
    command: click.Command
    fields: list[dict[str, Any]]  # each item is result of resources.input_fields.get_input_field() function

def get_form_for(command_path: str) -> str: ...
def _get_commands_by_path(command_path: str) -> list[tuple[click.Context, click.Command]]:
    """
    Take a (slash separated) string and generate (context, command) for each level.
    :param command_path: "some_group/a_command"
    :return: Return a list from root to leaf commands. each element is (Click.Context, Click.Command)
    """

def _generate_form_data(ctx_and_commands: list[tuple[click.Context, click.Command]]) -> list[_FormData]:
    """
    Construct a list of contexts and commands generate a python data structure for rendering jinja form
    :return: a list of dicts
    """

def _process_help(help_text: bool) -> str:
    """
    Convert click command help into html to be presented to browser.
    Respects the '\x08' char used by click to mark pre-formatted blocks.
    Also escapes html reserved characters in the help text.

    :param help_text: str
    :return: A html formatted help string.
    """
