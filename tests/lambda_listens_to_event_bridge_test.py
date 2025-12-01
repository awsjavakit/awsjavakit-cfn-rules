from pathlib import Path

from cfnlint import ConfigMixIn
from cfnlint.match import Match
from hamcrest import assert_that, contains_string, equal_to, greater_than, is_

from tests import TEMPLATES
from tests.test_utils import ParsedTemplate, TestUtils

EVENT_BRIDGE_EVENTS_TEMPLATE_FOLDER = "eventbridge-event-input-to-lambda"


class EventBridgeEventInputToLambdaRuleTest:

    @staticmethod
    def should_fail_when_lambda_listens_to_event_bridge_using_serverless_application_model():
        path: Path = (TEMPLATES / EVENT_BRIDGE_EVENTS_TEMPLATE_FOLDER/ "failing" /
                      "lambda-listens-to-event-bridge-serverless-application-model.yaml")
        template = TestUtils.parse_template(path)
        matches = EventBridgeEventInputToLambdaRuleTest._run_template_(template)
        assert_that(len(matches),is_(greater_than(0)) )
        for match in matches:
            assert_that(match.message,contains_string("FunctionListeningToEventBridge"))

    @staticmethod
    def should_fail_when_lambda_listens_to_event_bridge_using_cloudformation_event_rules():
        path: Path = (TEMPLATES / EVENT_BRIDGE_EVENTS_TEMPLATE_FOLDER / "failing" /
                      "lambda-listens-to-event-bridge-cloudformation.yaml")
        template = TestUtils.parse_template(path)
        matches = EventBridgeEventInputToLambdaRuleTest._run_template_(template)
        assert_that(len(matches), is_(greater_than(0)))
        for match in matches:
            assert_that(match.message, contains_string("FunctionListeningToEventBridge"))

    @staticmethod
    def should_not_fail_when_lambda_does_not_listen_to_directly():
        path: Path = (TEMPLATES / EVENT_BRIDGE_EVENTS_TEMPLATE_FOLDER / "passing" /
                      "lambda-does-not-listen-to-event-bridge.yaml")
        template = TestUtils.parse_template(path)
        matches = EventBridgeEventInputToLambdaRuleTest._run_template_(template)
        assert_that(len(matches), is_(equal_to(0)))
        
    @staticmethod
    def _run_template_(resource: ParsedTemplate)->list[Match]:
        configuration = ConfigMixIn(cli_args=None,**{"regions": ["eu-west-1"]})
        rules = TestUtils.load_all_rules()
        return TestUtils.run_validation(resource, configuration, rules)
    