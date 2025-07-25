from asgiref.server import StatelessServer
from channels.layers import BaseChannelLayer
from channels.utils import _ChannelApplication

class Worker(StatelessServer):
    """
    ASGI protocol server that surfaces events sent to specific channels
    on the channel layer into a single application instance.
    """

    channels: list[str]
    channel_layer: BaseChannelLayer

    def __init__(
        self, application: _ChannelApplication, channels: list[str], channel_layer: BaseChannelLayer, max_applications: int = 1000
    ) -> None: ...
    async def handle(self) -> None:
        """
        Listens on all the provided channels and handles the messages.
        """

    async def listener(self, channel: str) -> None:
        """
        Single-channel listener
        """
