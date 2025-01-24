from __future__ import annotations

from typing import Any, List

from attrs import define
from cfnlint.rules import CloudFormationLintRule, RuleMatch
from cfnlint.template.template import Template

EXPECTED_TAGS_FIELD_NAME = "expected_tags"

CONFIG_DEFINITION = {
    EXPECTED_TAGS_FIELD_NAME: {"default": [], "type": "list", "itemtype": "string"}
}

NON_TAGGABLE_RESOURCES = {
    "AWS::IAM::Policy": True,
    "AWS::IAM::ManagedPolicy": True,
}

SAMPLE_TEMPLATE_RULE_ID = "E9001"

EMPTY_DICT = {}


class TagsRule(CloudFormationLintRule):

    id: str = SAMPLE_TEMPLATE_RULE_ID
    shortdesc: str = "Missing Tags Rule for Lambdas"
    description: str = "A rule for checking that all lambdas have the required tags"
    tags = ["tags"]
    experimental = False

    def __init__(self):
        super().__init__()
        self.config_definition = CONFIG_DEFINITION
        self.configure()

    def match(self, cfn: Template) -> List[RuleMatch]:
        matches = []
        tags_rule_config = TagsRuleConfig(self.config)

        for _, value in cfn.get_resources().items():
            if self._is_non_taggable_resource_(value):
                continue
            tags: List[str] = self._extract_tags_(value)
            missing_tags = self._calculate_missing_tags_(tags, tags_rule_config)

            if self._is_not_empty_(missing_tags):
                matches.append(RuleMatch(path=["Resources", value],
                                         message=self._construct_message_(missing_tags)))
        return matches

    def _is_non_taggable_resource_(self, template: dict) -> bool:
        return NON_TAGGABLE_RESOURCES.get(template.get("Type")) is True

    def _extract_tags_(self, value) -> List[str]:
        tag_entries = value.get("Properties").get("Tags")
        tag_names = list(map(lambda tagEntry: tagEntry.get("Key"), tag_entries))
        return tag_names

    def _calculate_missing_tags_(self, tags: List[str], tags_rule_config: TagsRuleConfig) -> List[str]:
        return list(filter(lambda expected: (expected not in tags), tags_rule_config.expected_tags()))

    def _is_not_empty_(self, tags: List[str]) -> bool:
        return not (tags is None or tags == [])

    def _construct_message_(self, missing_tags):
        return f"Resource is missing required tags:{str(missing_tags)}"


@define
class TagsRuleConfig:
    cfnlint_config: dict[str, Any]

    def expected_tags(self):
        return self.cfnlint_config.get(EXPECTED_TAGS_FIELD_NAME)
