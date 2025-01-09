from __future__ import annotations
from pathlib import Path
from typing import override

import yaml
from attrs import define, field
from awsjavakit_cfn_rules.rules.utils.missing_config_exception import MissingConfigException
from awsjavakit_cfn_rules.rules.utils.rule_id import RuleId


def _default_config_file_() -> Path:
    return Path.cwd() / ".cfnlintrc"


@define(init=True, eq=False, frozen=True,order=False)
class Config:
    _values: field(type=dict)

    def values(self) -> dict:
        return self._values

    def __eq__(self, other: Config):
        return self.values() == other.values()

    def __ne__(self, other):
        return not self.__eq__(other)


class ConfigReader:

    def fetch_config(self, rule_id: RuleId) -> Config:
        pass


@define
class FileConfigReader(ConfigReader):
    file_path: field(type=Path)

    @override
    def fetch_config(self, rule_id: RuleId) -> Config:
        config_text: str = self.file_path.read_text(encoding='utf-8')
        config_value: dict = yaml.safe_load(config_text)
        ruleConfig = config_value.get("configure_rules").get(str(rule_id))
        if ruleConfig is not None:
            return Config(ruleConfig)
        else:
            raise MissingConfigException(rule_id)

    @classmethod
    def default(cls) -> FileConfigReader:
        return cls(_default_config_file_())
