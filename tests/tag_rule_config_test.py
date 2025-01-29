from hamcrest import assert_that, contains_inanyorder

from  awsjavakit_cfn_rules.rules import tags_checker
from awsjavakit_cfn_rules.rules.tags_checker import TagRule, TagsRuleConfig

# pylint: disable=too-few-public-methods
class TagRuleConfigTest:

    @staticmethod
    def should_create_tag_rules():
        config_yaml ={
            tags_checker.EXPECTED_TAGS_FIELD_NAME:
                {
                    "tag1":["ResourceANotRequiringTag1","ResourceBNotRequiringTag1"],
                    "tag2": ["ResourceCNotRequiringTag2", "ResourceDNotRequiringTag1"]

                }
        }
        config=TagsRuleConfig(config_yaml)
        rules = config.tag_rules()
        expected =[
            TagRule(expected_tag="tag1",
                    excluded_resource_types=["ResourceANotRequiringTag1", "ResourceBNotRequiringTag1"]),
            TagRule(expected_tag="tag2",
                    excluded_resource_types=["ResourceCNotRequiringTag2", "ResourceDNotRequiringTag1"])
        ]
        assert_that(rules,contains_inanyorder(*expected))
