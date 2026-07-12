import os
from pathlib import Path

# Tryb środowiska: local (domyślny), stg, prod.
# Ustawiany zmienną środowiskową ENV_MODE - obraz produkcyjny ma ENV_MODE=prod
# wbudowane w production.dockerfile, lokalnie wystarczy `ENV_MODE=stg make ...`.
ENV_MODE = os.getenv("ENV_MODE", "local")

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / "env" / f"{ENV_MODE}.env"
