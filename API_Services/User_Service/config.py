import json
import os
from pathlib import Path

# Locate appsettings.json with multiple fallbacks:
env_path = os.getenv("APP_SETTINGS_PATH") or os.getenv("CONFIG_PATH")
if env_path:
    config_path = Path(env_path)
else:
    BASE_DIR = Path(__file__).resolve().parent
    config_path = None
    # check this dir and parents (limit to a reasonable depth)
    for p in [BASE_DIR] + list(BASE_DIR.parents)[:6]:
        candidate = p / "Db" / "appsettings.json"
        if candidate.exists():
            config_path = candidate
            break
    # fallback to cwd/Db/appsettings.json
    if config_path is None:
        candidate = Path.cwd() / "Db" / "appsettings.json"
        if candidate.exists():
            config_path = candidate

if config_path is None or not config_path.exists():
    raise FileNotFoundError(
        "Could not find 'Db/appsettings.json'.\n"
        "Set environment variable APP_SETTINGS_PATH to the file path, or create 'Db/appsettings.json' in your project root.\n"
        f"Searched for config relative to: {Path(__file__).resolve().parent} and CWD={Path.cwd()}"
    )

with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# --------------------------
# CONFIG VALUES
# --------------------------
DB_CONNECTION_STRING = config.get("Database", {}).get("ConnectionString")

# JWT settings
JWT_SECRET = config.get("JWT", {}).get("SecretKey")
JWT_ALGORITHM = config.get("JWT", {}).get("Algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = config.get("JWT", {}).get("AccessTokenExpireMinutes", 30)
REFRESH_TOKEN_EXPIRE_DAYS = config.get("JWT", {}).get("RefreshTokenExpireDays", 7)

# Captcha
CAPTCHA_SECRET = config.get("Captcha", {}).get("SecretKey")

# Service metadata
SERVICE_NAME = config.get("Service", {}).get("Name")
