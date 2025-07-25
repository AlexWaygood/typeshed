""" """

def pre_read_control(attributes, criticality: bool = False):
    """Create a pre-read control for a request.
    When passed as a control to the controls parameter of an operation, it will
    return the value in `Connection.result` before the operation took place.
    """

def post_read_control(attributes, criticality: bool = False):
    """Create a post-read control for a request.
    When passed as a control to the controls parameter of an operation, it will
    return the value in `Connection.result` after the operation took place.
    """
