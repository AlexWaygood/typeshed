"""Implements `AMQPConnectionWorkflow` - the default workflow of performing
multiple TCP/[SSL]/AMQP connection attempts with timeouts and retries until one
succeeds or all attempts fail.

Defines the interface `AbstractAMQPConnectionWorkflow` that facilitates
implementing custom connection workflows.

"""

from _typeshed import Incomplete

import pika.compat

class AMQPConnectorException(Exception):
    """Base exception for this module"""

class AMQPConnectorStackTimeout(AMQPConnectorException):
    """Overall TCP/[SSL]/AMQP stack connection attempt timed out."""

class AMQPConnectorAborted(AMQPConnectorException):
    """Asynchronous request was aborted"""

class AMQPConnectorWrongState(AMQPConnectorException):
    """AMQPConnector operation requested in wrong state, such as aborting after
    completion was reported.
    """

class AMQPConnectorPhaseErrorBase(AMQPConnectorException):
    """Wrapper for exception that occurred during a particular bring-up phase."""

    exception: Incomplete
    def __init__(self, exception, *args) -> None:
        """

        :param BaseException exception: error that occurred while waiting for a
            subclass-specific protocol bring-up phase to complete.
        :param args: args for parent class
        """

class AMQPConnectorSocketConnectError(AMQPConnectorPhaseErrorBase):
    """Error connecting TCP socket to remote peer"""

class AMQPConnectorTransportSetupError(AMQPConnectorPhaseErrorBase):
    """Error setting up transport after TCP connected but before AMQP handshake."""

class AMQPConnectorAMQPHandshakeError(AMQPConnectorPhaseErrorBase):
    """Error during AMQP handshake"""

class AMQPConnectionWorkflowAborted(AMQPConnectorException):
    """AMQP Connection workflow was aborted."""

class AMQPConnectionWorkflowWrongState(AMQPConnectorException):
    """AMQP Connection Workflow operation requested in wrong state, such as
    aborting after completion was reported.
    """

class AMQPConnectionWorkflowFailed(AMQPConnectorException):
    """Indicates that AMQP connection workflow failed."""

    exceptions: Incomplete
    def __init__(self, exceptions, *args) -> None:
        """
        :param sequence exceptions: Exceptions that occurred during the
            workflow.
        :param args: args to pass to base class

        """

class AMQPConnector:
    """Performs a single TCP/[SSL]/AMQP connection workflow."""

    def __init__(self, conn_factory, nbio) -> None:
        """

        :param callable conn_factory: A function that takes
            `pika.connection.Parameters` as its only arg and returns a brand new
            `pika.connection.Connection`-based adapter instance each time it is
            called. The factory must instantiate the connection with
            `internal_connection_workflow=False`.
        :param pika.adapters.utils.nbio_interface.AbstractIOServices nbio:

        """

    def start(self, addr_record, conn_params, on_done) -> None:
        """Asynchronously perform a single TCP/[SSL]/AMQP connection attempt.

        :param tuple addr_record: a single resolved address record compatible
            with `socket.getaddrinfo()` format.
        :param pika.connection.Parameters conn_params:
        :param callable on_done: Function to call upon completion of the
            workflow: `on_done(pika.connection.Connection | BaseException)`. If
            exception, it's going to be one of the following:
                `AMQPConnectorSocketConnectError`
                `AMQPConnectorTransportSetupError`
                `AMQPConnectorAMQPHandshakeError`
                `AMQPConnectorAborted`

        """

    def abort(self) -> None:
        """Abort the workflow asynchronously. The completion callback will be
        called with an instance of AMQPConnectorAborted.

        NOTE: we can't cancel/close synchronously because aborting pika
        Connection and its transport requires an asynchronous operation.

        :raises AMQPConnectorWrongState: If called after completion has been
            reported or the workflow not started yet.
        """

class AbstractAMQPConnectionWorkflow(pika.compat.AbstractBase):
    """Interface for implementing a custom TCP/[SSL]/AMQP connection workflow."""

    def start(self, connection_configs, connector_factory, native_loop, on_done) -> None:
        """Asynchronously perform the workflow until success or all retries
        are exhausted. Called by the adapter.

        :param sequence connection_configs: A sequence of one or more
            `pika.connection.Parameters`-based objects. Will attempt to connect
            using each config in the given order.
        :param callable connector_factory: call it without args to obtain a new
            instance of `AMQPConnector` for each connection attempt.
            See `AMQPConnector` for details.
        :param native_loop: Native I/O loop passed by app to the adapter or
            obtained by the adapter by default.
        :param callable on_done: Function to call upon completion of the
            workflow:
            `on_done(pika.connection.Connection |
                     AMQPConnectionWorkflowFailed |
                     AMQPConnectionWorkflowAborted)`.
            `Connection`-based adapter on success,
            `AMQPConnectionWorkflowFailed` on failure,
            `AMQPConnectionWorkflowAborted` if workflow was aborted.

        :raises AMQPConnectionWorkflowWrongState: If called in wrong state, such
            as after starting the workflow.
        """

    def abort(self) -> None:
        """Abort the workflow asynchronously. The completion callback will be
        called with an instance of AMQPConnectionWorkflowAborted.

        NOTE: we can't cancel/close synchronously because aborting pika
        Connection and its transport requires an asynchronous operation.

        :raises AMQPConnectionWorkflowWrongState: If called in wrong state, such
            as before starting or after completion has been reported.
        """

class AMQPConnectionWorkflow(AbstractAMQPConnectionWorkflow):
    """Implements Pika's default workflow for performing multiple TCP/[SSL]/AMQP
    connection attempts with timeouts and retries until one succeeds or all
    attempts fail.

    The workflow:
        while not success and retries remain:
            1. For each given config (pika.connection.Parameters object):
                A. Perform DNS resolution of the config's host.
                B. Attempt to establish TCP/[SSL]/AMQP for each resolved address
                   until one succeeds, in which case we're done.
            2. If all configs failed but retries remain, resume from beginning
               after the given retry pause. NOTE: failure of DNS resolution
               is equivalent to one cycle and will be retried after the pause
               if retries remain.

    """

    def __init__(self, _until_first_amqp_attempt: bool = False) -> None:
        """
        :param int | float retry_pause: Non-negative number of seconds to wait
            before retrying the config sequence. Meaningful only if retries is
            greater than 0. Defaults to 2 seconds.
        :param bool _until_first_amqp_attempt: INTERNAL USE ONLY; ends workflow
            after first AMQP handshake attempt, regardless of outcome (success
            or failure). The automatic connection logic in
            `pika.connection.Connection` enables this because it's not
            designed/tested to reset all state properly to handle more than one
            AMQP handshake attempt.

        TODO: Do we need getaddrinfo timeout?
        TODO: Would it be useful to implement exponential back-off?

        """

    def set_io_services(self, nbio) -> None:
        """Called by the conneciton adapter only on pika's
        `AMQPConnectionWorkflow` instance to provide it the adapter-specific
        `AbstractIOServices` object before calling the `start()` method.

        NOTE: Custom workflow implementations should use the native I/O loop
        directly because `AbstractIOServices` is private to Pika
        implementation and its interface may change without notice.

        :param pika.adapters.utils.nbio_interface.AbstractIOServices nbio:

        """

    def start(self, connection_configs, connector_factory, native_loop, on_done) -> None:
        """Override `AbstractAMQPConnectionWorkflow.start()`.

        NOTE: This implementation uses `connection_attempts` and `retry_delay`
        values from the last element of the given `connection_configs` sequence
        as the overall number of connection attempts of the entire
        `connection_configs` sequence and pause between each sequence.

        """

    def abort(self) -> None:
        """Override `AbstractAMQPConnectionWorkflow.abort()`."""
