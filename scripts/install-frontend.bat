@echo off
chcp 65001 >nul
echo ========================================
echo AI Novel Platform - Frontend Install
echo ========================================
echo.

cd /d "%~dp0frontend"
echo Working directory: %CD%
echo.

echo Installing npm dependencies...
echo This may take a few minutes...
echo.

call npm install

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Installation completed successfully!
    echo ========================================
    echo.
    echo You can now run: npm run dev
    echo.
) else (
    echo.
    echo ========================================
    echo Installation failed with error code %ERRORLEVEL%
    echo ========================================
    echo.
    echo Please check if Node.js and npm are installed correctly.
    echo.
)

pause
