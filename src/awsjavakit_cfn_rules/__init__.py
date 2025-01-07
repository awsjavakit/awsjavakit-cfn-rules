import os
from pathlib import Path

PROJECT_FOLDER = Path(os.path.abspath(__file__)).parent

from src.awsjavakit_cfn_rules.rules.tags_rule import (
    TagsRule
)
__all__ = [
    "TagsRule"
]


