from _typeshed import Incomplete

def in_transaction():
    """Determine if there is a currently active transaction.

    Returns:
        bool: :data:`True` if there is a transaction for the current context,
            otherwise :data:`False`.
    """

def transaction(
    callback, retries=..., read_only: bool = ..., join: bool = ..., xg: bool = ..., propagation: Incomplete | None = ...
):
    """Run a callback in a transaction.

    Args:
        callback (Callable): The function or tasklet to be called.
        retries (int): Number of times to potentially retry the callback in
            case of transient server errors.
        read_only (bool): Whether to run the transaction in read only mode.
        join (bool): In the event of an already running transaction, if `join`
            is `True`, `callback` will be run in the already running
            transaction, otherwise an exception will be raised. Transactions
            cannot be nested.
        xg (bool): Enable cross-group transactions. This argument is included
            for backwards compatibility reasons and is ignored. All Datastore
            transactions are cross-group, up to 25 entity groups, all the time.
        propagation (int): An element from :class:`ndb.TransactionOptions`.
            This parameter controls what happens if you try to start a new
            transaction within an existing transaction. If this argument is
            provided, the `join` argument will be ignored.
    """

def transaction_async(
    callback, retries=..., read_only: bool = ..., join: bool = ..., xg: bool = ..., propagation: Incomplete | None = ...
): ...
def transaction_async_(
    callback, retries=..., read_only: bool = ..., join: bool = ..., xg: bool = ..., propagation: Incomplete | None = ...
):
    """Run a callback in a transaction.

    This is the asynchronous version of :func:`transaction`.
    """

def transactional(retries=..., read_only: bool = ..., join: bool = ..., xg: bool = ..., propagation: Incomplete | None = ...):
    """A decorator to run a function automatically in a transaction.

    Usage example:

    @transactional(retries=1, read_only=False)
    def callback(args):
        ...

    Unlike func:`transaction`_, the ``join`` argument defaults to ``True``,
    making functions decorated with func:`transactional`_ composable, by
    default. IE, a function decorated with ``transactional`` can call another
    function decorated with ``transactional`` and the second function will be
    executed in the already running transaction.

    See google.cloud.ndb.transaction for available options.
    """

def transactional_async(
    retries=..., read_only: bool = ..., join: bool = ..., xg: bool = ..., propagation: Incomplete | None = ...
):
    """A decorator to run a function in an async transaction.

    Usage example:

    @transactional_async(retries=1, read_only=False)
    def callback(args):
        ...

    Unlike func:`transaction`_, the ``join`` argument defaults to ``True``,
    making functions decorated with func:`transactional`_ composable, by
    default. IE, a function decorated with ``transactional_async`` can call
    another function decorated with ``transactional_async`` and the second
    function will be executed in the already running transaction.

    See google.cloud.ndb.transaction above for available options.
    """

def transactional_tasklet(
    retries=..., read_only: bool = ..., join: bool = ..., xg: bool = ..., propagation: Incomplete | None = ...
):
    """A decorator that turns a function into a tasklet running in transaction.

    Wrapped function returns a Future.

    Unlike func:`transaction`_, the ``join`` argument defaults to ``True``,
    making functions decorated with func:`transactional`_ composable, by
    default. IE, a function decorated with ``transactional_tasklet`` can call
    another function decorated with ``transactional_tasklet`` and the second
    function will be executed in the already running transaction.

    See google.cloud.ndb.transaction above for available options.
    """

def non_transactional(allow_existing: bool = ...):
    """A decorator that ensures a function is run outside a transaction.

    If there is an existing transaction (and allow_existing=True), the existing
    transaction is paused while the function is executed.

    Args:
        allow_existing: If false, an exception will be thrown when called from
            within a transaction. If true, a new non-transactional context will
            be created for running the function; the original transactional
            context will be saved and then restored after the function is
            executed. Defaults to True.
    """
