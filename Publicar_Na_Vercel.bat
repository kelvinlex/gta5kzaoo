@echo off
title Publicar GTA V Web na Nuvem (Vercel)
cd /d "%~dp0"
echo ====================================================
echo        Publicando GTA V Web na Nuvem Vercel
echo ====================================================
echo.
echo Se for a primeira vez, aperte Enter para fazer login com o GitHub.
echo.
call npx vercel --prod --yes
echo.
echo ====================================================
echo Concluido! Seu link permanente 24h/7 esta pronto acima!
echo ====================================================
pause
