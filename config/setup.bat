@echo off
REM SGNS Classroom Package - Setup and Verification (Windows)
REM Run this to verify everything is installed and working

echo.
echo ============================================================
echo Skip-gram with Negative Sampling - Classroom Package Setup
echo ============================================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Check required packages
echo Checking required packages...
set missing=0

for %%p in (numpy matplotlib sklearn seaborn) do (
    python -c "import %%p" >nul 2>&1
    if errorlevel 1 (
        echo   X %%p is NOT installed
        set missing=1
    ) else (
        echo   OK %%p is installed
    )
)

if %missing% equ 1 (
    echo.
    echo Installing missing packages...
    pip install numpy matplotlib scikit-learn seaborn
    echo.
)

REM Verify files exist
echo Checking package files...
for %%f in (sgns.py sgns_visualization.py classroom_examples.py README.md TEACHING_CHEATSHEET.md VISUALIZATION_GUIDE.md ONE_PAGE_SUMMARY.md INDEX.md) do (
    if exist "%%f" (
        echo   OK %%f
    ) else (
        echo   X %%f (MISSING)
    )
)

REM Test run sgns.py
echo.
echo Running test (this should complete in ^~5 seconds)...
python sgns.py >nul 2>&1
if errorlevel 1 (
    echo   X sgns.py failed to run
) else (
    echo   OK sgns.py runs successfully!
)

echo.
echo ============================================================
echo SETUP COMPLETE - Ready for classroom!
echo ============================================================
echo.
echo NEXT STEPS:
echo   1. Read INDEX.md for quick start
echo   2. Choose teaching approach from README.md
echo   3. Run: python sgns_visualization.py (to regenerate images)
echo   4. Run: python classroom_examples.py (for interactive demo)
echo.
echo Happy teaching! 
echo.
pause
