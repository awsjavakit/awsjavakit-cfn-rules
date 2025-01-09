from __future__ import annotations

from typing import List

import cfnlint
import pytest
from assertpy import assert_that
from cfnlint import Template, core

from awsjavakit_cfn_rules.rules import tags_rule
from awsjavakit_cfn_rules.rules import RULES_FOLDER
from awsjavakit_cfn_rules.rules.tags_rule import TagsRule
from awsjavakit_cfn_rules.rules.utils.config_reader import Config
from tests import RESOURCES
from tests.test_utils import ParsedJson, TestUtils

DEMO_RULE = "ES9001"



class TagsRuleTest:

    @staticmethod
    @pytest.fixture
    def demo_templates() -> List[ParsedJson]:

        templates_folder = (RESOURCES / "templates" / "tags_rule").absolute()
        template_files = TestUtils.get_templates(templates_folder)
        parsed_jsons = map(lambda file: TestUtils.parsed_template(file), template_files)
        return list(parsed_jsons)

    @staticmethod
    @pytest.fixture
    def demo_template(demo_templates):
        for template in demo_templates:
            yield template

    @staticmethod
    def should_report_error_when_resource_does_not_have_tag(demo_template):
        template = Template(demo_template.filename, demo_template.jsondoc)

        rules = cfnlint.core.get_rules(append_rules=[str(RULES_FOLDER)], ignore_rules=[DEMO_RULE], include_experimental=False,
                                       include_rules=[],)
        results = cfnlint.core.run_checks(filename=template.filename, rules=rules, regions=["eu-west-1"],
                                          template=template.template)
        expected_failure = list(filter(lambda result: result.rule.id == tags_rule.SAMPLE_TEMPLATE_RULE_ID, results))[0]
        assert_that(expected_failure.message).is_equal_to("Lambda Function should be tagged")

    @staticmethod
    def should_accept_a_rule_config():
        config = Config({"some_key":"some_value"})
        tags_rule = TagsRule(config=config)
        assert_that(tags_rule.config).is_equal_to(config)

    @staticmethod
    def should_read_the_config_file_in_the_root_folder_by_default():
        config = Config({"main_key": "some_value"})
        tags_rule = TagsRule()
        assert_that(tags_rule.config == config).is_true()