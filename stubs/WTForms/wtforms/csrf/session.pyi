"""
A provided CSRF implementation which puts CSRF data in a session.

This can be used fairly comfortably with many `request.session` type
objects, including the Werkzeug/Flask session store, Django sessions, and
potentially other similar objects which use a dict-like API for storing
session keys.

The basic concept is a randomly generated value is stored in the user's
session, and an hmac-sha1 of it (along with an optional expiration time,
for extra security) is used as the value of the csrf_token. If this token
validates with the hmac of the random value + expiration time, and the
expiration time is not passed, the CSRF validation will pass.
"""

from _typeshed import SupportsItemAccess
from datetime import datetime, timedelta
from typing import Any

from wtforms.csrf.core import CSRF, CSRFTokenField
from wtforms.form import BaseForm
from wtforms.meta import DefaultMeta

__all__ = ("SessionCSRF",)

class SessionCSRF(CSRF):
    TIME_FORMAT: str
    form_meta: DefaultMeta
    def generate_csrf_token(self, csrf_token_field: CSRFTokenField) -> str: ...
    def validate_csrf_token(self, form: BaseForm, field: CSRFTokenField) -> None: ...
    def now(self) -> datetime:
        """
        Get the current time. Used for test mocking/overriding mainly.
        """

    @property
    def time_limit(self) -> timedelta: ...
    @property
    def session(self) -> SupportsItemAccess[str, Any]: ...
