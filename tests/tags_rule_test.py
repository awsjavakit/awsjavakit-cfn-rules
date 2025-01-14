from __future__ import annotations

import json
from typing import List

import cfnlint
import pytest
from assertpy import assert_that
from cfnlint import ConfigMixIn, Rules, Template, core
from cfnlint import decode
from faker import Faker
from faker.providers import lorem
from hamcrest import any_of, contains_string, equal_to

from awsjavakit_cfn_rules.rules import tags_rule
from awsjavakit_cfn_rules.rules import RULES_FOLDER
from awsjavakit_cfn_rules.rules.tags_rule import TagsRule
from awsjavakit_cfn_rules.rules.utils.config_reader import Config
from tests import RESOURCES
from tests.test_utils import ParsedJson, TestUtils
from cfnlint.runner import TemplateRunner
import hamcrest

CONFIG_MAP_IN_ROOT_FOLDER = {"main_key": "some_value"}

fake = Faker()
fake.add_provider(lorem)


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
    def should_report_missing_tag_as_specified_in_config(demo_template):
        template = Template(demo_template.filename, demo_template.jsondoc)
        expected_tags = [fake.word(), fake.word()]
        config = {"expectedTags": expected_tags}
        rules = cfnlint.core.get_rules(append_rules=[str(RULES_FOLDER)],
                                       ignore_rules=[],
                                       include_experimental=False,
                                       include_rules=[],
                                       configure_rules={tags_rule.SAMPLE_TEMPLATE_RULE_ID: config}
                                       )
        results = cfnlint.core.run_checks(filename=template.filename, rules=rules, regions=["eu-west-1"],
                                          template=template.template)
        failure = list(filter(lambda result: result.rule.id == tags_rule.SAMPLE_TEMPLATE_RULE_ID, results))[0]
        hamcrest.assert_that(failure.message, any_of(
            contains_string(expected_tags[0]),
            contains_string(expected_tags[1])
        ))


