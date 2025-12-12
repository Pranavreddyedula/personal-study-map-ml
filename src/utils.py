import os
import re
import datetime
import logging

# Simple logger configured for stdout (Render shows stdout)
logger = logging.getLogger("personal_study_map")
if not logger.handlers:
    handler = logging.StreamHandler()
    fmt = "%(asctime)s %(levelname)s %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def ensure_dir(path):
    """Create directory if missing."""
    os.makedirs(path, exist_ok=True)
    return path

def safe_filename(name):
    """Make a filesystem-safe filename (keeps extension if present)."""
    name = name.strip().replace(" ", "_")
    name = re.sub(r"[^A-Za-z0-9._-]", "", name)
    return name

def timestamp_str():
    return datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
