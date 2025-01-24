from __future__ import annotations

from typing import List

import hamcrest
import pytest
from assertpy import assert_that
from cfnlint import Template
from cfnlint import core as cfnlintcore
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
    def failing_templates() -> List[ParsedJson]:
        templates_folder = (RESOURCES / "templates" / "tags_rule" / "failing").absolute()
        template_files = TestUtils.get_templates(templates_folder)
        parsed_jsons = map(TestUtils.parsed_template, template_files)
        return list(parsed_jsons)

    @staticmethod
    def passing_templates() -> List[ParsedJson]:
        templates_folder = (RESOURCES / "templates" / "tags_rule" / "passing").absolute()
        template_files = TestUtils.get_templates(templates_folder)
        parsed_jsons = map(TestUtils.parsed_template, template_files)
        return list(parsed_jsons)

    @staticmethod
    @pytest.fixture(params=failing_templates())
    def failing_template(request) -> ParsedJson:
        yield request.param

    @staticmethod
    @pytest.fixture(params=passing_templates())
    def passing_template(request) -> ParsedJson:
        yield request.param


    @staticmethod
    def should_not_fail_when_resource_does_not_have_tags():
        resource_without_tags = TestUtils.parsed_template(
            RESOURCES / "templates" / "tags_rule" / "failing" / "resource_without_tags.yaml")
        template = Template(resource_without_tags.filename, resource_without_tags.jsondoc)
        expected_tags = ["expectedTag"]
        config = {tags_rule.EXPECTED_TAGS_FIELD_NAME: expected_tags}
        rules = cfnlintcore.get_rules(append_rules=[str(RULES_FOLDER)],
                                      ignore_rules=[],
                                      include_experimental=False,
                                      include_rules=[],
                                      configure_rules={tags_rule.SAMPLE_TEMPLATE_RULE_ID: config}
                                      )
        results = cfnlintcore.run_checks(filename=template.filename, rules=rules, regions=["eu-west-1"],
                                         template=template.template)
        failure_ids = list(map(lambda result: result.rule.id , results))
        assert_that(failure_ids).contains(tags_rule.SAMPLE_TEMPLATE_RULE_ID)

    @staticmethod
    def should_report_missing_tag_as_specified_in_config(failing_template: ParsedJson):
        template = Template(failing_template.filename, failing_template.jsondoc)
        expected_tags = [fake.word(), fake.word()]
        config = {tags_rule.EXPECTED_TAGS_FIELD_NAME: expected_tags}
        rules = cfnlintcore.get_rules(append_rules=[str(RULES_FOLDER)],
                                      ignore_rules=[],
                                      include_experimental=False,
                                      include_rules=[],
                                      configure_rules={tags_rule.SAMPLE_TEMPLATE_RULE_ID: config}
                                      )
        results = cfnlintcore.run_checks(filename=template.filename, rules=rules, regions=["eu-west-1"],
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
        rules = cfnlintcore.get_rules(append_rules=[str(RULES_FOLDER)],
                                      ignore_rules=[],
                                      include_experimental=False,
                                      include_rules=[],
                                      configure_rules={tags_rule.SAMPLE_TEMPLATE_RULE_ID: config}
                                      )
        results = cfnlintcore.run_checks(filename=template.filename, rules=rules, regions=["eu-west-1"],
                                         template=template.template)
        failures = results
        assert_that(failures).is_empty().described_as(template.filename)

    @staticmethod
    def should_report_resource_name_and_type_when_failing():
        failing_template = TestUtils.parsed_template(
            RESOURCES / "templates" / "tags_rule" / "failing" / "resource_without_tags.yaml")
        template = Template(failing_template.filename, failing_template.jsondoc)
        expected_tags = ["expectedTag"]
        config = {tags_rule.EXPECTED_TAGS_FIELD_NAME: expected_tags}
        rules = cfnlintcore.get_rules(append_rules=[str(RULES_FOLDER)],
                                      ignore_rules=[],
                                      include_experimental=False,
                                      include_rules=[],
                                      configure_rules={tags_rule.SAMPLE_TEMPLATE_RULE_ID: config}
                                      )
        results = cfnlintcore.run_checks(filename=template.filename, rules=rules, regions=["eu-west-1"],
                                         template=template.template)
        for failure in results:
            assert_that(failure.message).contains("UntaggedFunction").contains("AWS::Lambda::Function")
