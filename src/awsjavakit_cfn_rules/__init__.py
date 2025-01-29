"""
awsjavakit_cfn_rules package
"""
from pathlib import Path
import os
from awsjavakit_cfn_rules.rules.tags_checker import (
    TagsChecker
)

PROJECT_FOLDER = Path(os.path.abspath(__file__)).parent


__all__ = [
    "TagsChecker"
]
