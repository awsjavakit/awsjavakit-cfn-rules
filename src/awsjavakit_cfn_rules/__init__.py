import os
from pathlib import Path

from src.awsjavakit_cfn_rules.rules.tags_rule import (
    TagsRule
)
__all__ = [
    "TagsRule"
]

PROJECT_FOLDER = Path(os.path.abspath(__file__)).parent
