from typing import ClassVar

from braintree.attribute_getter import AttributeGetter

class PackageDetails(AttributeGetter):
    """
    A class representing the package tracking information of a transaction.

    An example of package details including all available fields::

        result = braintree.PackageDetails.create({
            "id": "my_id",
            "carrier": "a_carrier",
            "tracking_number": "my_tracking_number",
            "paypal_tracking_id": "my_paypal_tracking_id",
            "paypal_tracker_id": "my_paypal_tracker_id",
        })

    """

    detail_list: ClassVar[list[str]]
    def __init__(self, attributes) -> None: ...
