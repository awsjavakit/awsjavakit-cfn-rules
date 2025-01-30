from hamcrest import assert_that, contains_inanyorder

from awsjavakit_cfn_rules.rules import tags_checker
from awsjavakit_cfn_rules.rules.tags_checker import TagRule, TagsRuleConfig


# pylint: disable=too-few-public-methods
class TagRuleConfigTest:

    @staticmethod
    def should_create_tag_rules():
        config_yaml = {
            tags_checker.EXPECTED_TAGS_FIELD_NAME:
                [
                    "tag1",
                    "tag2"

                ]
        }
        config = TagsRuleConfig(config_yaml)
        rules = config.tag_rules()
        expected = [
            TagRule(expected_tag="tag1",
                    excluded_resource_types=[]),
            TagRule(expected_tag="tag2",
                    excluded_resource_types=[])
        ]
        assert_that(rules, contains_inanyorder(*expected))
