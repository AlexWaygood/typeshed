"""A friendly Python SFTP interface."""

from collections.abc import Callable, Sequence
from contextlib import AbstractContextManager
from stat import S_IMODE as S_IMODE
from types import TracebackType
from typing import IO, Literal
from typing_extensions import Self, TypeAlias

import paramiko
from paramiko import AuthenticationException as AuthenticationException
from pysftp.exceptions import (
    ConnectionException as ConnectionException,
    CredentialException as CredentialException,
    HostKeysException as HostKeysException,
)
from pysftp.helpers import (
    WTCallbacks as WTCallbacks,
    _PathCallback,
    cd as cd,
    known_hosts as known_hosts,
    path_advance as path_advance,
    path_retreat as path_retreat,
    reparent as reparent,
    st_mode_to_int as st_mode_to_int,
    walktree as walktree,
)

class CnOpts:
    """additional connection options beyond authentication

    :ivar bool|str log: initial value: False -
        log connection/handshake details? If set to True,
        pysftp creates a temporary file and logs to that.  If set to a valid
        path and filename, pysftp logs to that.  The name of the logfile can
        be found at  ``.logfile``
    :ivar bool compression: initial value: False - Enables compression on the
        transport, if set to True.
    :ivar list|None ciphers: initial value: None -
        List of ciphers to use in order.
    :ivar paramiko.hostkeys.HostKeys|None hostkeys: HostKeys object to use for
        host key checking.
    :param filepath|None knownhosts: initial value: None - file to load
        hostkeys. If not specified, uses ~/.ssh/known_hosts
    :returns: (obj) CnOpts - A connection options object, used for passing
        extended options to the Connection
    :raises HostKeysException:
    """

    log: bool | str
    compression: bool
    ciphers: Sequence[str] | None
    hostkeys: paramiko.HostKeys | None
    def __init__(self, knownhosts: str | None = None) -> None: ...
    def get_hostkey(self, host: str) -> paramiko.PKey:
        """return the matching hostkey to use for verification for the host
        indicated or raise an SSHException
        """

_Callback: TypeAlias = Callable[[int, int], object]
_Path: TypeAlias = str | bytes

class Connection:
    """Connects and logs into the specified hostname.
    Arguments that are not given are guessed from the environment.

    :param str host:
        The Hostname or IP of the remote machine.
    :param str|None username: *Default: None* -
        Your username at the remote machine.
    :param str|obj|None private_key: *Default: None* -
        path to private key file(str) or paramiko.AgentKey
    :param str|None password: *Default: None* -
        Your password at the remote machine.
    :param int port: *Default: 22* -
        The SSH port of the remote machine.
    :param str|None private_key_pass: *Default: None* -
        password to use, if private_key is encrypted.
    :param list|None ciphers: *Deprecated* -
        see ``pysftp.CnOpts`` and ``cnopts`` parameter
    :param bool|str log: *Deprecated* -
        see ``pysftp.CnOpts`` and ``cnopts`` parameter
    :param None|CnOpts cnopts: *Default: None* - extra connection options
        set in a CnOpts object.
    :param str|None default_path: *Default: None* -
        set a default path upon connection.
    :returns: (obj) connection to the requested host
    :raises ConnectionException:
    :raises CredentialException:
    :raises SSHException:
    :raises AuthenticationException:
    :raises PasswordRequiredException:
    :raises HostKeysException:

    """

    def __init__(
        self,
        host: str,
        username: str | None = None,
        private_key: str | paramiko.RSAKey | paramiko.AgentKey | None = None,
        password: str | None = None,
        port: int = 22,
        private_key_pass: str | None = None,
        ciphers: Sequence[str] | None = None,
        log: bool | str = False,
        cnopts: CnOpts | None = None,
        default_path: _Path | None = None,
    ) -> None: ...
    @property
    def pwd(self) -> str:
        """return the current working directory

        :returns: (str) current working directory

        """

    def get(
        self, remotepath: _Path, localpath: _Path | None = None, callback: _Callback | None = None, preserve_mtime: bool = False
    ) -> None:
        """Copies a file between the remote host and the local host.

        :param str remotepath: the remote path and filename, source
        :param str localpath:
            the local path and filename to copy, destination. If not specified,
            file is copied to local current working directory
        :param callable callback:
            optional callback function (form: ``func(int, int)``) that accepts
            the bytes transferred so far and the total bytes to be transferred.
        :param bool preserve_mtime:
            *Default: False* - make the modification time(st_mtime) on the
            local file match the time on the remote. (st_atime can differ
            because stat'ing the localfile can/does update it's st_atime)

        :returns: None

        :raises: IOError

        """

    def get_d(self, remotedir: _Path, localdir: _Path, preserve_mtime: bool = False) -> None:
        """get the contents of remotedir and write to locadir. (non-recursive)

        :param str remotedir: the remote directory to copy from (source)
        :param str localdir: the local directory to copy to (target)
        :param bool preserve_mtime: *Default: False* -
            preserve modification time on files

        :returns: None

        :raises:
        """

    def get_r(self, remotedir: _Path, localdir: _Path, preserve_mtime: bool = False) -> None:
        """recursively copy remotedir structure to localdir

        :param str remotedir: the remote directory to copy from
        :param str localdir: the local directory to copy to
        :param bool preserve_mtime: *Default: False* -
            preserve modification time on files

        :returns: None

        :raises:

        """

    def getfo(self, remotepath: _Path, flo: IO[bytes], callback: _Callback | None = None) -> int:
        """Copy a remote file (remotepath) to a file-like object, flo.

        :param str remotepath: the remote path and filename, source
        :param flo: open file like object to write, destination.
        :param callable callback:
            optional callback function (form: ``func(int, int``)) that accepts
            the bytes transferred so far and the total bytes to be transferred.

        :returns: (int) the number of bytes written to the opened file object

        :raises: Any exception raised by operations will be passed through.

        """

    def put(
        self,
        localpath: _Path,
        remotepath: _Path | None = None,
        callback: _Callback | None = None,
        confirm: bool = True,
        preserve_mtime: bool = False,
    ) -> paramiko.SFTPAttributes:
        """Copies a file between the local host and the remote host.

        :param str localpath: the local path and filename
        :param str remotepath:
            the remote path, else the remote :attr:`.pwd` and filename is used.
        :param callable callback:
            optional callback function (form: ``func(int, int``)) that accepts
            the bytes transferred so far and the total bytes to be transferred.
        :param bool confirm:
            whether to do a stat() on the file afterwards to confirm the file
            size
        :param bool preserve_mtime:
            *Default: False* - make the modification time(st_mtime) on the
            remote file match the time on the local. (st_atime can differ
            because stat'ing the localfile can/does update it's st_atime)

        :returns:
            (obj) SFTPAttributes containing attributes about the given file

        :raises IOError: if remotepath doesn't exist
        :raises OSError: if localpath doesn't exist

        """

    def put_d(self, localpath: _Path, remotepath: _Path, confirm: bool = True, preserve_mtime: bool = False) -> None:
        """Copies a local directory's contents to a remotepath

        :param str localpath: the local path to copy (source)
        :param str remotepath:
            the remote path to copy to (target)
        :param bool confirm:
            whether to do a stat() on the file afterwards to confirm the file
            size
        :param bool preserve_mtime:
            *Default: False* - make the modification time(st_mtime) on the
            remote file match the time on the local. (st_atime can differ
            because stat'ing the localfile can/does update it's st_atime)

        :returns: None

        :raises IOError: if remotepath doesn't exist
        :raises OSError: if localpath doesn't exist
        """

    def put_r(self, localpath: _Path, remotepath: _Path, confirm: bool = True, preserve_mtime: bool = False) -> None:
        """Recursively copies a local directory's contents to a remotepath

        :param str localpath: the local path to copy (source)
        :param str remotepath:
            the remote path to copy to (target)
        :param bool confirm:
            whether to do a stat() on the file afterwards to confirm the file
            size
        :param bool preserve_mtime:
            *Default: False* - make the modification time(st_mtime) on the
            remote file match the time on the local. (st_atime can differ
            because stat'ing the localfile can/does update it's st_atime)

        :returns: None

        :raises IOError: if remotepath doesn't exist
        :raises OSError: if localpath doesn't exist
        """

    def putfo(
        self,
        flo: IO[bytes],
        remotepath: _Path | None = None,
        file_size: int = 0,
        callback: _Callback | None = None,
        confirm: bool = True,
    ) -> paramiko.SFTPAttributes:
        """Copies the contents of a file like object to remotepath.

        :param flo: a file-like object that supports .read()
        :param str remotepath: the remote path.
        :param int file_size:
            the size of flo, if not given the second param passed to the
            callback function will always be 0.
        :param callable callback:
            optional callback function (form: ``func(int, int``)) that accepts
            the bytes transferred so far and the total bytes to be transferred.
        :param bool confirm:
            whether to do a stat() on the file afterwards to confirm the file
            size

        :returns:
            (obj) SFTPAttributes containing attributes about the given file

        :raises: TypeError, if remotepath not specified, any underlying error

        """

    def execute(self, command: str) -> list[str]:
        """Execute the given commands on a remote machine.  The command is
        executed without regard to the remote :attr:`.pwd`.

        :param str command: the command to execute.

        :returns: (list of str) representing the results of the command

        :raises: Any exception raised by command will be passed through.

        """

    def cd(self, remotepath: _Path | None = None) -> AbstractContextManager[None]:  # noqa: F811
        """context manager that can change to a optionally specified remote
        directory and restores the old pwd on exit.

        :param str|None remotepath: *Default: None* -
            remotepath to temporarily make the current directory
        :returns: None
        :raises: IOError, if remote path doesn't exist
        """

    def chdir(self, remotepath: _Path) -> None:
        """change the current working directory on the remote

        :param str remotepath: the remote path to change to

        :returns: None

        :raises: IOError, if path does not exist

        """

    def cwd(self, remotepath: _Path) -> None:
        """change the current working directory on the remote

        :param str remotepath: the remote path to change to

        :returns: None

        :raises: IOError, if path does not exist

        """

    def chmod(self, remotepath: _Path, mode: int = 777) -> None:
        """set the mode of a remotepath to mode, where mode is an integer
        representation of the octal mode to use.

        :param str remotepath: the remote path/file to modify
        :param int mode: *Default: 777* -
            int representation of octal mode for directory

        :returns: None

        :raises: IOError, if the file doesn't exist

        """

    def chown(self, remotepath: _Path, uid: int | None = None, gid: int | None = None) -> None:
        """set uid and/or gid on a remotepath, you may specify either or both.
        Unless you have **permission** to do this on the remote server, you
        will raise an IOError: 13 - permission denied

        :param str remotepath: the remote path/file to modify
        :param int uid: the user id to set on the remotepath
        :param int gid: the group id to set on the remotepath

        :returns: None

        :raises:
            IOError, if you don't have permission or the file doesn't exist

        """

    def getcwd(self) -> str:
        """return the current working directory on the remote. This is a wrapper
        for paramiko's method and not to be confused with the SFTP command,
        cwd.

        :returns: (str) the current remote path. None, if not set.

        """

    def listdir(self, remotepath: _Path = ".") -> list[str]:
        """return a list of files/directories for the given remote path.
        Unlike, paramiko, the directory listing is sorted.

        :param str remotepath: path to list on the server

        :returns: (list of str) directory entries, sorted

        """

    def listdir_attr(self, remotepath: _Path = ".") -> list[paramiko.SFTPAttributes]:
        """return a list of SFTPAttribute objects of the files/directories for
        the given remote path. The list is in arbitrary order. It does not
        include the special entries '.' and '..'.

        The returned SFTPAttributes objects will each have an additional field:
        longname, which may contain a formatted string of the file's
        attributes, in unix format. The content of this string will depend on
        the SFTP server.

        :param str remotepath: path to list on the server

        :returns: (list of SFTPAttributes), sorted

        """

    def mkdir(self, remotepath: _Path, mode: int = 777) -> None:
        """Create a directory named remotepath with mode. On some systems,
        mode is ignored. Where it is used, the current umask value is first
        masked out.

        :param str remotepath: directory to create`
        :param int mode: *Default: 777* -
            int representation of octal mode for directory

        :returns: None

        """

    def normalize(self, remotepath: _Path) -> str:
        """Return the expanded path, w.r.t the server, of a given path.  This
        can be used to resolve symlinks or determine what the server believes
        to be the :attr:`.pwd`, by passing '.' as remotepath.

        :param str remotepath: path to be normalized

        :return: (str) normalized form of the given path

        :raises: IOError, if remotepath can't be resolved
        """

    def isdir(self, remotepath: _Path) -> bool:
        """return true, if remotepath is a directory

        :param str remotepath: the path to test

        :returns: (bool)

        """

    def isfile(self, remotepath: _Path) -> bool:
        """return true if remotepath is a file

        :param str remotepath: the path to test

        :returns: (bool)

        """

    def makedirs(self, remotedir: _Path, mode: int = 777) -> None:
        """create all directories in remotedir as needed, setting their mode
        to mode, if created.

        If remotedir already exists, silently complete. If a regular file is
        in the way, raise an exception.

        :param str remotedir: the directory structure to create
        :param int mode: *Default: 777* -
            int representation of octal mode for directory

        :returns: None

        :raises: OSError

        """

    def readlink(self, remotelink: _Path) -> str:
        """Return the target of a symlink (shortcut).  The result will be
        an absolute pathname.

        :param str remotelink: remote path of the symlink

        :return: (str) absolute path to target

        """

    def remove(self, remotefile: _Path) -> None:
        """remove the file @ remotefile, remotefile may include a path, if no
        path, then :attr:`.pwd` is used.  This method only works on files

        :param str remotefile: the remote file to delete

        :returns: None

        :raises: IOError

        """

    def unlink(self, remotefile: _Path) -> None:
        """remove the file @ remotefile, remotefile may include a path, if no
        path, then :attr:`.pwd` is used.  This method only works on files

        :param str remotefile: the remote file to delete

        :returns: None

        :raises: IOError

        """

    def rmdir(self, remotepath: _Path) -> None:
        """remove remote directory

        :param str remotepath: the remote directory to remove

        :returns: None

        """

    def rename(self, remote_src: _Path, remote_dest: _Path) -> None:
        """rename a file or directory on the remote host.

        :param str remote_src: the remote file/directory to rename

        :param str remote_dest: the remote file/directory to put it

        :returns: None

        :raises: IOError

        """

    def stat(self, remotepath: _Path) -> paramiko.SFTPAttributes:
        """return information about file/directory for the given remote path

        :param str remotepath: path to stat

        :returns: (obj) SFTPAttributes

        """

    def lstat(self, remotepath: _Path) -> paramiko.SFTPAttributes:
        """return information about file/directory for the given remote path,
        without following symbolic links. Otherwise, the same as .stat()

        :param str remotepath: path to stat

        :returns: (obj) SFTPAttributes object

        """

    def close(self) -> None:
        """Closes the connection and cleans up."""

    def open(self, remote_file: _Path, mode: str = "r", bufsize: int = -1) -> paramiko.SFTPFile:
        """Open a file on the remote server.

        See http://paramiko-docs.readthedocs.org/en/latest/api/sftp.html for
        details.

        :param str remote_file: name of the file to open.
        :param str mode:
            mode (Python-style) to open file (always assumed binary)
        :param int bufsize: *Default: -1* - desired buffering

        :returns: (obj) SFTPFile, a handle the remote open file

        :raises: IOError, if the file could not be opened.

        """

    def exists(self, remotepath: _Path) -> bool:
        """Test whether a remotepath exists.

        :param str remotepath: the remote path to verify

        :returns: (bool) True, if remotepath exists, else False

        """

    def lexists(self, remotepath: _Path) -> bool:
        """Test whether a remotepath exists.  Returns True for broken symbolic
        links

        :param str remotepath: the remote path to verify

        :returns: (bool), True, if lexists, else False

        """

    def symlink(self, remote_src: _Path, remote_dest: _Path) -> None:
        """create a symlink for a remote file on the server

        :param str remote_src: path of original file
        :param str remote_dest: path of the created symlink

        :returns: None

        :raises:
            any underlying error, IOError if something already exists at
            remote_dest

        """

    def truncate(self, remotepath: _Path, size: int) -> int:
        """Change the size of the file specified by path. Used to modify the
        size of the file, just like the truncate method on Python file objects.
        The new file size is confirmed and returned.

        :param str remotepath: remote file path to modify
        :param int|long size: the new file size

        :returns: (int) new size of file

        :raises: IOError, if file does not exist

        """

    def walktree(  # noqa: F811
        self,
        remotepath: _Path,
        fcallback: _PathCallback,
        dcallback: _PathCallback,
        ucallback: _PathCallback,
        recurse: bool = True,
    ) -> None:
        """recursively descend, depth first, the directory tree rooted at
        remotepath, calling discreet callback functions for each regular file,
        directory and unknown file type.

        :param str remotepath:
            root of remote directory to descend, use '.' to start at
            :attr:`.pwd`
        :param callable fcallback:
            callback function to invoke for a regular file.
            (form: ``func(str)``)
        :param callable dcallback:
            callback function to invoke for a directory. (form: ``func(str)``)
        :param callable ucallback:
            callback function to invoke for an unknown file type.
            (form: ``func(str)``)
        :param bool recurse: *Default: True* - should it recurse

        :returns: None

        :raises:

        """

    @property
    def sftp_client(self) -> paramiko.SFTPClient:
        """give access to the underlying, connected paramiko SFTPClient object

        see http://paramiko-docs.readthedocs.org/en/latest/api/sftp.html

        :params: None

        :returns: (obj) the active SFTPClient object

        """

    @property
    def active_ciphers(self) -> tuple[str, str]:
        """Get tuple of currently used local and remote ciphers.

        :returns:
            (tuple of  str) currently used ciphers (local_cipher,
            remote_cipher)

        """

    @property
    def active_compression(self) -> tuple[str, str]:
        """Get tuple of currently used local and remote compression.

        :returns:
            (tuple of  str) currently used compression (local_compression,
            remote_compression)

        """

    @property
    def security_options(self) -> paramiko.SecurityOptions:
        """return the available security options recognized by paramiko.

        :returns:
            (obj) security preferences of the ssh transport. These are tuples
            of acceptable `.ciphers`, `.digests`, `.key_types`, and key
            exchange algorithms `.kex`, listed in order of preference.

        """

    @property
    def logfile(self) -> str | Literal[False]:
        """return the name of the file used for logging or False it not logging

        :returns: (str)logfile or (bool) False

        """

    @property
    def timeout(self) -> float | None:
        """(float|None) *Default: None* -
            get or set the underlying socket timeout for pending read/write
            ops.

        :returns:
            (float|None) seconds to wait for a pending read/write operation
            before raising socket.timeout, or None for no timeout
        """

    @timeout.setter
    def timeout(self, val: float | None) -> None: ...
    @property
    def remote_server_key(self) -> paramiko.PKey:
        """return the remote server's key"""

    def __del__(self) -> None:
        """Attempt to clean up if not explicitly closed."""

    def __enter__(self) -> Self: ...
    def __exit__(
        self, etype: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> None: ...
