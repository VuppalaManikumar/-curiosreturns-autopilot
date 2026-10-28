import json
from pathlib import Path
from typing import Dict, Any, List

HISTORY_FILE = Path(__file__).parent / "history_registry.json"

def load_history() -> Dict[str, Any]:
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "used_titles": [],
        "used_headlines": [],
        "recent_niches": [],
        "last_background_combo": []
    }

def save_history(history: Dict[str, Any]):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"[!] History save error: {e}")

def is_title_used(title: str) -> bool:
    h = load_history()
    title_lower = title.strip().lower()
    return any(title_lower in t.lower() or t.lower() in title_lower for t in h.get("used_titles", []))

def is_headline_used(headline: str) -> bool:
    h = load_history()
    hl_lower = headline.strip().lower()
    return any(hl_lower in h_item.lower() or h_item.lower() in hl_lower for h_item in h.get("used_headlines", []))

def record_used_content(title: str, niche: str, headline: str = None, bg_combo: List[str] = None):
    h = load_history()
    if "used_titles" not in h:
        h["used_titles"] = []
    if "used_headlines" not in h:
        h["used_headlines"] = []
    if "recent_niches" not in h:
        h["recent_niches"] = []

    if title and title not in h["used_titles"]:
        h["used_titles"].append(title)
        # Keep last 500 titles
        if len(h["used_titles"]) > 500:
            h["used_titles"].pop(0)

    if headline and headline not in h["used_headlines"]:
        h["used_headlines"].append(headline)
        if len(h["used_headlines"]) > 500:
            h["used_headlines"].pop(0)

    if niche:
        h["recent_niches"].append(niche)
        if len(h["recent_niches"]) > 10:
            h["recent_niches"].pop(0)

    if bg_combo:
        h["last_background_combo"] = bg_combo

    save_history(h)

def get_last_niche() -> str:
    h = load_history()
    recent = h.get("recent_niches", [])
    return recent[-1] if recent else ""

def get_last_bg_combo() -> List[str]:
    h = load_history()
    return h.get("last_background_combo", [])
