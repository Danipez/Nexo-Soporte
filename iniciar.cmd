@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -File scripts\abrir_nexo.ps1
if errorlevel 1 pause
