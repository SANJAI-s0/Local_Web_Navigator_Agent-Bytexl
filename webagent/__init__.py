# Empty init file to make webagent a package
from .agent import WebAgent
from .browser_controller import BrowserController

__all__ = ['WebAgent', 'BrowserController']
__version__ = '1.0.0'
