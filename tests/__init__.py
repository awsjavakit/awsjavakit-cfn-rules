import os
from pathlib import Path

TEST_FOLDER: Path = Path(os.path.abspath(__file__)).parent.absolute()
RESOURCES = (TEST_FOLDER / "resources").absolute()
TEMPLATES = RESOURCES / "templates"
