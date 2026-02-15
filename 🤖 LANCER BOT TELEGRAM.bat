@echo off
chcp 65001 >nul
title 🤖 BLACKROCK SCREENER — BOT TELEGRAM
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║  🤖 BLACKROCK SCREENER — BOT TELEGRAM   ║
echo  ║  Rapport quotidien TOP 10 x 3 horizons  ║
echo  ╚══════════════════════════════════════════╝
echo.
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe telegram_bot.py
) else (
    python telegram_bot.py
)
pause
