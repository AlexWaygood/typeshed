class ExecApiMixin:
    def exec_create(
        self,
        container,
        cmd,
        stdout: bool = True,
        stderr: bool = True,
        stdin: bool = False,
        tty: bool = False,
        privileged: bool = False,
        user: str = "",
        environment=None,
        workdir=None,
        detach_keys=None,
    ):
        """
        Sets up an exec instance in a running container.

        Args:
            container (str): Target container where exec instance will be
                created
            cmd (str or list): Command to be executed
            stdout (bool): Attach to stdout. Default: ``True``
            stderr (bool): Attach to stderr. Default: ``True``
            stdin (bool): Attach to stdin. Default: ``False``
            tty (bool): Allocate a pseudo-TTY. Default: False
            privileged (bool): Run as privileged.
            user (str): User to execute command as. Default: root
            environment (dict or list): A dictionary or a list of strings in
                the following format ``["PASSWORD=xxx"]`` or
                ``{"PASSWORD": "xxx"}``.
            workdir (str): Path to working directory for this exec session
            detach_keys (str): Override the key sequence for detaching
                a container. Format is a single character `[a-Z]`
                or `ctrl-<value>` where `<value>` is one of:
                `a-z`, `@`, `^`, `[`, `,` or `_`.
                ~/.docker/config.json is used by default.

        Returns:
            (dict): A dictionary with an exec ``Id`` key.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def exec_inspect(self, exec_id):
        """
        Return low-level information about an exec command.

        Args:
            exec_id (str): ID of the exec instance

        Returns:
            (dict): Dictionary of values returned by the endpoint.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def exec_resize(self, exec_id, height=None, width=None) -> None:
        """
        Resize the tty session used by the specified exec command.

        Args:
            exec_id (str): ID of the exec instance
            height (int): Height of tty session
            width (int): Width of tty session
        """

    def exec_start(
        self, exec_id, detach: bool = False, tty: bool = False, stream: bool = False, socket: bool = False, demux: bool = False
    ):
        """
        Start a previously set up exec instance.

        Args:
            exec_id (str): ID of the exec instance
            detach (bool): If true, detach from the exec command.
                Default: False
            tty (bool): Allocate a pseudo-TTY. Default: False
            stream (bool): Return response data progressively as an iterator
                of strings, rather than a single string.
            socket (bool): Return the connection socket to allow custom
                read/write operations. Must be closed by the caller when done.
            demux (bool): Return stdout and stderr separately

        Returns:

            (generator or str or tuple): If ``stream=True``, a generator
            yielding response chunks. If ``socket=True``, a socket object for
            the connection. A string containing response data otherwise. If
            ``demux=True``, a tuple with two elements of type byte: stdout and
            stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
