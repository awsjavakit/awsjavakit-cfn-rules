from pathlib import Path, PosixPath, PurePath

from assertpy import assert_that

from awsjavakit_cfn_rules.utils.config_reader import FileConfigReader, RuleId


class FileConfigReaderTest:

    def should_return_the_config_of_specified_rule(self):
        file_path = Path("resources",".sample_cfnlintrc")
        print(str(file_path.absolute()))
        config_reader = FileConfigReader(file_path=file_path)
        rule_id_in_file = "E9000"
        config = config_reader.fetch_config(RuleId(rule_id_in_file))
        expected_config_values= {"some_key":"some_value"}
        assert_that(config.values()).is_equal_to(expected_config_values)