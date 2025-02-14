from __future__ import annotations

import numbers
from typing import List

from cfnlint.rules import CloudFormationLintRule, RuleMatch
from cfnlint.template.template import Template

TAGS_RULE_ID = "E9002"
LONG_POLLING_PROPERTY = "ReceiveMessageWaitTimeSeconds"
ERROR_MESSAGE = f"Queue should enable long polling by setting  {LONG_POLLING_PROPERTY} to non zero value"


class SqsLongPollingRule(CloudFormationLintRule):

    id: str = TAGS_RULE_ID
    shortdesc: str = "Ensure that long polling is enabled for SQS queue to avoid costs"
    description: str = "Ensure that long polling is enabled for SQS queue to avoid costs"
    tags = ["SQS", "long polling"]
    experimental = False

    def __init__(self):
        super().__init__()
        self.configure()

    def match(self, cfn: Template) -> List[RuleMatch]:
        queue_names_with_short_polling = SqsLongPollingRule._list_queues_with_short_polling_(cfn)
        matches = list(map(SqsLongPollingRule._construct_match_, queue_names_with_short_polling))
        return matches

    @staticmethod
    def _list_queues_with_short_polling_(cfn: Template) -> List[str]:
        queues = cfn.get_resources("AWS::SQS::Queue")
        return list(
            filter(lambda queue_name: SqsLongPollingRule._is_short_polling_(queues.get(queue_name)),queues.keys())
        )


    @staticmethod
    def _is_short_polling_(queue: dict) -> bool:
        long_property_value = queue.get("Properties", {}).get(LONG_POLLING_PROPERTY)
        return SqsLongPollingRule._is_not_a_number_(long_property_value) or long_property_value == 0

    @staticmethod
    def _is_not_a_number_( long_property_value) -> bool:
        return not isinstance(long_property_value, numbers.Number)

    @staticmethod
    def _construct_match_(queue_name: str) -> RuleMatch:
        return RuleMatch(["Resources", queue_name], ERROR_MESSAGE)
