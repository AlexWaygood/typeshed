"""
Extra click types that could be useful in a web context as they have corresponding HTML form input type.

The custom web click types need only be imported into the main script, not the app.py that flask runs.

Example usage in your click command:
\x08
    from click_web.web_click_types import EMAIL_TYPE
    @cli.command()
    @click.option("--the_email", type=EMAIL_TYPE)
    def email(the_email):
        click.echo(f"{the_email} is a valid email syntax.")

"""

import re
from typing import ClassVar, TypeVar

import click

_T = TypeVar("_T")

class EmailParamType(click.ParamType):
    EMAIL_REGEX: ClassVar[re.Pattern[str]]
    def convert(self, value: str, param: click.Parameter | None, ctx: click.Context | None) -> str: ...

class PasswordParamType(click.ParamType):
    def convert(self, value: _T, param: click.Parameter | None, ctx: click.Context | None) -> _T: ...

class TextAreaParamType(click.ParamType):
    def convert(self, value: _T, param: click.Parameter | None, ctx: click.Context | None) -> _T: ...

EMAIL_TYPE: EmailParamType
PASSWORD_TYPE: PasswordParamType
TEXTAREA_TYPE: TextAreaParamType
