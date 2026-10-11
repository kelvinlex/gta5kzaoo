@echo off
title GTA V Web - Servidor Local
cd /d "%~dp0"
echo ====================================================
echo       Iniciando GTA V Web (Sem Anuncios)
echo ====================================================
echo.
echo Abrindo o jogo no navegador em http://localhost:8000/ ...
echo.
"runtime\python.exe" "serve_local.py" --open
pause
