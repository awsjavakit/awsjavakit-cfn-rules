from typing import List

from cfnlint.rules import CloudFormationLintRule, RuleMatch
from cfnlint.template.template import Template

SAMPLE_TEMPLATE_RULE_ID = "ES9001"

EMPTY_DICT = {}


class SampleTemplateRule(CloudFormationLintRule):

    id = SAMPLE_TEMPLATE_RULE_ID
    shortdesc = "Demo Rule"
    description = "A rule for checking that testing works"
    tags = ["lambda"]
    experimental = False

    def match(self, cfn: Template) -> List[RuleMatch]:
        matches = []

        for key, value in cfn.get_resources(["AWS::Lambda::Function"]).items():
            function_name = value.get("FunctionName", EMPTY_DICT)

            if function_name != "MyFunction":
                matches.append(RuleMatch(["Resources", key], "Function Name should be MyFunctionName"))
        return matches
