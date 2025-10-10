@echo off
mkdir Bytexplore
cd Bytexplore
mkdir webagent
mkdir tests
mkdir deploy
mkdir data
echo. > webagent/__init__.py
echo. > requirements.txt
echo. > README.md
echo. > setup.bat
echo. > .gitignore
cd webagent
echo. > agent.py
echo. > browser_controller.py
echo. > main.py
cd ..
cd tests
echo. > test_agent.py
echo. > test_browser_controller.py
cd ..
cd deploy
echo. > build_exe.py
cd ..
cd ..
echo data/* > Bytexplore/.gitignore
echo Structure created successfully!
pause