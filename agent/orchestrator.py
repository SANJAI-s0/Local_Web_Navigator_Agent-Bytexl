# agent/orchestrator.py
"""
Orchestrator: glue code connecting the Planner, BrowserController and Memory.
"""


from .planner import Planner
from .browser_controller import BrowserController
from .memory import Memory
from typing import Dict, Any
import time
import traceback


class Orchestrator:
    def __init__(self, headless: bool = True, model_path: str = None, db_path: str = None):
        self.planner = Planner(model_path=model_path) if model_path else Planner()
        self.browser = BrowserController(headless=headless)
        self.memory = Memory(db_path) if db_path else Memory()
        self._last_plan = None

    def run(self, instruction: str) -> Dict[str, Any]:
        plan = self.planner.plan(instruction)
        self._last_plan = plan
        results: Dict[str, Any] = {"task_id": plan.get("task_id"), "actions": [], "status": "ok", "meta": plan.get("meta", {})}
        try:
            self.browser.start()
            for action in plan.get("actions", []):
                typ = action.get("type")
                try:
                    if typ == "search":
                        engine = action.get("engine", "duckduckgo")
                        q = action.get("query", instruction)
                        maxr = int(action.get("max_results", 5))
                        r = self.browser.search(engine, q, max_results=maxr)
                        results["actions"].append({"action": "search", "engine": engine, "results": r})
                    elif typ == "open_url":
                        url = action.get("url")
                        self.browser.goto(url)
                        results["actions"].append({"action": "open_url", "url": url})
                    elif typ == "extract":
                        sel = action.get("selector")
                        items = self.browser.extract_text(sel)
                        results["actions"].append({"action": "extract", "selector": sel, "items": items})
                    elif typ == "screenshot":
                        path = action.get("path", "screenshot.png")
                        p = self.browser.screenshot(path=path)
                        results["actions"].append({"action": "screenshot", "path": p})
                    else:
                        results["actions"].append({"action": "unknown", "raw": action})
                except Exception as e:
                    results["actions"].append({"action": typ, "error": str(e), "trace": traceback.format_exc()})
                time.sleep(0.3)
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            results["trace"] = traceback.format_exc()
        finally:
            try:
                self.browser.stop()
            except Exception:
                pass
            try:
                self.memory.save_task(results.get("task_id") or "no-id", instruction, results)
            except Exception:
                pass
        return results
