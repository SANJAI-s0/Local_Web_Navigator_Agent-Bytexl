# agent/planner.py
"""
Planner: Uses a local GPT4All model if available to convert a natural-language
instruction into a JSON plan. Falls back to a heuristic planner when model is
not available or fails.
"""

from typing import Dict, Any
import json
import uuid
from datetime import datetime
import os
import re

MODEL_PATH_DEFAULT = os.path.join("models", "gpt4all-model.bin")

try:
    # Optional import - if not installed we'll fallback
    from gpt4all import GPT4All  # type: ignore
    GPT4ALL_AVAILABLE = True
except Exception:
    GPT4ALL_AVAILABLE = False

PROMPT_TEMPLATE = """
You are a web automation planner. Convert the user instruction into JSON with keys:
- task_id (uuid string)
- actions (list of actions). Possible action types: search, open_url, click, extract, fill_form, screenshot, wait.
Each action is an object with a "type" and parameters (e.g., query, url, selector, max_results).
Return ONLY valid JSON (no explanatory text). Example:
{{"task_id":"...","actions":[{{"type":"search","engine":"google","query":"...","max_results":5}}],"meta":{{"created":"...Z"}}}}
User instruction:
\"\"\"{instruction}\"\"\"
"""

class Planner:
    def __init__(self, model_path: str = MODEL_PATH_DEFAULT):
        self.model_path = model_path
        self._model = None
        self._use_model = False
        if GPT4ALL_AVAILABLE and os.path.exists(self.model_path):
            try:
                self._model = GPT4All(model=self.model_path)
                self._use_model = True
            except Exception:
                self._model = None
                self._use_model = False

    def plan(self, instruction: str) -> Dict[str, Any]:
        if not instruction or not instruction.strip():
            raise ValueError("Instruction must be a non-empty string.")

        if self._use_model and self._model:
            prompt = PROMPT_TEMPLATE.format(instruction=instruction)
            try:
                resp = self._model.generate(prompt, max_tokens=512)
                if isinstance(resp, (list, tuple)):
                    text = " ".join(map(str, resp))
                else:
                    text = str(resp)
                return self._safe_load_json_from_text(text)
            except Exception:
                pass

        return self._heuristic_plan(instruction)

    def _heuristic_plan(self, instruction: str) -> Dict[str, Any]:
        tid = str(uuid.uuid4())
        il = instruction.lower()

        if "flipkart" in il:
            query_clean = re.sub(r"flipkart", "", il).strip()
            query_encoded = query_clean.replace(" ", "+")
            url = f"https://www.flipkart.com/search?q={query_encoded}"
            action1 = {"type": "open_url", "url": url}
            # Updated Flipkart product title selector with wait
            action2 = {"type": "extract", "selector": "div._2kHMtA div._4rR01T"}  # Flipkart laptop titles selector
            actions = [action1, action2]
        elif any(w in il for w in ("search", "find", "look for", "list", "show")):
            actions = [{"type": "search", "engine": "duckduckgo", "query": instruction, "max_results": 5}]
        elif "open" in il and "http" in il:
            m = re.search(r"https?://\S+", instruction)
            url = m.group(0) if m else "https://www.example.com"
            actions = [{"type": "open_url", "url": url}]
        else:
            actions = [{"type": "search", "engine": "duckduckgo", "query": instruction, "max_results": 5}]

        return {
            "task_id": tid,
            "actions": actions,
            "meta": {"created": datetime.utcnow().isoformat() + "Z", "planner": "heuristic"}
        }

    def _safe_load_json_from_text(self, text: str) -> Dict[str, Any]:
        try:
            return json.loads(text)
        except Exception:
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and end > start:
                sub = text[start:end+1]
                try:
                    return json.loads(sub)
                except Exception:
                    pass
        return {
            "task_id": str(uuid.uuid4()),
            "actions": [{"type": "search", "engine": "duckduckgo", "query": text[:120], "max_results": 5}],
            "meta": {"created": datetime.utcnow().isoformat() + "Z", "planner": "fallback_parse"}
        }
