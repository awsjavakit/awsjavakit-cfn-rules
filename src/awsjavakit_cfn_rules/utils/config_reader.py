from pathlib import Path
from typing import override

import yaml
from attrs import define


@define(repr=False, str=False)
class RuleId:
    rule_id: str

    def __str__(self) -> str:
        return self.rule_id

    def __repr__(self) -> str:
        return self.__str__()


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

        return Config(config_value.get("configure_rules").get(str(rule_id)))


