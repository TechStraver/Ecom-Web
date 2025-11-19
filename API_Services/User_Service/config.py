import json
import os
from pathlib import Path

# Locate appsettings.json with multiple fallbacks:
# 1. Use environment variable `APP_SETTINGS_PATH` or `CONFIG_PATH` if set.
# 2. Walk up from this file's directory looking for `Db/appsettings.json`.
# 3. Check the current working directory for `Db/appsettings.json`.

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

# Access configuration values with safe lookups (KeyError will surface if required values missing)
DB_CONNECTION_STRING = config.get("Database", {}).get("ConnectionString")
JWT_SECRET = config.get("JWT", {}).get("SecretKey")
JWT_ALGORITHM = config.get("JWT", {}).get("Algorithm")
JWT_EXPIRE_MINUTES = config.get("JWT", {}).get("AccessTokenExpireMinutes")
CAPTCHA_SECRET = config.get("Captcha", {}).get("SecretKey")
SERVICE_NAME = config.get("Service", {}).get("Name")
