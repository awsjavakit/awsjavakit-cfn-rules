import os
from typing import override
from src.awsjavakit_cfn_rules.utils.rule_id import RuleId

class MissingConfigException(RuntimeError):

    @override
    def __init__(self,ruleid:RuleId):
        super().__init__(self.message(ruleid))

    @classmethod
    def message(cls, ruleid)->str:
        message = f'Missing configuration for rule {ruleid}'
        example="""
        Add your configuration in the .cflintrc configuration file. 
        Example file with configuration for rule id E9000:
        ...
            templates:
                - tests/templates/**/*.yaml
            append_rules:
                - awsjavakit_cfn_rules
            configure_rules:
                E9000:
                    some_key: some_value

        ...
        """
        return "".join([message,os.linesep,example])