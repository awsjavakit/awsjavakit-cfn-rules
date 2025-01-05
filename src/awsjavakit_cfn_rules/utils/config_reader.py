from __future__ import annotations
from pathlib import Path
from typing import override

import yaml
from attrs import define
from src.awsjavakit_cfn_rules.utils.missing_config_exception import MissingConfigException
from src.awsjavakit_cfn_rules.utils.rule_id import RuleId

@define(init=True, eq=True, frozen=True)
class Config:
    _values: dict

    def values(self) -> dict:
        return self._values


class ConfigReader:

    def fetch_config(self, rule_id: RuleId) -> Config:
        pass


@define
class FileConfigReader(ConfigReader):
    file_path: Path

    @override
    def fetch_config(self, rule_id: RuleId) -> Config:
        config_text: str = self.file_path.read_text(encoding='utf-8')
        config_value: dict = yaml.safe_load(config_text)
        ruleConfig = config_value.get("configure_rules").get(str(rule_id))
        if ruleConfig is not  None:
            return Config(ruleConfig)
        else:
            raise MissingConfigException(rule_id)


