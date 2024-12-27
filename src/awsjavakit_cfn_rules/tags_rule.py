from typing import List

from cfnlint.rules import CloudFormationLintRule, RuleMatch
from cfnlint.template.template import Template

SAMPLE_TEMPLATE_RULE_ID = "ES9002"

EMPTY_DICT = {}


class TagsRule(CloudFormationLintRule):

    id = SAMPLE_TEMPLATE_RULE_ID
    shortdesc = "Missing Tags Rule"
    description = "A rule for checking that all resources requiring tags have tags"
    tags = ["tags"]
    experimental = False

    def match(self, cfn: Template) -> List[RuleMatch]:
        matches = []

        for key, value in cfn.get_resources(["AWS::Lambda::Function"]).items():
            tags: dict = value.get("Tags", EMPTY_DICT)

            if self.__is_empty_dict__(tags):
                matches.append(RuleMatch(path=["Resources", value],
                                         message="Lambda Function should be tagged"))
        return matches

    def __is_empty_dict__(self, tags: dict) -> bool:
        return tags is None or tags == EMPTY_DICT
