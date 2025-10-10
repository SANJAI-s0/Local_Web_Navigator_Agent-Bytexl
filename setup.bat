@echo off
echo Setting up Web Navigator AI Agent...
python --version >nul 2>&1 || (echo Install Python 3.12 from python.org & pause & exit /b 1)
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
playwright install
echo Download Ollama from ollama.ai and run: ollama serve
echo Then: ollama run tinyllama (or another model of your choice)
echo Adjust virtual memory: Right-click This PC > Properties > Advanced > Performance Settings > Virtual Memory > Custom (Initial: 8000MB, Max: 16000MB)
echo Run: python webagent/main.py
pause
