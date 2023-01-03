# Description: This file is used to add the parent directory to the path so that the modules can be imported
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd().parent))
