import json
import os
from typing import List, Dict

PROGRESS_FILE = "progress.json"
IMAGE_DIR = "progress_images"


def load_progress() -> List[Dict]:
    """
    Load saved progress entries from disk.
    Each entry is a dict:
      {
        "date": "YYYY-MM-DD",
        "challenge": str,
        "why_it_matters": str,
        "impact_estimate": str,
        "category": str,
        "image_filename": str or None
      }
    """
    if not os.path.exists(PROGRESS_FILE):
        return []

    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        # If file is corrupted or invalid JSON, just start fresh
        return []


def save_progress(log: List[Dict]) -> None:
    """
    Save the full progress log (list of dicts) to disk.
    """
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
