from pathlib import Path

# local, dev, prod
ENV_MODE = "local"
AUTO_REMOVE_FILES = True

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / "env" / f"{ENV_MODE}.env"

FILE = BASE_DIR / "file"
TMP = BASE_DIR / "tmp"
DOWNLOAD = BASE_DIR / "download"

# Fonts
BASIC_FONT = BASE_DIR / "fonts" / "DejaVuSans.ttf"

# App working
CONVERT_XLS_TO_XLSX = False
START_LITERAL_COLUMN_FILE_XLSX = 10
