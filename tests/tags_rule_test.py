from __future__ import annotations

from typing import List

import cfnlint
import hamcrest
import pytest
from assertpy import assert_that
from cfnlint import Template, core
from faker import Faker
from faker.providers import lorem
from hamcrest import any_of, contains_string

from awsjavakit_cfn_rules.rules import RULES_FOLDER, tags_rule
from tests import RESOURCES
from tests.test_utils import ParsedJson, TestUtils

CONFIG_MAP_IN_ROOT_FOLDER = {"main_key": "some_value"}

fake = Faker()
fake.add_provider(lorem)


class TagsRuleTest:

    @staticmethod
    @pytest.fixture
    def failing_templates() -> List[ParsedJson]:

        templates_folder = (RESOURCES / "templates" / "tags_rule" / "failing").absolute()
        template_files = TestUtils.get_templates(templates_folder)
        parsed_jsons = map(lambda file: TestUtils.parsed_template(file), template_files)
        return list(parsed_jsons)

    @staticmethod
    @pytest.fixture
    def passing_templates() -> List[ParsedJson]:

        templates_folder = (RESOURCES / "templates" / "tags_rule" / "passing").absolute()
        template_files = TestUtils.get_templates(templates_folder)
        parsed_jsons = map(lambda file: TestUtils.parsed_template(file), template_files)
        return list(parsed_jsons)

    @staticmethod
    @pytest.fixture
    def failing_template(failing_templates) -> ParsedJson:
        for template in failing_templates:
            yield template

    @staticmethod
    @pytest.fixture
    def passing_template(passing_templates) -> ParsedJson:
        for template in passing_templates:
            yield template

    @staticmethod
    def should_report_missing_tag_as_specified_in_config(failing_template: ParsedJson):
        template = Template(failing_template.filename, failing_template.jsondoc)
        expected_tags = [fake.word(), fake.word()]
        config = {tags_rule.EXPECTED_TAGS_FIELD_NAME: expected_tags}
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

    @staticmethod
    def should_pass_when_required_tags_are_in_place(passing_template: ParsedJson):
        template = Template(passing_template.filename, passing_template.jsondoc)
        expected_tags = ["expectedTag"]
        config = {tags_rule.EXPECTED_TAGS_FIELD_NAME: expected_tags}
        rules = cfnlint.core.get_rules(append_rules=[str(RULES_FOLDER)],
                                       ignore_rules=[],
                                       include_experimental=False,
                                       include_rules=[],
                                       configure_rules={tags_rule.SAMPLE_TEMPLATE_RULE_ID: config}
                                       )
        results = cfnlint.core.run_checks(filename=template.filename, rules=rules, regions=["eu-west-1"],
                                          template=template.template)
        failures = list(filter(lambda result: result.rule.id == tags_rule.SAMPLE_TEMPLATE_RULE_ID, results))
        assert_that(failures).is_empty()
