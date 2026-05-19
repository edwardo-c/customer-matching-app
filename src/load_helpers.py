from dataclasses import dataclass
from pathlib import Path

@dataclass
class AppPaths:
    db_path: Path
    views_path: Path