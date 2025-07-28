def patch() -> None:
    """
    Patch botocore client so it generates subsegments
    when calling AWS services.
    """
