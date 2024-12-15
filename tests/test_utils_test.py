from tests.test_utils import TestUtils

from cfnlint.template.template import Template
from assertpy import assert_that

class TestUtilsTest:

    def should_list_template_files(self):
        template_files = TestUtils.get_templates()
        assert_that(template_files).is_length(1)

    def should_parse_template(self):
        template_files = TestUtils.get_templates()
        parsed_jsons = map(lambda file:TestUtils.parsed_template(file), template_files)
        templates = map(lambda parsed_json: Template(parsed_json.filename,parsed_json.jsondoc),parsed_jsons)
        for template in templates:
            assert_that(template).is_instance_of(Template)