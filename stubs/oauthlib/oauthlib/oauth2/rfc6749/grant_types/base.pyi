"""
oauthlib.oauth2.rfc6749.grant_types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from _typeshed import Incomplete
from collections.abc import Callable, Iterable
from itertools import chain
from logging import Logger
from typing import TypeVar
from typing_extensions import TypeAlias

from oauthlib.common import Request

from ..request_validator import RequestValidator
from ..tokens import TokenBase

log: Logger

_T = TypeVar("_T")
_AuthValidator: TypeAlias = Callable[[Request], dict[str, Incomplete]]
_TokenValidator: TypeAlias = Callable[[Request], None]
_CodeModifier: TypeAlias = Callable[[dict[str, str], TokenBase | None, Request | None], dict[str, str]]
_TokenModifier: TypeAlias = Callable[[dict[str, Incomplete], TokenBase | None, Request | None], dict[str, Incomplete]]

class ValidatorsContainer:
    """
    Container object for holding custom validator callables to be invoked
    as part of the grant type `validate_authorization_request()` or
    `validate_authorization_request()` methods on the various grant types.

    Authorization validators must be callables that take a request object and
    return a dict, which may contain items to be added to the `request_info`
    returned from the grant_type after validation.

    Token validators must be callables that take a request object and
    return None.

    Both authorization validators and token validators may raise OAuth2
    exceptions if validation conditions fail.

    Authorization validators added to `pre_auth` will be run BEFORE
    the standard validations (but after the critical ones that raise
    fatal errors) as part of `validate_authorization_request()`

    Authorization validators added to `post_auth` will be run AFTER
    the standard validations as part of `validate_authorization_request()`

    Token validators added to `pre_token` will be run BEFORE
    the standard validations as part of `validate_token_request()`

    Token validators added to `post_token` will be run AFTER
    the standard validations as part of `validate_token_request()`

    For example:

    >>> def my_auth_validator(request):
    ...    return {'myval': True}
    >>> auth_code_grant = AuthorizationCodeGrant(request_validator)
    >>> auth_code_grant.custom_validators.pre_auth.append(my_auth_validator)
    >>> def my_token_validator(request):
    ...     if not request.everything_okay:
    ...         raise errors.OAuth2Error("uh-oh")
    >>> auth_code_grant.custom_validators.post_token.append(my_token_validator)
    """

    pre_auth: Iterable[_AuthValidator]
    post_auth: Iterable[_AuthValidator]
    pre_token: Iterable[_TokenValidator]
    post_token: Iterable[_TokenValidator]
    def __init__(
        self,
        post_auth: Iterable[_AuthValidator],
        post_token: Iterable[_TokenValidator],
        pre_auth: Iterable[_AuthValidator],
        pre_token: Iterable[_TokenValidator],
    ) -> None: ...
    @property
    def all_pre(self) -> chain[_AuthValidator | _TokenValidator]: ...
    @property
    def all_post(self) -> chain[_AuthValidator | _TokenValidator]: ...

class GrantTypeBase:
    error_uri: str | None
    request_validator: RequestValidator | None
    default_response_mode: str
    refresh_token: bool
    response_types: list[str]
    def __init__(
        self,
        request_validator: RequestValidator | None = None,
        *,
        post_auth: Iterable[_AuthValidator] | None = None,
        post_token: Iterable[_TokenValidator] | None = None,
        pre_auth: Iterable[_AuthValidator] | None = None,
        pre_token: Iterable[_TokenValidator] | None = None,
        **kwargs,
    ) -> None: ...
    def register_response_type(self, response_type: str) -> None: ...
    def register_code_modifier(self, modifier: _CodeModifier) -> None: ...
    def register_token_modifier(self, modifier: _TokenModifier) -> None: ...
    def create_authorization_response(
        self, request: Request, token_handler: TokenBase
    ) -> tuple[dict[str, str], str | None, int | None]:
        """
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :param token_handler: A token handler instance, for example of type
                              oauthlib.oauth2.BearerToken.
        """

    def create_token_response(self, request: Request, token_handler: TokenBase) -> tuple[dict[str, str], str | None, int | None]:
        """
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :param token_handler: A token handler instance, for example of type
                              oauthlib.oauth2.BearerToken.
        """

    def add_token(self, token: dict[str, _T], token_handler: TokenBase, request: Request) -> dict[str, _T]:
        """
        :param token:
        :param token_handler: A token handler instance, for example of type
                              oauthlib.oauth2.BearerToken.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        """

    def validate_grant_type(self, request: Request) -> None:
        """
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        """

    def validate_scopes(self, request: Request) -> None:
        """
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        """

    def prepare_authorization_response(
        self, request: Request, token: dict[str, Incomplete], headers: dict[str, str], body: str | None, status: int | None
    ) -> tuple[dict[str, str], str | None, int | None]:
        """Place token according to response mode.

        Base classes can define a default response mode for their authorization
        response by overriding the static `default_response_mode` member.

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :param token:
        :param headers:
        :param body:
        :param status:
        """
