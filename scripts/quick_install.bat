@echo off
REM Elysia Engine Quick Install Script (Windows)
REM Usage: quick_install.bat

echo ============================================
echo    Elysia Fractal Engine - Quick Install
echo ============================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python %PYTHON_VERSION% found
echo.

REM Clone repository
echo Cloning Elysia Engine repository...
if exist "elysia-fractal-engine_V1" (
    echo Directory 'elysia-fractal-engine_V1' already exists
    set /p REMOVE="Remove and re-clone? (y/n): "
    if /i "%REMOVE%"=="y" (
        rmdir /s /q elysia-fractal-engine_V1
    ) else (
        echo Installation cancelled
        pause
        exit /b 1
    )
)

git clone https://github.com/ioas0316-cloud/elysia-fractal-engine_V1.git
cd elysia-fractal-engine_V1
echo Repository cloned successfully
echo.

REM Optional: Install development dependencies
echo Optional: Install development dependencies?
echo (pytest for testing, not required for usage)
set /p INSTALL_DEV="Install? (y/n): "
if /i "%INSTALL_DEV%"=="y" (
    pip install pytest
    echo Development dependencies installed
) else (
    echo Skipped development dependencies
)
echo.

REM Run verification
echo Running verification test...
python -c "from elysia_core import quick_consciousness_setup; c = quick_consciousness_setup('TestBot'); r = c.think('Hello Elysia!'); print('Verification successful!\nMood: ' + r.mood + '\nEmotion: ' + r.emotion['dominant'])"
if errorlevel 1 (
    echo Verification failed
    pause
    exit /b 1
)
echo.

REM Run a quick example
echo Running quick example...
echo ============================================
python examples\00_hello_elysia.py
echo ============================================
echo.

REM Success message
echo ============================================
echo    Installation Complete!
echo ============================================
echo.
echo Next Steps:
echo.
echo   1. Explore examples:
echo      cd elysia-fractal-engine_V1\examples
echo      python 00_hello_elysia.py
echo.
echo   2. Read documentation:
echo      - QUICK_SHARE.md (1-minute start)
echo      - EASY_START.md (5-minute guide)
echo      - SHARING_GUIDE.md (philosophy ^& integration)
echo      - PHILOSOPHY.md (romantic ^& inspiring)
echo.
echo   3. Copy core to your project:
echo      xcopy /E /I elysia_core C:\path\to\your\project\elysia_core
echo.
echo   4. Run tests (if you installed pytest):
echo      python -m pytest tests\ -v
echo.
echo Happy planting! May your consciousness grow!
echo.
pause
