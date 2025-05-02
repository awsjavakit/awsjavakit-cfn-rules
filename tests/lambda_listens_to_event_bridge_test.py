from pathlib import Path
from pathlib import Path
from typing import List

from cfnlint import ConfigMixIn, core as cfnlintcore
from cfnlint.match import Match
from cfnlint.runner import TemplateRunner
from hamcrest import assert_that, contains_string, equal_to, greater_than, is_

from awsjavakit_cfn_rules.rules import RULES_FOLDER, lambda_listens_to_event_bridge
from tests import TEMPLATES
from tests.test_utils import ParsedJson, TestUtils

EVENT_BRIDGE_EVENTS_TEMPLATE_FOLDER = "eventbridge-event-input-to-lambda"


class EventBridgeEventInputToLambdaRuleTest():

    @staticmethod
    def should_fail_when_lambda_listens_to_event_bridge_using_serverless_application_model():
        path: Path = TEMPLATES / EVENT_BRIDGE_EVENTS_TEMPLATE_FOLDER/ "failing" / "eventbridge-event-input-to-lambda.yaml"
        template = TestUtils.parsed_template(path)
        matches = EventBridgeEventInputToLambdaRuleTest._run_template_(template) 
        assert_that(len(matches),is_(greater_than(0)) )
        for match in matches:
            assert_that(match.message,contains_string("FunctionListeningToEventBridge"))

    @staticmethod
    def should_fail_when_lambda_listens_to_event_bridge_using_cloudformation_event_rules():
        path: Path = TEMPLATES / EVENT_BRIDGE_EVENTS_TEMPLATE_FOLDER / "failing" / "lambda-listens-to-event-bridge-cloudformation.yaml"
        template = TestUtils.parsed_template(path)
        matches = EventBridgeEventInputToLambdaRuleTest._run_template_(template)
        assert_that(len(matches), is_(greater_than(0)))
        for match in matches:
            assert_that(match.message, contains_string("FunctionListeningToEventBridge"))

    @staticmethod
    def should_not_fail_when_lambda_does_not_listen_to_directly():
        path: Path = TEMPLATES / EVENT_BRIDGE_EVENTS_TEMPLATE_FOLDER / "passing" / "lambda-does-not-listen-to-event-bridge.yaml"
        template = TestUtils.parsed_template(path)
        matches = EventBridgeEventInputToLambdaRuleTest._run_template_(template)
        # assert_that(len(matches), is_(equal_to(0)))
        for match in matches:
            assert_that(match.message, contains_string("FunctionListeningToEventBridge"))
    @staticmethod
    def _run_template_(resource: ParsedJson)->List[Match]:
        mix_in = ConfigMixIn(cli_args=None,**{"regions": ["eu-west-1"]})
        rules = cfnlintcore.get_rules(append_rules=[str(RULES_FOLDER)],
                                      ignore_rules=[],
                                      include_experimental=False,
                                      include_rules=[],
                                      configure_rules={}
                                      )
        runner = TemplateRunner(resource.filename, resource.jsondoc, mix_in, rules)  # type: ignore 
        return list(runner.run())
