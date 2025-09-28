# agent/utils.py
"""
Utility helpers.
"""

import json
import time
import os
import re
import functools
from datetime import datetime
from typing import Callable, Any, Optional

def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)
    return path

def safe_json_loads(s: str, default=None):
    try:
        return json.loads(s)
    except Exception:
        return default

def save_json_file(path: str, obj, indent: int = 2):
    ensure_dir(os.path.dirname(path) or ".")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)

def load_json_file(path: str, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return default

def sanitize_filename(name: str, max_len: int = 200) -> str:
    name = re.sub(r"[<>:\"/\\|?*\x00-\x1F]", "_", name)
    name = re.sub(r"\s+", "_", name).strip("_")
    return name[:max_len] or "file"

def retry(
    tries: int = 3,
    delay: float = 0.5,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
    logger: Optional[Callable[[str], None]] = None,
):
    def deco(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            last_exc = None
            for attempt in range(1, _tries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if logger:
                        logger(f"Attempt {attempt} failed: {e}. Retrying in {_delay}s...")
                    time.sleep(_delay)
                    _delay *= backoff
            if last_exc:
                raise last_exc
        return wrapper
    return deco

def parse_price_text(text: str) -> Optional[float]:
    if not text:
        return None
    cleaned = text.replace(",", "")
    m = re.search(r"([₹RsRs\.]*\s*[-+]?[0-9]*\.?[0-9]+)", cleaned)
    if not m:
        return None
    num = m.group(0)
    num = re.sub(r"[^\d\.\-+]", "", num)
    try:
        return float(num)
    except Exception:
        return None

def slugify(text: str, max_len: int = 60) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:max_len]
