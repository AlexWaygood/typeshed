import traceback

def get_stacktrace(limit: int | None = None) -> list[traceback.FrameSummary]:
    """
    Get a full stacktrace for the current state of execution.

    Include the current state of the stack, minus this function.
    If there is an active exception, include the stacktrace information from
    the exception as well.

    :param int limit:
        Optionally limit stack trace size results. This parmaeters has the same
        meaning as the `limit` parameter in `traceback.print_stack`.
    :returns:
        List of stack trace objects, in the same form as
        `traceback.extract_stack`.
    """
