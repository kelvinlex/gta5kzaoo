@echo off
title GTA V Web - Compartilhar Com Amigos
cd /d "%~dp0"
echo ====================================================
echo       Iniciando Servidor e Link Publico...
echo ====================================================
echo.
start "" "runtime\python.exe" "serve_local.py"
timeout /t 2 /nobreak >nul
echo.
echo ====================================================
echo   SEU LINK PUBLICO SERA EXIBIDO ABAIXO:
echo   Envie o link que termina em .trycloudflare.com para seus amigos!
echo ====================================================
echo.
cloudflared tunnel --url http://127.0.0.1:8000
pause
