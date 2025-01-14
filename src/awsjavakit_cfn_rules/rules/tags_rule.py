from __future__ import annotations

from typing import List

from cfnlint.rules import CloudFormationLintRule, RuleMatch
from cfnlint.template.template import Template

CONFIG_DEFINITION = {"expectedTags": {"default": {}, "type": "list", "itemtype": "string"}}

SAMPLE_TEMPLATE_RULE_ID = "E9001"

EMPTY_DICT = {}


class TagsRule(CloudFormationLintRule):

    id:str = SAMPLE_TEMPLATE_RULE_ID
    shortdesc:str = "Missing Tags Rule for Lambdas"
    description:str = "A rule for checking that all lambdas have the required tags"
    tags = ["tags"]
    experimental = False

    def __init__(self):
        super().__init__()
        self.config_definition = CONFIG_DEFINITION
        self.configure()


    def match(self, cfn: Template) -> List[RuleMatch]:
        matches = []

        for key, value in cfn.get_resources(["AWS::Lambda::Function"]).items():
            tags: dict = value.get("Tags", EMPTY_DICT)
            expected_tags = self.config.get("expectedTags")
            missing_tags= list(filter(lambda expected: (expected not in tags),expected_tags))
            if self._is_not_empty_(missing_tags):
                matches.append(RuleMatch(path=["Resources", value],
                                         message=f"Lambda Function is missing required tags:{str(missing_tags)}"))
        return matches

    def _is_not_empty_(self, tags: List[str]) -> bool:
        return not (tags is None or tags == [])
