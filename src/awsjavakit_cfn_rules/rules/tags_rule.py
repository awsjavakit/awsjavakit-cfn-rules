from __future__ import annotations

from typing import Any, List

from attrs import define
from cfnlint.rules import CloudFormationLintRule, RuleMatch
from cfnlint.template.template import Template

EXPECTED_TAGS_FIELD_NAME = "expected_tags"

CONFIG_DEFINITION = {EXPECTED_TAGS_FIELD_NAME: {"default": [], "type": "list", "itemtype": "string"}}

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
        for key, value in cfn.get_resources(["AWS::Lambda::Function"]).items():
            tags: List[str] = self._extractTags_(value)
            missing_tags = self._calculate_missing_tags_(tags,tags_rule_config)

            if self._is_not_empty_(missing_tags):
                matches.append(RuleMatch(path=["Resources", value],
                                         message=f"Lambda Function is missing required tags:{str(missing_tags)}"))
        return matches

    def _extractTags_(self, value) -> List[str]:
        tagEntries = value.get("Properties").get("Tags")
        tagNames = list(map(lambda tagEntry: tagEntry.get("Key"), tagEntries))
        return tagNames

    def _calculate_missing_tags_(self, tags: List[str], tags_rule_config: TagsRuleConfig) -> List[str]:
        return list(filter(lambda expected: (expected not in tags), tags_rule_config.expected_tags()))

    def _is_not_empty_(self, tags: List[str]) -> bool:
        return not (tags is None or tags == [])


@define
class TagsRuleConfig:
    cfnlint_config: dict[str, Any]

    def expected_tags(self):
        return self.cfnlint_config.get(EXPECTED_TAGS_FIELD_NAME)
