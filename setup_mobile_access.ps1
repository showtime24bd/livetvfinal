# ========================================
# Mobile/Android TV Access Setup Script
# ========================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Live TV Mobile Access Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  WARNING: Not running as Administrator!" -ForegroundColor Yellow
    Write-Host "Some features may not work properly." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To run as Admin:" -ForegroundColor Cyan
    Write-Host "Right-click PowerShell → Run as Administrator" -ForegroundColor Cyan
    Write-Host "Then run: .\setup_mobile_access.ps1" -ForegroundColor Cyan
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne 'y') {
        exit
    }
}

Write-Host "🔍 Step 1: Detecting Network Information..." -ForegroundColor Green
Write-Host ""

# Get local IP address
$ipAddresses = Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
    $_.IPAddress -notlike "127.*" -and 
    $_.IPAddress -notlike "169.254.*" -and
    $_.PrefixOrigin -ne "WellKnown"
}

if ($ipAddresses.Count -eq 0) {
    Write-Host "❌ No network connection found!" -ForegroundColor Red
    Write-Host "Please connect to Wi-Fi and try again." -ForegroundColor Yellow
    pause
    exit
}

Write-Host "📡 Available Network Interfaces:" -ForegroundColor Cyan
$ipAddresses | ForEach-Object {
    $adapter = Get-NetAdapter -InterfaceIndex $_.InterfaceIndex
    Write-Host "  - $($adapter.Name): $($_.IPAddress)" -ForegroundColor White
}
Write-Host ""

# Select primary IP (prefer WiFi)
$primaryIP = ($ipAddresses | Where-Object {
    $adapter = Get-NetAdapter -InterfaceIndex $_.InterfaceIndex
    $adapter.Name -like "*Wi-Fi*" -or $adapter.Name -like "*Wireless*"
} | Select-Object -First 1)

if (-not $primaryIP) {
    $primaryIP = $ipAddresses | Select-Object -First 1
}

$computerIP = $primaryIP.IPAddress
Write-Host "✅ Selected IP: $computerIP" -ForegroundColor Green
Write-Host ""

# Check Flask port
Write-Host "🔍 Step 2: Checking Flask Application..." -ForegroundColor Green
Write-Host ""

$flaskPort = 5000
$flaskRunning = Get-NetTCPConnection -LocalPort $flaskPort -State Listen -ErrorAction SilentlyContinue

if ($flaskRunning) {
    Write-Host "✅ Flask app is running on port $flaskPort" -ForegroundColor Green
    $processId = $flaskRunning.OwningProcess
    $process = Get-Process -Id $processId
    Write-Host "   Process: $($process.ProcessName) (PID: $processId)" -ForegroundColor Gray
} else {
    Write-Host "⚠️  Flask app is NOT running on port $flaskPort" -ForegroundColor Yellow
    Write-Host "   Start it with: python app.py" -ForegroundColor Cyan
}
Write-Host ""

# Check/Create Firewall Rule
Write-Host "🔍 Step 3: Configuring Windows Firewall..." -ForegroundColor Green
Write-Host ""

$ruleName = "Flask Live TV App"
$existingRule = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue

if ($existingRule) {
    Write-Host "✅ Firewall rule already exists: $ruleName" -ForegroundColor Green
    
    # Check if rule is enabled
    if ($existingRule.Enabled -eq $true) {
        Write-Host "   Status: Enabled" -ForegroundColor Green
    } else {
        Write-Host "   Status: Disabled" -ForegroundColor Yellow
        if ($isAdmin) {
            Write-Host "   Enabling rule..." -ForegroundColor Cyan
            Enable-NetFirewallRule -DisplayName $ruleName
            Write-Host "   ✅ Rule enabled" -ForegroundColor Green
        }
    }
} else {
    Write-Host "⚠️  Firewall rule does NOT exist" -ForegroundColor Yellow
    
    if ($isAdmin) {
        Write-Host "   Creating firewall rule..." -ForegroundColor Cyan
        try {
            New-NetFirewallRule -DisplayName $ruleName `
                               -Direction Inbound `
                               -LocalPort $flaskPort `
                               -Protocol TCP `
                               -Action Allow `
                               -Profile Any `
                               -Description "Allow inbound traffic for Flask Live TV application" `
                               -ErrorAction Stop | Out-Null
            Write-Host "   ✅ Firewall rule created successfully!" -ForegroundColor Green
        } catch {
            Write-Host "   ❌ Failed to create firewall rule: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "   ⚠️  Need Administrator rights to create firewall rule" -ForegroundColor Yellow
        Write-Host "   Run this script as Administrator" -ForegroundColor Cyan
    }
}
Write-Host ""

# Network Profile Check
Write-Host "🔍 Step 4: Checking Network Profile..." -ForegroundColor Green
Write-Host ""

$connectionProfile = Get-NetConnectionProfile | Where-Object {
    $_.IPv4Connectivity -eq "Internet" -or $_.IPv4Connectivity -eq "LocalNetwork"
} | Select-Object -First 1

if ($connectionProfile) {
    Write-Host "   Network: $($connectionProfile.Name)" -ForegroundColor White
    Write-Host "   Category: $($connectionProfile.NetworkCategory)" -ForegroundColor White
    
    if ($connectionProfile.NetworkCategory -eq "Public") {
        Write-Host "   ⚠️  Network is set to Public" -ForegroundColor Yellow
        Write-Host "   For better connectivity, consider changing to Private" -ForegroundColor Yellow
        
        if ($isAdmin) {
            $changeProfile = Read-Host "   Change to Private? (y/n)"
            if ($changeProfile -eq 'y') {
                Set-NetConnectionProfile -InterfaceIndex $connectionProfile.InterfaceIndex -NetworkCategory Private
                Write-Host "   ✅ Changed to Private" -ForegroundColor Green
            }
        }
    } else {
        Write-Host "   ✅ Network profile is OK" -ForegroundColor Green
    }
}
Write-Host ""

# Port availability test
Write-Host "🔍 Step 5: Testing Port Availability..." -ForegroundColor Green
Write-Host ""

$portTest = Test-NetConnection -ComputerName localhost -Port $flaskPort -InformationLevel Quiet -WarningAction SilentlyContinue

if ($portTest) {
    Write-Host "✅ Port $flaskPort is accessible" -ForegroundColor Green
} else {
    Write-Host "❌ Port $flaskPort is NOT accessible" -ForegroundColor Red
    if (-not $flaskRunning) {
        Write-Host "   Reason: Flask app is not running" -ForegroundColor Yellow
    } else {
        Write-Host "   Reason: Port might be blocked" -ForegroundColor Yellow
    }
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  📋 SETUP SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Your Computer IP: " -NoNewline -ForegroundColor White
Write-Host "$computerIP" -ForegroundColor Yellow
Write-Host ""

Write-Host "Access URL from Mobile/TV:" -ForegroundColor White
Write-Host "  http://$computerIP`:$flaskPort" -ForegroundColor Green -BackgroundColor Black
Write-Host ""

if ($flaskRunning) {
    Write-Host "✅ Flask App: Running" -ForegroundColor Green
} else {
    Write-Host "❌ Flask App: Not Running" -ForegroundColor Red
    Write-Host "   Start with: python app.py" -ForegroundColor Cyan
}

if ($existingRule -and $existingRule.Enabled) {
    Write-Host "✅ Firewall: Configured" -ForegroundColor Green
} else {
    Write-Host "⚠️  Firewall: Needs Configuration" -ForegroundColor Yellow
}

Write-Host ""

# QR Code suggestion
Write-Host "💡 Pro Tip:" -ForegroundColor Cyan
Write-Host "Create a QR code for easy mobile access:" -ForegroundColor White
Write-Host "Visit: https://www.qr-code-generator.com/" -ForegroundColor Cyan
Write-Host "URL: http://$computerIP`:$flaskPort" -ForegroundColor Yellow
Write-Host ""

# Troubleshooting
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🔧 TROUBLESHOOTING" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "If mobile access doesn't work:" -ForegroundColor White
Write-Host ""
Write-Host "1. Ensure mobile is on SAME Wi-Fi network" -ForegroundColor Yellow
Write-Host "2. Start Flask app if not running:" -ForegroundColor Yellow
Write-Host "   python app.py" -ForegroundColor Cyan
Write-Host "3. Try disabling firewall temporarily (test only):" -ForegroundColor Yellow
Write-Host "   Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False" -ForegroundColor Cyan
Write-Host "4. Check router AP Isolation settings" -ForegroundColor Yellow
Write-Host "5. Try different port (8080, 8000, etc.)" -ForegroundColor Yellow
Write-Host ""

# Test connection offer
Write-Host "========================================" -ForegroundColor Cyan
$testNow = Read-Host "Start Flask app now? (y/n)"

if ($testNow -eq 'y') {
    Write-Host ""
    Write-Host "Starting Flask app..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host ""
    
    $appPath = Join-Path $PSScriptRoot "app.py"
    if (Test-Path $appPath) {
        python $appPath
    } else {
        Write-Host "❌ app.py not found in current directory" -ForegroundColor Red
        Write-Host "Current directory: $PSScriptRoot" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "Setup complete! 🎉" -ForegroundColor Green
    Write-Host ""
    pause
}
