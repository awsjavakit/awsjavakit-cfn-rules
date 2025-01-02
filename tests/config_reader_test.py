import random
import string
from pathlib import Path

import pytest
from assertpy import assert_that, fail

from utils.config_reader import FileConfigReader, RuleId


class FileConfigReaderTest:

    @staticmethod
    def should_return_the_config_of_specified_rule(config_reader: FileConfigReader):
        rule_id_in_file = "E9000"
        config = config_reader.fetch_config(RuleId(rule_id_in_file))
        expected_config_values = {"some_key": "some_value"}
        assert_that(config.values()).is_equal_to(expected_config_values)

    @staticmethod
    def should_return_error_message_containing_rule_id_when_requested_config_is_missing(
            config_reader: FileConfigReader):
        non_existent_rule_id = FileConfigReaderTest.random_string(8)
        try:
            config_reader.fetch_config(RuleId(non_existent_rule_id))
            fail('Attempting to fetch config of non existing rule id should raise error')
        except Exception as e:
            assert_that((str(e))).contains(non_existent_rule_id)


    @staticmethod
    def random_string(length: int) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    @pytest.fixture(scope="function")
    def config_file_path() -> Path:
        file_path = Path("resources", ".sample_cfnlintrc")
        return file_path

    @staticmethod
    @pytest.fixture(scope="function")
    def config_reader(config_file_path: Path):
        return FileConfigReader(config_file_path)
