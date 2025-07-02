from __future__ import annotations

from collections.abc import Iterable

import pytest
from assertpy import assert_that
from cfnlint import ConfigMixIn

from awsjavakit_cfn_rules.rules.sqs_long_polling_rule import ERROR_MESSAGE
from tests import TEMPLATES
from tests.test_utils import ParsedJson, TestUtils


class SqsLongPollingRuleTest:


    @staticmethod
    def should_report_sqs_queues_with_short_polling(failing_template:ParsedJson):


        results = SqsLongPollingRuleTest._run_template_(failing_template)

        assert_that(len(results)).is_equal_to(1)
        assert_that(results[0].message).is_equal_to(ERROR_MESSAGE)
        resource_line_in_sample_file = 11
        assert_that(results[0].linenumber).is_equal_to(resource_line_in_sample_file)

    def should_accept_sqs_queues_with_long_polling(self):
        path = TEMPLATES / "sqs_long_polling_rule" / "passing" / "queue_with_long_polling.yaml"
        template = TestUtils.parsed_template(path)
        results = SqsLongPollingRuleTest._run_template_(template)

        assert_that(len(results)).is_equal_to(0)


    @staticmethod
    def _run_template_(resource: ParsedJson):
        configuration = ConfigMixIn(cli_args=None)
        rules = TestUtils.load_all_rules()
        return TestUtils.run_validation(resource, configuration, rules)

    @staticmethod
    def failing_templates() -> list[ParsedJson]:
        templates_folder = (TEMPLATES / "sqs_long_polling_rule" / "failing").absolute()
        template_files = TestUtils.get_templates(templates_folder)
        parsed_jsons = map(TestUtils.parsed_template, template_files)
        return list(parsed_jsons)

    @staticmethod
    @pytest.fixture(params=failing_templates())
    def failing_template(request) -> Iterable[ParsedJson]:
        yield request.param
