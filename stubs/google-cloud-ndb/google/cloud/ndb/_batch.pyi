"""Support for batching operations."""

from _typeshed import Incomplete

def get_batch(batch_cls, options: Incomplete | None = ...):
    """Gets a data structure for storing batched calls to Datastore Lookup.

    The batch data structure is stored in the current context. If there is
    not already a batch started, a new structure is created and an idle
    callback is added to the current event loop which will eventually perform
    the batch look up.

    Args:
        batch_cls (type): Class representing the kind of operation being
            batched.
        options (_options.ReadOptions): The options for the request. Calls with
            different options will be placed in different batches.

    Returns:
        batch_cls: An instance of the batch class.
    """
