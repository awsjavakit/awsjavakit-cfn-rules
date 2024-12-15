import os
from typing import List

import cfnlint.decode.cfn_yaml
from cfnlint import core
import pytest

from cfnlint.template.template import Template
from assertpy import assert_that


from tests.test_utils import TestUtils

class SampleTemplateRuleTest:


    @pytest.fixture(scope="function")
    def demo_templates(self):
        template_files = TestUtils.get_templates()
        parsed_jsons = map(lambda file: TestUtils.parsed_template(file), template_files)
        return list(map(lambda parsed_json: Template(parsed_json.filename, parsed_json.jsondoc), parsed_jsons))

    def should_match_demorule(self, demo_templates:List[Template]):
        for template in demo_templates:
            rules=cfnlint.core.get_rules(append_rules=["../src"],ignore_rules=[],include_experimental=False,include_rules=[])
            results=cfnlint.core.run_checks(filename=template.filename,rules=rules,regions=["eu-west-1"],template=template.template)
            assert_that(results).is_not_empty()


