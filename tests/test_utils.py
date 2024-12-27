import os
from typing import List

import cfnlint
import cfnlint.decode.cfn_yaml
from attrs import define


@define
class ParsedJson:
    filename: str
    jsondoc: dict


class TestUtils:

    @staticmethod
    def get_templates(path:str="templates") -> List[str]:
        template_folder = os.path.join(os.path.dirname(__file__), path)
        template_filenames = os.listdir(template_folder)
        full_paths = map(lambda filename: os.path.join(template_folder, filename), template_filenames)
        return list(full_paths)



    @staticmethod
    def parsed_template(file: str) -> ParsedJson:
        return ParsedJson(filename=file, jsondoc=cfnlint.decode.cfn_yaml.load(file))


