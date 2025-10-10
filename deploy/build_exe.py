import PyInstaller.__main__
import os

# Ensure data dir exists
os.makedirs('data', exist_ok=True)

PyInstaller.__main__.run([
    'webagent/main.py',
    '--onefile',
    '--windowed',  # No console for GUI app
    '--name=WebNavigatorAgent',
    '--add-data=data;data',  # Include empty data dir
    '--exclude-module=tkinter',  # It's built-in, but ensure
])
