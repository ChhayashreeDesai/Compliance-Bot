# Run Streamlit Web Application for Compliance Auditor

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "`n╔═════════════════════════════════════════════╗`n║  COMPLIANCE AUDITOR - Streamlit Web App    ║`n╚═════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "Starting web application...`n" -ForegroundColor Green
Write-Host "🌐 Open your browser to: http://localhost:8501`n" -ForegroundColor White
Write-Host "Press Ctrl+C to stop the server.`n" -ForegroundColor Yellow

& .\.venv\Scripts\streamlit run web\app.py
