"""
Web Navigator AI Agent package

Core components for AI-powered web navigation:
- WebAgent: Main agent class
- BrowserController: Browser automation
"""

from .agent import WebAgent
from .browser_controller import BrowserController

__all__ = ['WebAgent', 'BrowserController']
__version__ = '1.0.0'
