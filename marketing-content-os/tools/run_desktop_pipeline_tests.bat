@echo off
setlocal
set SCRIPT_DIR=%~dp0
for %%I in ("%SCRIPT_DIR%..\..") do set REPO_ROOT=%%~fI
if exist "%REPO_ROOT%\.venv\Scripts\python.exe" (
  set PYTHON=%REPO_ROOT%\.venv\Scripts\python.exe
) else (
  set PYTHON=python
)
cd /d "%REPO_ROOT%"
"%PYTHON%" -m unittest discover -s "%REPO_ROOT%\marketing-content-os\tests" -p "test_*.py"
exit /b %ERRORLEVEL%
