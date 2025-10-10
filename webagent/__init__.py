# Empty init file to make webagent a package
"""
Web Navigator AI Agent package

This package contains the core components for the AI-powered web navigation agent:
- agent: Core agent logic and instruction processing
- browser_controller: Browser automation functionality
"""

from .agent import WebAgent
from .browser_controller import BrowserController

__all__ = ['WebAgent', 'BrowserController']
__version__ = '1.0.0'
