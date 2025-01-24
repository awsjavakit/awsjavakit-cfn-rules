from __future__ import annotations

from typing import Any, List

from attrs import define
from cfnlint.rules import CloudFormationLintRule, RuleMatch
from cfnlint.template.template import Template

EXPECTED_TAGS_FIELD_NAME = "expected_tags"

CONFIG_DEFINITION = {
    EXPECTED_TAGS_FIELD_NAME: {"default": [], "type": "list", "itemtype": "string"}
}

NON_TAGGABLE_RESOURCES = {"AWS::IAM::Policy",
                          "AWS::IAM::ManagedPolicy",
                          "AWS::CloudFormation::Stack",
                          "AWS::CloudWatch::Dashboard"}

SAMPLE_TEMPLATE_RULE_ID = "E9001"

EMPTY_DICT = {}


class TagsRule(CloudFormationLintRule):

    id: str = SAMPLE_TEMPLATE_RULE_ID
    shortdesc: str = "Missing Tags Rule for Resources"
    description: str = "A rule for checking that all resources have the required tags"
    tags = ["tags"]
    experimental = False

    def __init__(self):
        super().__init__()
        self.config_definition = CONFIG_DEFINITION
        self.configure()

    def match(self, cfn: Template) -> List[RuleMatch]:
        matches = []
        tags_rule_config = TagsRuleConfig(self.config)

        for resource_name, resource in cfn.get_resources().items():
            if self._is_non_taggable_resource_(resource):
                continue
            tags: List[str] = self._extract_tags_(resource)
            missing_tags = self._calculate_missing_tags_(tags, tags_rule_config)

            if self._is_not_empty_(missing_tags):
                matches.append(RuleMatch(path=["Resources", resource],
                                         message=self._construct_message_(missing_tags, resource_name,
                                                                          self._type_of_(resource))))
        return matches

    def _type_of_(self, resource):
        return resource.get("Type")

    def _is_non_taggable_resource_(self, resource: dict) -> bool:
        return self._type_of_(resource) in NON_TAGGABLE_RESOURCES

    def _extract_tags_(self, value) -> List[str]:

        tag_entries = self._extract_tags_as_non_none(value)
        tag_names = list(map(lambda tagEntry: tagEntry.get("Key"), tag_entries))
        return tag_names

    def _extract_tags_as_non_none(self, value):
        return value.get("Properties", {}).get("Tags", [])

    def _calculate_missing_tags_(self, tags: List[str], tags_rule_config: TagsRuleConfig) -> List[str]:
        return list(filter(lambda expected: (expected not in tags), tags_rule_config.expected_tags()))

    def _is_not_empty_(self, tags: List[str]) -> bool:
        return not (tags is None or tags == [])

    def _construct_message_(self, missing_tags,resource_name: str, resource_type:str) -> str:
        return f"Resource {resource_name}:{resource_type} is missing required tags:{str(missing_tags)}"


@define
class TagsRuleConfig:
    cfnlint_config: dict[str, Any]

    def expected_tags(self):
        return self.cfnlint_config.get(EXPECTED_TAGS_FIELD_NAME)
