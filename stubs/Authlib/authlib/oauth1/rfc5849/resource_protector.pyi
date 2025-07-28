from authlib.oauth1.rfc5849.base_server import BaseServer

class ResourceProtector(BaseServer):
    def validate_request(self, method, uri, body, headers): ...
    def get_token_credential(self, request) -> None:
        """Fetch the token credential from data store like a database,
        framework should implement this function.

        :param request: OAuth1Request instance
        :return: Token model instance
        """
