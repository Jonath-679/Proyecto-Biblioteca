@echo off
REM ==========================================================
REM  Sistema de Biblioteca - Equipo 3
REM  Genera una version .EXE que NO necesita Python instalado.
REM  Resultado: carpeta dist\Biblioteca  (copia esa carpeta completa)
REM ==========================================================
title Construir ejecutable - Biblioteca
cd /d "%~dp0"

set "PY="
py -3 --version >nul 2>nul && set "PY=py -3"
if not defined PY python --version >nul 2>nul && set "PY=python"
if not defined PY (
    echo [ERROR] Se necesita Python para construir el ejecutable.
    pause
    exit /b 1
)

echo Instalando herramientas de construccion...
%PY% -m pip install --user -r requirements.txt pyinstaller
if errorlevel 1 %PY% -m pip install -r requirements.txt pyinstaller

echo.
echo Construyendo ejecutable, puede tardar unos minutos...
%PY% -m PyInstaller --noconfirm --clean --windowed --name Biblioteca main.py
if errorlevel 1 (
    echo [ERROR] Fallo la construccion.
    pause
    exit /b 1
)

REM los datos (base de datos, portadas, sonidos) van junto al .exe
REM para que se puedan modificar y respaldar facilmente
echo Copiando base de datos y recursos...
if exist biblioteca.db copy /Y biblioteca.db dist\Biblioteca\ >nul
xcopy /E /I /Y recursos dist\Biblioteca\recursos >nul

echo.
echo ==========================================================
echo  LISTO. El programa quedo en:  dist\Biblioteca\Biblioteca.exe
echo  Copia la carpeta dist\Biblioteca completa a la otra PC.
echo ==========================================================
pause
