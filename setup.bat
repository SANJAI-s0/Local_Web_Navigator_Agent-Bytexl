@echo off
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
playwright install
echo Setup complete. Activate with .venv\Scripts\activate
pause
