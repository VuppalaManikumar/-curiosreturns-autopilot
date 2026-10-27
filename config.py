import os
import sys
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.resolve()
ASSETS_DIR = BASE_DIR / "assets"
BACKGROUNDS_DIR = ASSETS_DIR / "backgrounds"
AUDIO_DIR = ASSETS_DIR / "audio"

# DIRECT DESKTOP AUTO FOLDER OUTPUT (Windows) or project outputs (Linux / Cloud)
if sys.platform == "win32" and Path(r"C:\Users\manik\Desktop").exists():
    DESKTOP_AUTO_DIR = Path(r"C:\Users\manik\Desktop\AUTO")
    OUTPUTS_DIR = DESKTOP_AUTO_DIR / "CREATED_VIDEOS"
else:
    DESKTOP_AUTO_DIR = BASE_DIR / "outputs"
    OUTPUTS_DIR = DESKTOP_AUTO_DIR

TEMP_DIR = BASE_DIR / "temp"

# Create directories if not exist
for d in [BACKGROUNDS_DIR, AUDIO_DIR, OUTPUTS_DIR, TEMP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Load config.env manually
CONFIG = {}
env_file = BASE_DIR / "config.env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                CONFIG[k.strip()] = v.strip().strip('"').strip("'")

def get_config(key, default=""):
    return os.environ.get(key, CONFIG.get(key, default))

def get_ffmpeg_binary():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"
