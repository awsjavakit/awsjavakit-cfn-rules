from typing import Any

import pytest
from hamcrest import assert_that, contains_inanyorder, empty, is_

from awsjavakit_cfn_rules.rules import tags_checker
from awsjavakit_cfn_rules.rules.tags_checker import TagRule, TagsRuleConfig
from awsjavakit_cfn_rules.utils.invalid_config_exception import InvalidConfigException


# pylint: disable=too-few-public-methods
class TagRuleConfigTest:

    @staticmethod
    def should_create_one_tag_rule_per_tag():
        expected_tags_field_name = tags_checker.EXPECTED_TAGS_FIELD_NAME
        config_json = {
            expected_tags_field_name:["tag1", "tag2"]
        }
        config = TagsRuleConfig(config_json)
        rules = config.tag_rules()
        expected = [
            TagRule(expected_tag="tag1"),
            TagRule(expected_tag="tag2")
        ]
        assert_that(rules, contains_inanyorder(*expected))
    
        
    @staticmethod
    def should_report_error_on_invalid_tag_rule_configuration():
        with pytest.raises(InvalidConfigException):
            config_json: dict[str,Any] = {tags_checker.EXPECTED_TAGS_FIELD_NAME:"someExpectedTag"}
            config = TagsRuleConfig(config_json) #type:ignore
            rules = config.tag_rules()
            assert_that(rules, is_(empty()))
