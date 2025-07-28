from _typeshed import Incomplete

from braintree.error_result import ErrorResult
from braintree.graphql import CreateCustomerSessionInput, CustomerRecommendationsInput, UpdateCustomerSessionInput
from braintree.successful_result import SuccessfulResult

class CustomerSessionGateway:
    """
    Creates and manages PayPal customer sessions.
    """

    gateway: Incomplete
    graphql_client: Incomplete
    def __init__(self, gateway) -> None: ...
    def create_customer_session(self, customer_session_input: CreateCustomerSessionInput) -> SuccessfulResult | ErrorResult:
        """
        Creates a new customer session.

        Example:
          customer_session = (
            CustomerSessionInput
            .builder()
            .email("test@example.com")
            .build()
          )

          create_input = (
            CreateCustomerSessionInput
            .builder()
            .customer(customer_session)
            .build()
          )

          result = gateway.customer_session.create_customer_session(create_input)

          if result.is_success:
            print(result.session_id)

        Args:
            CreateCustomerSessionInput: Input object for creating a customer session.

        Returns:
            (Successful|Error)Result: A result object with session ID if successful, or errors otherwise.

        Raises:
            UnexpectedError: If there is an unexpected error during the process.
        """

    def update_customer_session(
        self, update_customer_session_input: UpdateCustomerSessionInput
    ) -> SuccessfulResult | ErrorResult:
        """
        Updates an existing customer session.

        Example:
          customer_session = (
            CustomerSessionInput
            .builder()
            .email("test@example.com")
            .build()
          )

          update_input = (
            UpdateCustomerSessionInput
            .builder(session_id)
            .customer(customer_session)
            .build()
          )

          result = gateway.customer_session.update_customer_session(update_input)

          if result.is_success:
            print(result.session_id)

        Args:
            UpdateCustomerSessionInput: Input object for updating a customer session.

        Returns:
            (Successful|Error)Result: A result object with session ID if successful, or errors otherwise.

        Raises:
            UnexpectedError: If there is an unexpected error during the process.
        """

    def get_customer_recommendations(
        self, get_customer_recommendations_input: CustomerRecommendationsInput
    ) -> SuccessfulResult | ErrorResult:
        """
        Retrieves customer recommendations associated with a customer session.

        Example:

          recommendations_input = (
            CustomerRecommendationsInput
              .builder()
              .session_id(session_id)
              .build()
          )

          result = gateway.customer_session.get_customer_recommendations(recommendations_input)

          if result.is_success:
            print(result.customer_recommendations.recommendations.payment_recommendations)

        Args:
            GenerateCustomerRecommendationsInput: Input object for retrieving customer recommendations.

        Returns:
            (Successful|Error)Result: A result object containing a GenerateCustomerRecommendationsPayload and a success flag if successful, or errors otherwise.

        Raises:
            UnexpectedError: If there is an unexpected error during the process.
        """
