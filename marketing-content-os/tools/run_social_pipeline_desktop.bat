@echo off
setlocal EnableExtensions

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%..\.."
pushd "%REPO_ROOT%" >nul

if not exist ".venv\Scripts\python.exe" (
  echo Local virtual environment not found.
  echo.
  echo Run first:
  echo   python -m venv .venv
  echo   .venv\Scripts\activate
  echo   pip install -r requirements.txt
  echo.
  popd >nul
  exit /b 2
)

".venv\Scripts\python.exe" marketing-content-os\apps\social_pipeline_desktop\main_queue.py
set "EXIT_CODE=%ERRORLEVEL%"

popd >nul
exit /b %EXIT_CODE%
