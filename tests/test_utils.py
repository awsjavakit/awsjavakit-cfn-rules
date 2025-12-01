from pathlib import Path
from typing import Any

import cfnlint
import cfnlint.decode.cfn_yaml
from attrs import define
from cfnlint import ConfigMixIn
from cfnlint import core as cfnlintcore
from cfnlint.rules import Match
from cfnlint.runner.template.runner import run_template_by_data

from awsjavakit_cfn_rules.rules import RULES_FOLDER


@define
class ParsedTemplate:
    filename: str
    jsondoc: dict[str, Any]


class TestUtils:

    @staticmethod
    def get_templates(folder: Path) -> list[Path]:
        template_filenames = list(filter(lambda file: file.is_file(), folder.iterdir()))
        full_paths = map(lambda filename: folder.with_segments(filename).absolute(), template_filenames)
        return list(full_paths)

    @staticmethod
    def parse_template(file: Path) -> ParsedTemplate:
        return ParsedTemplate(filename=str(file.absolute()), jsondoc=cfnlint.decode.cfn_yaml.load(file))

    @staticmethod
    def load_all_rules(cfnlint_rule_config: dict[str, Any] | None = None):
        return cfnlintcore.get_rules(append_rules=[str(RULES_FOLDER)],
                                     ignore_rules=[],
                                     include_experimental=False,
                                     include_rules=[],
                                     configure_rules=cfnlint_rule_config if cfnlint_rule_config is not None else {}
                                     )

    @staticmethod
    def run_validation(resource: ParsedTemplate, configuration: ConfigMixIn, rules: dict[str, Any]) -> list[Match]:
        return list(run_template_by_data(resource.jsondoc,configuration,rules)) # type: ignore
        
