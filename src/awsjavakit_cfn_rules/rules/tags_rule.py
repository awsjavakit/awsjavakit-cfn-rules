from __future__ import annotations

from typing import List

from cfnlint.rules import CloudFormationLintRule, RuleMatch
from cfnlint.template.template import Template

from awsjavakit_cfn_rules.rules.utils.rule_id import RuleId
from awsjavakit_cfn_rules.rules.utils.config_reader import Config, FileConfigReader

SAMPLE_TEMPLATE_RULE_ID = "E9001"

EMPTY_DICT = {}


class TagsRule(CloudFormationLintRule):

    id:str = SAMPLE_TEMPLATE_RULE_ID
    shortdesc:str = "Missing Tags Rule for Lambdas"
    description:str = "A rule for checking that all lambdas have tags"
    tags = ["tags"]
    experimental = False

    def __init__(self,config: Config=None):
        super().__init__()
        if config is None:
            config_reader= FileConfigReader.default()
            self.config = config_reader.fetch_config(RuleId(SAMPLE_TEMPLATE_RULE_ID))
        else:
            self.config = config

    @staticmethod
    def create(config: Config) -> TagsRule:
        return TagsRule(config)



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
