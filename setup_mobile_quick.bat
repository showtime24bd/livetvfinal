@echo off
:: ========================================
:: Quick Mobile Access Setup
:: ========================================

title Live TV Mobile Access Setup

echo ========================================
echo   Live TV Mobile Access Setup
echo ========================================
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Running as Administrator
    echo.
) else (
    echo [WARNING] Not running as Administrator!
    echo Some features may not work.
    echo.
    echo Right-click this file and select "Run as Administrator"
    echo.
    pause
)

:: Get IP Address
echo Step 1: Finding your IP address...
echo.

for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set IP=%%a
    goto :found
)

:found
set IP=%IP:~1%
echo Your Computer IP: %IP%
echo.

:: Check if Flask is running
echo Step 2: Checking Flask application...
echo.

netstat -ano | findstr ":5000" | findstr "LISTENING" >nul
if %errorLevel% == 0 (
    echo [OK] Flask app is running on port 5000
) else (
    echo [WARNING] Flask app is NOT running
    echo Start it with: python app.py
)
echo.

:: Create Firewall Rule
echo Step 3: Configuring Windows Firewall...
echo.

netsh advfirewall firewall show rule name="Flask Live TV App" >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Firewall rule already exists
) else (
    echo Creating firewall rule...
    netsh advfirewall firewall add rule name="Flask Live TV App" dir=in action=allow protocol=TCP localport=5000 >nul 2>&1
    if %errorLevel% == 0 (
        echo [OK] Firewall rule created successfully
    ) else (
        echo [ERROR] Failed to create firewall rule
        echo Try running as Administrator
    )
)
echo.

:: Summary
echo ========================================
echo   SETUP COMPLETE
echo ========================================
echo.
echo Access from Mobile/Android TV:
echo.
echo     http://%IP%:5000
echo.
echo ========================================
echo.

:: Ask to start Flask
set /p START="Start Flask app now? (y/n): "
if /i "%START%"=="y" (
    echo.
    echo Starting Flask app...
    echo Press Ctrl+C to stop
    echo.
    python app.py
) else (
    echo.
    echo Setup complete!
    pause
)
