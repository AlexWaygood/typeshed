from asgiref.typing import ASGIReceiveCallable, ASGISendCallable
from channels.middleware import BaseMiddleware
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import LazyObject

from .consumer import _ChannelScope
from .utils import _ChannelApplication

async def get_user(scope: _ChannelScope) -> AbstractBaseUser | AnonymousUser:
    """
    Return the user model instance associated with the given scope.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """

async def login(scope: _ChannelScope, user: AbstractBaseUser, backend: BaseBackend | None = None) -> None:
    """
    Persist a user id and a backend in the request.
    This way a user doesn't have to re-authenticate on every request.
    Note that data set during the anonymous session is retained when the user
    logs in.
    """

async def logout(scope: _ChannelScope) -> None:
    """
    Remove the authenticated user's ID from the request and flush their session
    data.
    """

# Inherits AbstractBaseUser to improve autocomplete and show this is a lazy proxy for a user.
# At runtime, it's just a LazyObject that wraps the actual user instance.
class UserLazyObject(AbstractBaseUser, LazyObject):
    """
    Throw a more useful error message when scope['user'] is accessed before
    it's resolved
    """

class AuthMiddleware(BaseMiddleware):
    """
    Middleware which populates scope["user"] from a Django session.
    Requires SessionMiddleware to function.
    """

    def populate_scope(self, scope: _ChannelScope) -> None: ...
    async def resolve_scope(self, scope: _ChannelScope) -> None: ...
    async def __call__(
        self, scope: _ChannelScope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> _ChannelApplication: ...

def AuthMiddlewareStack(inner: _ChannelApplication) -> _ChannelApplication: ...
