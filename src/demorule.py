from typing import List

from cfnlint.rules import CloudFormationLintRule, RuleMatch
from cfnlint.template.template import Template

class SampleTemplateRule(CloudFormationLintRule):

    id = "ES9001"  # noqa: VNE003
    shortdesc = "Lambda Event Source Mapping Destination"
    description = "Ensure Lambda event source mappings have a destination configured"
    source_url = "https://awslabs.github.io/serverless-rules/rules/lambda/eventsourcemapping_failure_destination/"
    tags = ["lambda"]
    experimental = False

    def match(self, cfn: Template) -> List[RuleMatch]:
        matches = []

        for key, value in cfn.get_resources(["AWS::Lambda::Function"]).items():
            tracing_mode = value.get("Properties", {}).get("TracingConfig", {}).get("Mode", None)

            if tracing_mode != "Active":
                matches.append(RuleMatch(["Resources", key], "Tracing Config has not been set to active"))
        return matches
