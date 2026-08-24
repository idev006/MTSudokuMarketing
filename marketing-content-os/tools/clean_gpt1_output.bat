@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM BiiigBee GPT1 Cleaner Wrapper
REM Usage:
REM   clean_gpt1_output.bat <raw_input_text_file> [expected_rows]
REM Example:
REM   marketing-content-os\tools\clean_gpt1_output.bat marketing-content-os\tmp\pilot001_raw.md 10

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%..\.."
pushd "%REPO_ROOT%" >nul

if "%~1"=="" (
  echo ERROR: Missing raw input text file.
  echo.
  echo Usage:
  echo   marketing-content-os\tools\clean_gpt1_output.bat ^<raw_input_text_file^> [expected_rows]
  echo.
  echo Example:
  echo   marketing-content-os\tools\clean_gpt1_output.bat marketing-content-os\tmp\pilot001_raw.md 10
  popd >nul
  exit /b 2
)

set "RAW_INPUT=%~1"
set "EXPECTED_ROWS=%~2"
if "%EXPECTED_ROWS%"=="" set "EXPECTED_ROWS=10"

if not exist "%RAW_INPUT%" (
  echo ERROR: Raw input file not found: %RAW_INPUT%
  popd >nul
  exit /b 2
)

if not exist "marketing-content-os\tmp" mkdir "marketing-content-os\tmp"
if not exist "marketing-content-os\production\social-posts\clean" mkdir "marketing-content-os\production\social-posts\clean"
if not exist "marketing-content-os\production\social-posts\reports" mkdir "marketing-content-os\production\social-posts\reports"

for %%F in ("%RAW_INPUT%") do set "BASE_NAME=%%~nF"

set "CLEAN_OUTPUT=marketing-content-os\production\social-posts\clean\%BASE_NAME%_clean.tsv"
set "REPORT_OUTPUT=marketing-content-os\production\social-posts\reports\%BASE_NAME%_clean_report.json"

echo.
echo ============================================================
echo BiiigBee GPT1 Cleaner
echo ============================================================
echo Raw input     : %RAW_INPUT%
echo Expected rows : %EXPECTED_ROWS%
echo Clean output  : %CLEAN_OUTPUT%
echo Report output : %REPORT_OUTPUT%
echo.

python marketing-content-os\tools\clean_validate_campaign_markdown.py ^
  --raw-input "%RAW_INPUT%" ^
  --clean-output "%CLEAN_OUTPUT%" ^
  --expected-rows "%EXPECTED_ROWS%" ^
  --sku-lookup marketing-content-os\schemas\sku_lookup_v1.tsv ^
  --taxonomy marketing-content-os\schemas\controlled_vocabulary_v1.tsv ^
  --template-registry marketing-content-os\templates\prompt_template_registry_v1.tsv ^
  --report "%REPORT_OUTPUT%"

set "EXIT_CODE=%ERRORLEVEL%"

echo.
if "%EXIT_CODE%"=="0" (
  echo RESULT: PASS
  echo.
  echo NEXT STEPS:
  echo   1. Open the clean TSV file:
  echo      %CLEAN_OUTPUT%
  echo   2. Choose the best 5 rows for the SKU.
  echo   3. Copy ONE complete 27-field row at a time into GPT2.
  echo   4. Use this GPT2 mode:
  echo      MODE: TEMPLATE_HANDOFF
  echo   5. After GPT2 returns PASS/PASS_WITH_WARNING, use its final image prompt to generate the image.
  echo   6. Record status in:
  echo      marketing-content-os\production\social-posts\social_content_inventory_v1.tsv
) else (
  echo RESULT: FAIL
  echo.
  echo Open the report and fix the input before sending anything to GPT2:
  echo   %REPORT_OUTPUT%
)

popd >nul
exit /b %EXIT_CODE%
