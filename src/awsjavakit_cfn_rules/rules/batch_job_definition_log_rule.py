from __future__ import annotations

import logging
import sys
from collections.abc import Iterable
from typing import Any, ClassVar

import attrs
from cfnlint.rules import CloudFormationLintRule, RuleMatch
from cfnlint.template.template import Template

from awsjavakit_cfn_rules.rules.lambda_listens_to_event_bridge import EMPTY_STRING

EMPTY_DICT = {}

ERROR_MESSAGE = ("A BatchJobDefinition should have a valid log configuration and a log group with a retention period "
                 "if Cloudwatch is used")
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

RULE_ID: str = "E9005"


class BatchJobDefinitionLogRule(CloudFormationLintRule):

    id: str = RULE_ID
    shortdesc: str = "Ensure that Fargate Job definitions have defined a log group with retention period"
    description: str = "Ensure that Fargate Job definitions have defined a log group with retention period"
    tags = ["Fargate", "Cloudwatch", "logs"]
    experimental = False

    def __init__(self):
        super().__init__()
        self.configure()

    def match(self, cfn: Template) -> list[RuleMatch]:
        try:
            batch_job_definitions: dict[str, dict[str, Any]] = cfn.get_resources(BatchJobDefinitionEntry.type)
            job_definition_entries = map(lambda item: BatchJobDefinitionEntry(item[0], item[1]),
                                         batch_job_definitions.items())
            entries_logging_to_cloudwatch_without_log_group: Iterable[BatchJobDefinitionEntry] = \
                filter(lambda entry: entry.has_no_log_group(),job_definition_entries)
            matches: list[RuleMatch] = list(
                map(lambda entry: entry.to_rule_match(), entries_logging_to_cloudwatch_without_log_group))

            return matches
        except Exception as e:
            logger.error(str(e))
            raise e


@attrs.define
class BatchJobDefinitionEntry:
    type: ClassVar[str] = "AWS::Batch::JobDefinition"
    cloudwatch_log_driver: ClassVar[str] = "awslogs"
    key: str
    entry: dict[str, Any]

    def get_aws_log_group(self) -> str:
        return self.entry.get("Properties", EMPTY_DICT) \
            .get("ContainerProperties", EMPTY_DICT) \
            .get("LogConfiguration", EMPTY_DICT) \
            .get("Options", EMPTY_DICT) \
            .get("awslogs-group", EMPTY_STRING)

    def has_no_log_group(self):
        return self.is_sending_logs_to_cloudwatch() and \
            self.get_aws_log_group() == EMPTY_STRING

    def is_sending_logs_to_cloudwatch(self) -> bool:
        log_driver: str = self.entry.get("Properties", EMPTY_DICT) \
            .get("ContainerProperties", EMPTY_DICT) \
            .get("LogConfiguration", EMPTY_DICT) \
            .get("LogDriver", EMPTY_STRING)
        return log_driver == BatchJobDefinitionEntry.cloudwatch_log_driver

    def to_rule_match(self) -> RuleMatch:
        return RuleMatch(["Resources", self.key], ERROR_MESSAGE)
