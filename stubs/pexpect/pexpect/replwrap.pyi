"""Generic wrapper for read-eval-print-loops, a.k.a. interactive shells"""

import sys
from _typeshed import Incomplete

PY3: Incomplete
basestring = str
PEXPECT_PROMPT: str
PEXPECT_CONTINUATION_PROMPT: str

class REPLWrapper:
    """Wrapper for a REPL.

    :param cmd_or_spawn: This can either be an instance of :class:`pexpect.spawn`
      in which a REPL has already been started, or a str command to start a new
      REPL process.
    :param str orig_prompt: The prompt to expect at first.
    :param str prompt_change: A command to change the prompt to something more
      unique. If this is ``None``, the prompt will not be changed. This will
      be formatted with the new and continuation prompts as positional
      parameters, so you can use ``{}`` style formatting to insert them into
      the command.
    :param str new_prompt: The more unique prompt to expect after the change.
    :param str extra_init_cmd: Commands to do extra initialisation, such as
      disabling pagers.
    """

    child: Incomplete
    prompt: Incomplete
    continuation_prompt: Incomplete
    def __init__(
        self,
        cmd_or_spawn,
        orig_prompt,
        prompt_change,
        new_prompt="[PEXPECT_PROMPT>",
        continuation_prompt="[PEXPECT_PROMPT+",
        extra_init_cmd=None,
    ) -> None: ...
    def set_prompt(self, orig_prompt, prompt_change) -> None: ...
    def run_command(self, command, timeout: float | None = -1, async_: bool = False):
        """Send a command to the REPL, wait for and return output.

        :param str command: The command to send. Trailing newlines are not needed.
          This should be a complete block of input that will trigger execution;
          if a continuation prompt is found after sending input, :exc:`ValueError`
          will be raised.
        :param int timeout: How long to wait for the next prompt. -1 means the
          default from the :class:`pexpect.spawn` object (default 30 seconds).
          None means to wait indefinitely.
        :param bool async_: On Python 3.4, or Python 3.3 with asyncio
          installed, passing ``async_=True`` will make this return an
          :mod:`asyncio` Future, which you can yield from to get the same
          result that this method would normally give directly.
        """

def python(command: str = sys.executable):
    """Start a Python shell and return a :class:`REPLWrapper` object."""

def bash(command: str = "bash"):
    """Start a bash shell and return a :class:`REPLWrapper` object."""

def zsh(command: str = "zsh", args=("--no-rcs", "-V", "+Z")):
    """Start a zsh shell and return a :class:`REPLWrapper` object."""
