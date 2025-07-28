"""Callback management class, common area for keeping track of all callbacks in
the Pika stack.

"""

from _typeshed import Incomplete
from collections.abc import Callable
from logging import Logger
from typing import Literal

from pika import amqp_object, frame

LOGGER: Logger

def name_or_value(value: amqp_object.AMQPObject | frame.Frame | int | str) -> str:
    """Will take Frame objects, classes, etc and attempt to return a valid
    string identifier for them.

    :param pika.amqp_object.AMQPObject|pika.frame.Frame|int|str value: The
        value to sanitize
    :rtype: str

    """

def sanitize_prefix(function):
    """Automatically call name_or_value on the prefix passed in."""

def check_for_prefix_and_key(function):
    """Automatically return false if the key or prefix is not in the callbacks
    for the instance.

    """

class CallbackManager:
    """CallbackManager is a global callback system designed to be a single place
    where Pika can manage callbacks and process them. It should be referenced
    by the CallbackManager.instance() method instead of constructing new
    instances of it.

    """

    CALLS: str
    ARGUMENTS: str
    DUPLICATE_WARNING: str
    CALLBACK: str
    ONE_SHOT: str
    ONLY_CALLER: str
    def __init__(self) -> None:
        """Create an instance of the CallbackManager"""

    def add(
        self,
        prefix: str | int,
        key: str | object,
        callback: Callable[[Incomplete], Incomplete],
        one_shot: bool = True,
        only_caller: object | None = None,
        arguments=None,
    ) -> tuple[str | int, str | object]:
        """Add a callback to the stack for the specified key. If the call is
        specified as one_shot, it will be removed after being fired

        The prefix is usually the channel number but the class is generic
        and prefix and key may be any value. If you pass in only_caller
        CallbackManager will restrict processing of the callback to only
        the calling function/object that you specify.

        :param str|int prefix: Categorize the callback
        :param str|dict key: The key for the callback
        :param callable callback: The callback to call
        :param bool one_shot: Remove this callback after it is called
        :param object only_caller: Only allow one_caller value to call the
                                   event that fires the callback.
        :param dict arguments: Arguments to validate when processing
        :rtype: tuple(prefix, key)

        """

    def clear(self) -> None:
        """Clear all the callbacks if there are any defined."""

    def cleanup(self, prefix: str | int) -> bool:
        """Remove all callbacks from the stack by a prefix. Returns True
        if keys were there to be removed

        :param str or int prefix: The prefix for keeping track of callbacks with
        :rtype: bool

        """

    def pending(self, prefix: str | int, key: str | object) -> int | None:
        """Return count of callbacks for a given prefix or key or None

        :param str|int prefix: Categorize the callback
        :param object|str|dict key: The key for the callback
        :rtype: None or int

        """

    def process(self, prefix: str | int, key: str | object, caller, *args, **keywords) -> bool:
        """Run through and process all the callbacks for the specified keys.
        Caller should be specified at all times so that callbacks which
        require a specific function to call CallbackManager.process will
        not be processed.

        :param str|int prefix: Categorize the callback
        :param object|str|int key: The key for the callback
        :param object caller: Who is firing the event
        :param list args: Any optional arguments
        :param dict keywords: Optional keyword arguments
        :rtype: bool

        """

    def remove(
        self,
        prefix: str | int,
        key: str | object,
        callback_value: Callable[[Incomplete], Incomplete] | None = None,
        arguments=None,
    ) -> Literal[True]:
        """Remove a callback from the stack by prefix, key and optionally
        the callback itself. If you only pass in prefix and key, all
        callbacks for that prefix and key will be removed.

        :param str or int prefix: The prefix for keeping track of callbacks with
        :param str key: The callback key
        :param callable callback_value: The method defined to call on callback
        :param dict arguments: Optional arguments to check
        :rtype: bool

        """

    def remove_all(self, prefix: str | int, key: str | object) -> None:
        """Remove all callbacks for the specified prefix and key.

        :param str prefix: The prefix for keeping track of callbacks with
        :param str key: The callback key

        """
