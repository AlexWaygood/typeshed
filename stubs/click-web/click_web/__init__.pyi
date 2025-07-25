import logging
import types
from _typeshed import Incomplete

import click
import flask

# This should be jinja2.Environment, but it does not have stubs and forbidden for requires in METADATA.toml
jinja_env: Incomplete
script_file: str | None
click_root_cmd: str | None
OUTPUT_FOLDER: str
_flask_app: flask.Flask | None
logger: logging.Logger | None

def create_click_web_app(module: types.ModuleType, command: click.Command, root: str = "/") -> flask.Flask:
    """
    Create a Flask app that wraps a click command. (Call once)

    :param module: the module that contains the click command, needed to get the path to the script.
    :param command: The actual click root command, needed to be able to read the command tree and arguments
                    in order to generate the index page and the html forms
    :param root: the root url path to server click-web under.
    usage:

        from click_web import create_click_web_app

        import a_click_script

        app = create_click_web_app(a_click_script, a_click_script.a_group_or_command)

    """
