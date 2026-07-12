from pathlib import Path

# local, dev, prod
ENV_MODE = "local"

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / "env" / f"{ENV_MODE}.env"
