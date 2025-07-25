from _typeshed import Incomplete
from decimal import Decimal
from typing import Final

from braintree.add_on import AddOn
from braintree.descriptor import Descriptor
from braintree.discount import Discount
from braintree.resource import Resource
from braintree.subscription_status_event import SubscriptionStatusEvent
from braintree.transaction import Transaction

class Subscription(Resource):
    """
    A class representing a Subscription.

    An example of creating a subscription with all available fields::

        result = braintree.Subscription.create({
            "id": "my_subscription_id",
            "merchant_account_id": "merchant_account_one",
            "payment_method_token": "my_payment_token",
            "plan_id": "some_plan_id",
            "price": "29.95",
            "trial_duration": 1,
            "trial_duration_unit": braintree.Subscription.TrialDurationUnit.Month,
            "trial_period": True
        })

    For more information on Subscriptions, see https://developer.paypal.com/braintree/docs/reference/request/subscription/create/python

    """

    class TrialDurationUnit:
        """
        Constants representing trial duration units.  Available types are:

        * braintree.Subscription.TrialDurationUnit.Day
        * braintree.Subscription.TrialDurationUnit.Month
        """

        Day: Final = "day"
        Month: Final = "month"

    class Source:
        Api: Final = "api"
        ControlPanel: Final = "control_panel"
        Recurring: Final = "recurring"

    class Status:
        """
        Constants representing subscription statuses.  Available statuses are:

        * braintree.Subscription.Status.Active
        * braintree.Subscription.Status.Canceled
        * braintree.Subscription.Status.Expired
        * braintree.Subscription.Status.PastDue
        * braintree.Subscription.Status.Pending
        """

        Active: Final = "Active"
        Canceled: Final = "Canceled"
        Expired: Final = "Expired"
        PastDue: Final = "Past Due"
        Pending: Final = "Pending"

    @staticmethod
    def create(params=None):
        """
        Create a Subscription

        Token and Plan are required:::

            result = braintree.Subscription.create({
                "payment_method_token": "my_payment_token",
                "plan_id": "some_plan_id",
            })

        """

    @staticmethod
    def create_signature(): ...
    @staticmethod
    def find(subscription_id):
        """
        Find a subscription given a subscription_id.  This does not return a result
        object.  This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>`
        if the provided subscription_id is not found. ::

            subscription = braintree.Subscription.find("my_subscription_id")
        """

    @staticmethod
    def retry_charge(subscription_id, amount=None, submit_for_settlement: bool = False): ...
    @staticmethod
    def update(subscription_id, params=None):
        """
        Update an existing subscription

        By subscription_id. The params are similar to create::


            result = braintree.Subscription.update("my_subscription_id", {
                "price": "9.99",
            })

        """

    @staticmethod
    def cancel(subscription_id):
        """
        Cancel a subscription

        By subscription_id::

            result = braintree.Subscription.cancel("my_subscription_id")

        """

    @staticmethod
    def search(*query):
        """
        Allows searching on subscriptions. There are two types of fields that are searchable: text and
        multiple value fields. Searchable text fields are:
        - plan_id
        - days_past_due

        Searchable multiple value fields are:
        - status

        For text fields, you can search using the following operators: ==, !=, starts_with, ends_with
        and contains. For multiple value fields, you can search using the in_list operator. An example::

            braintree.Subscription.search([
                braintree.SubscriptionSearch.plan_id.starts_with("abc"),
                braintree.SubscriptionSearch.days_past_due == "30",
                braintree.SubscriptionSearch.status.in_list([braintree.Subscription.Status.PastDue])
            ])
        """

    @staticmethod
    def update_signature(): ...
    price: Decimal
    balance: Decimal
    next_billing_period_amount: Decimal
    add_ons: list[AddOn]
    descriptor: Descriptor
    description: Incomplete
    discounts: list[Discount]
    status_history: list[SubscriptionStatusEvent]
    transactions: list[Transaction]
    def __init__(self, gateway, attributes) -> None: ...
