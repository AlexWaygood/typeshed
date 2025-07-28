"""Helper for the test suite - determines where to write output.

When our test suite runs as source, a script "test_foo.py" will typically
create "test_foo.pdf" alongside it.  But if you are testing a package of
compiled code inside a zip archive, this won't work.  This determines
where to write test suite output, creating a subdirectory of /tmp/ or
whatever if needed.

"""

def get_rl_tempdir(*subdirs: str) -> str: ...
def get_rl_tempfile(fn: str | None = None) -> str: ...

__all__ = ("get_rl_tempdir", "get_rl_tempdir")
