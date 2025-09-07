@echo off
setlocal ENABLEDELAYEDEXPANSION

REM === Keep console attached & use script's folder as working dir ===
pushd "%~dp0"
title Streamlit App Launcher

REM === Visual feedback ===
echo [1/6] Checking Python/venv...

REM === Create venv once if missing (use py launcher if available) ===
if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  where py >nul 2>nul
  if %ERRORLEVEL%==0 (
    py -3 -m venv .venv
  ) else (
    python -m venv .venv
  )
)

REM === Activate venv ===
call ".venv\Scripts\activate"
echo activated py

echo [2/6] Upgrading pip (quiet)...
.venv\Scripts\python.exe -m pip -q install --upgrade pip

REM === Install requirements if present ===
pip install -r requirements.txt

REM === App config ===
set APP=app.py
set PORT=8501
set ADDRESS=127.0.0.1

if not exist "%APP%" (
  echo [ERROR] Could not find "%APP%" in %CD%
  echo Make sure your Streamlit entry file is named app.py or update APP variable.
  echo Press any key to exit...
  pause >nul
  exit /b 1
)
set USE_HTML_LOGIN=false
setx USE_HTML_LOGIN "false" >nul

echo [4/6] Launching Streamlit on http://%ADDRESS%:%PORT% ...
streamlit run .\app.py
pause
