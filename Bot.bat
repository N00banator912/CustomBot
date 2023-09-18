@echo off
setlocal

REM Define your bot Python script file
set BOT_SCRIPT=Custombot.py

REM List of dependencies
set DEPENDENCIES=python cv2 websocket-client irc requests

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b 1
)

REM Check for and install missing Python packages
for %%D in (%DEPENDENCIES%) do (
    pip show %%D > nul 2>&1
    if %errorlevel% neq 0 (
        echo Installing missing dependency: %%D
        pip install %%D
    )
)

REM Run your bot script
echo Running the bot...
python %BOT_SCRIPT%

REM End of the script
pause