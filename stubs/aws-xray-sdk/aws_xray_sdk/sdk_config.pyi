from logging import Logger
from typing import ClassVar

log: Logger

class SDKConfig:
    """
    Global Configuration Class that defines SDK-level configuration properties.

    Enabling/Disabling the SDK:
        By default, the SDK is enabled unless if an environment variable AWS_XRAY_SDK_ENABLED
            is set. If it is set, it needs to be a valid string boolean, otherwise, it will default
            to true. If the environment variable is set, all calls to set_sdk_enabled() will
            prioritize the value of the environment variable.
        Disabling the SDK affects the recorder, patcher, and middlewares in the following ways:
        For the recorder, disabling automatically generates DummySegments for subsequent segments
            and DummySubsegments for subsegments created and thus not send any traces to the daemon.
        For the patcher, module patching will automatically be disabled. The SDK must be disabled
            before calling patcher.patch() method in order for this to function properly.
        For the middleware, no modification is made on them, but since the recorder automatically
            generates DummySegments for all subsequent calls, they will not generate segments/subsegments
            to be sent.

    Environment variables:
        "AWS_XRAY_SDK_ENABLED" - If set to 'false' disables the SDK and causes the explained above
            to occur.
    """

    XRAY_ENABLED_KEY: ClassVar[str]
    DISABLED_ENTITY_NAME: ClassVar[str]
    @classmethod
    def sdk_enabled(cls) -> bool:
        """
        Returns whether the SDK is enabled or not.
        """

    @classmethod
    def set_sdk_enabled(cls, value: bool | None) -> None:
        """
        Modifies the enabled flag if the "AWS_XRAY_SDK_ENABLED" environment variable is not set,
        otherwise, set the enabled flag to be equal to the environment variable. If the
        env variable is an invalid string boolean, it will default to true.

        :param bool value: Flag to set whether the SDK is enabled or disabled.

        Environment variables AWS_XRAY_SDK_ENABLED overrides argument value.
        """
