# webagent/__init__.py
"""
webagent package initializer.
This file marks the directory as a python package so tests and imports
like `from webagent.agent import WebNavigatorAgent` work reliably.
"""

# optional: export commonly used names (keeps imports nicer)
from .agent import WebNavigatorAgent  # type: ignore
from .browser_controller import BrowserController  # type: ignore

__all__ = ["WebNavigatorAgent", "BrowserController"]
