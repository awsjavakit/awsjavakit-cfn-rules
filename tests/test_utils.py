from pathlib import Path

import cfnlint
import cfnlint.decode.cfn_yaml
from attrs import define


@define
class ParsedJson:
    filename: str
    jsondoc: dict


class TestUtils:

    @staticmethod
    def get_templates(folder: Path) -> list[Path]:
        template_filenames = list(filter(lambda file: file.is_file(), folder.iterdir()))
        full_paths = map(lambda filename: folder.with_segments(filename).absolute(), template_filenames)
        return list(full_paths)

    @staticmethod
    def parsed_template(file: Path) -> ParsedJson:
        return ParsedJson(filename=str(file.absolute()), jsondoc=cfnlint.decode.cfn_yaml.load(file))
