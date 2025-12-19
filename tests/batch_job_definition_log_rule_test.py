from __future__ import annotations

from assertpy import assert_that
from cfnlint import ConfigMixIn
from cfnlint.match import Match

from awsjavakit_cfn_rules.rules.batch_job_definition_log_rule import ERROR_MESSAGE
from tests import TEMPLATES
from tests.test_utils import ParsedTemplate, TestUtils


class BatchJobDefinitionLogRuleTest:

    @staticmethod
    def should_report_fargate_jobs_without_logging_config():
        template = TestUtils.parse_template(TEMPLATES / "batch_job_logging" / "failing" / "batch_job_definition.yaml")
        results = BatchJobDefinitionLogRuleTest._run_template_(template)

        assert_that(len(results)).described_as(str(results)).is_equal_to(1)
        assert_that(results[0].message).is_equal_to(ERROR_MESSAGE)
        resource_line_in_sample_file = 11
        assert_that(results[0].linenumber).is_equal_to(resource_line_in_sample_file)

    @staticmethod
    def should_accept_fargate_jobs_with_logging_config_that_contains_log_group():
        template = TestUtils.parse_template(TEMPLATES / "batch_job_logging" / "passing" / "batch_job_definition.yaml")
        results = BatchJobDefinitionLogRuleTest._run_template_(template)

        assert_that(len(results)).described_as(str(results)).is_equal_to(0)

    @staticmethod
    def should_accept_fargate_jobs_with_logging_config_that_is_other_than_cloudwatch():
        template = TestUtils.parse_template(TEMPLATES / "batch_job_logging" / "passing" \
                                            / "batch_job_definition_with_other_than_cloudwatch.yaml")
        results = BatchJobDefinitionLogRuleTest._run_template_(template)
        assert_that(len(results)).described_as(str(results)).is_equal_to(0)

    @staticmethod
    def _run_template_(resource: ParsedTemplate) -> list[Match]:
        configuration = ConfigMixIn(cli_args=None, **{"regions": ["eu-west-1"]})
        rules = TestUtils.load_all_rules()
        return TestUtils.run_validation(resource, configuration, rules)  # pyright: ignore [reportArgumentType]
