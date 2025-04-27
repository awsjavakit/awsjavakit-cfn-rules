from __future__ import annotations

import numbers
from collections.abc import Iterable
from pathlib import Path
from typing import List

from cfnlint.rules import CloudFormationLintRule, RuleMatch
from cfnlint.template.template import Template

RESOURCE_NAME = 0

RULE_ID: str = "E9003"

ERROR_MESSAGE: str = """
Lambda is listening to an EventBridge event directly.
Better to set up an SQS queue to listen to the Event Bridge event and the Lambda to listen to the SQS queue.
This way, you have better control over the parallelism. 
"""


class LambdaListensToEventBridgeRule(CloudFormationLintRule):

    id: str = RULE_ID
    shortdesc: str = "Ensure better event control by forwarding EventBridge events to an SQS queue first"
    description: str = "Ensure better event control by forwarding EventBridge events to an SQS queue first"
    tags = ["EventBridge", "SQS", "Lambda"]
    experimental = False

    def __init__(self):
        super().__init__()
        self.configure()

    def match(self, cfn: Template) -> list[RuleMatch]:
        rule_matches: Iterable[RuleMatch] = []

        event_rules = cfn.get_resources("AWS::Events::Rule")
        for key in event_rules.keys():
            value = event_rules.get(key)
            targets = value.get("Properties").get("Targets")
            lambda_function_targets = list(filter(lambda target: self._is_lambda_function_(target, cfn), targets))
            rule_matches = map(lambda target: self._create_match_(target), lambda_function_targets)

        return list(rule_matches)

    def _create_match_(self, target_arn) -> RuleMatch:
        return RuleMatch(["Resources", target_arn], ERROR_MESSAGE)

    def _extract_lambda_functions_(self, cfn) -> List[str]:
        return list(cfn.get_resources("AWS::Lambda::Function").keys())

    
    @staticmethod
    def _is_not_a_number_(long_property_value) -> bool:
        return not isinstance(long_property_value, numbers.Number)

    @staticmethod
    def _construct_match_(queue_name: str) -> RuleMatch:
        return RuleMatch(["Resources", queue_name], ERROR_MESSAGE)

    def _is_lambda_function_(self, target_arn: str, cfn: Template):
        return target_arn in self._extract_lambda_functions_(cfn)
