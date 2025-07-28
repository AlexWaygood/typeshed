from typing import TypedDict, type_check_only
from typing_extensions import NotRequired

from .sampling_rule import SamplingRule, _Rule

@type_check_only
class _SamplingRule(TypedDict):
    version: NotRequired[int]
    default: _Rule
    rules: list[_Rule]

local_sampling_rule: _SamplingRule
SUPPORTED_RULE_VERSION: tuple[int, ...]

class LocalSampler:
    """
    The local sampler that holds either custom sampling rules
    or default sampling rules defined locally. The X-Ray recorder
    use it to calculate if this segment should be sampled or not
    when local rules are neccessary.
    """

    def __init__(self, rules: _SamplingRule = ...) -> None:
        """
        :param dict rules: a dict that defines custom sampling rules.
        An example configuration:
        {
            "version": 2,
            "rules": [
                {
                    "description": "Player moves.",
                    "host": "*",
                    "http_method": "*",
                    "url_path": "/api/move/*",
                    "fixed_target": 0,
                    "rate": 0.05
                }
            ],
            "default": {
                "fixed_target": 1,
                "rate": 0.1
            }
        }
        This example defines one custom rule and a default rule.
        The custom rule applies a five-percent sampling rate with no minimum
        number of requests to trace for paths under /api/move/. The default
        rule traces the first request each second and 10 percent of additional requests.
        The SDK applies custom rules in the order in which they are defined.
        If a request matches multiple custom rules, the SDK applies only the first rule.
        """

    def should_trace(self, sampling_req: SamplingRule | None = None) -> bool:
        """
        Return True if the sampler decide to sample based on input
        information and sampling rules. It will first check if any
        custom rule should be applied, if not it falls back to the
        default sampling rule.

        All optional arugments are extracted from incoming requests by
        X-Ray middleware to perform path based sampling.
        """

    def load_local_rules(self, rules: _SamplingRule) -> None: ...
