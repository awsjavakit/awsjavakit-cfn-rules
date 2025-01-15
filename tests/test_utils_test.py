from assertpy import assert_that
from cfnlint.template.template import Template

from tests import TEMPLATES
from tests.test_utils import TestUtils


class TestUtilsTest:

    def should_list_template_files(self):
        template_files = TestUtils.get_templates(TEMPLATES / "tags_rule" / "failing")
        assert_that(len(template_files)).is_greater_than_or_equal_to(1)

    def should_parse_template(self):
        template_files = TestUtils.get_templates(TEMPLATES / "tags_rule" / "failing")
        parsed_jsons = map(lambda file: TestUtils.parsed_template(file), template_files)
        templates = map(lambda parsed_json: Template(parsed_json.filename, parsed_json.jsondoc), parsed_jsons)
        for template in templates:
            assert_that(template).is_instance_of(Template)
