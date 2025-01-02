from __future__ import annotations

from typing import List

import cfnlint
from assertpy import assert_that
from cfnlint import Template, core
import pytest

from src.awsjavakit_cfn_rules.rules import tags_rule
from tests.test_utils import TestUtils
from tests.test_utils import ParsedJson
from src.awsjavakit_cfn_rules.utils.config_reader import    Config
from src.awsjavakit_cfn_rules.rules.tags_rule import TagsRule

DEMO_RULE = "ES9001"


class TagsRuleTest:

    @staticmethod
    @pytest.fixture
    def demo_templates() -> List[ParsedJson]:
        template_files = TestUtils.get_templates("templates/tags_rule")
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
        rules = cfnlint.core.get_rules(append_rules=["../src/awsjavakit_cfn_rules"], ignore_rules=[DEMO_RULE], include_experimental=False,
                                       include_rules=[],)
        results = cfnlint.core.run_checks(filename=template.filename, rules=rules, regions=["eu-west-1"],
                                          template=template.template)
        expected_failure = list(filter(lambda result: result.rule.id == tags_rule.SAMPLE_TEMPLATE_RULE_ID, results))[0]
        assert_that(expected_failure.message).is_equal_to("Lambda Function should be tagged")

    @staticmethod
    def should_accept_a_rule_config_file():
        config = Config({"some_key":"some_value"})
        tags_rule = TagsRule(config=config)
        assert_that(tags_rule.config).is_equal_to(config)
