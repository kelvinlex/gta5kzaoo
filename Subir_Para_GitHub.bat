@echo off
title Subir GTA Web para o GitHub
cd /d "%~dp0"
echo ====================================================
echo        Enviando projeto para o seu GitHub...
echo        Repositorio: kelvinlex/gta5kzaoo
echo ====================================================
echo.
git push -u origin main
if errorlevel 1 (
    echo.
    echo Tentando com force (caso o repositorio tenha sido criado com README)...
    git push -u origin main --force
)
echo.
echo ====================================================
echo Concluido! Verifique seu GitHub:
echo https://github.com/kelvinlex/gta5kzaoo
echo ====================================================
pause
