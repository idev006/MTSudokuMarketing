@echo off
setlocal
set SCRIPT_DIR=%~dp0
for %%I in ("%SCRIPT_DIR%..\..") do set REPO_ROOT=%%~fI
if "%~1"=="" (
  set WORKSPACE=%REPO_ROOT%\_operator_workspace
) else (
  set WORKSPACE=%~1
)
if exist "%REPO_ROOT%\.venv\Scripts\python.exe" (
  set PYTHON=%REPO_ROOT%\.venv\Scripts\python.exe
) else (
  set PYTHON=python
)
cd /d "%REPO_ROOT%"
"%PYTHON%" "%REPO_ROOT%\marketing-content-os\tools\workspace_health_check.py" "%WORKSPACE%" --write-report
exit /b %ERRORLEVEL%
