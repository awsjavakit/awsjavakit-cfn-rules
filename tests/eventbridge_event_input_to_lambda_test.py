from collections.abc import Iterable
from pathlib import Path

from cfnlint.rules import RuleMatch

from awsjavakit_cfn_rules.rules import sqs_long_polling_rule 
 
from cfnlint import ConfigMixIn, core as cfnlintcore
from cfnlint.match import Match
from cfnlint.runner import TemplateRunner
from hamcrest import assert_that, empty, is_not, not_none

from awsjavakit_cfn_rules.rules import RULES_FOLDER
from tests import TEMPLATES
from tests.test_utils import ParsedJson, TestUtils


class EventBridgeEventInputToLambdaRuleTest():

    @staticmethod
    def should_read_input_template():
        path: Path = TEMPLATES / "eventbridge-event-input-to-lambda" / "eventbridge-event-input-to-lambda.yaml"
        template = TestUtils.parsed_template(path)
        matches = EventBridgeEventInputToLambdaRuleTest._run_template_(template) 
        print(matches)
        assert_that(matches,is_not(empty()))

    @staticmethod
    def _run_template_(resource: ParsedJson)->Iterable[Match]:
        mix_in = ConfigMixIn(cli_args=None,**{"regions": ["eu-west-1"]})
        rules = cfnlintcore.get_rules(append_rules=[str(RULES_FOLDER)],
                                      ignore_rules=[],
                                      include_experimental=False,
                                      include_rules=["E9002"],
                                      configure_rules={}
                                      )
        runner = TemplateRunner(resource.filename, resource.jsondoc, mix_in, rules)  # type: ignore 
        return list(runner.run())
