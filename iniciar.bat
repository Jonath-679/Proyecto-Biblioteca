@echo off
REM ==========================================================
REM  Sistema de Biblioteca - Equipo 3
REM  Lanzador portable: doble clic para abrir el programa.
REM  - Busca Python 3.9+ en la computadora (o usa .venv / venv)
REM  - Instala PyQt6 automaticamente la primera vez
REM  - Ejecuta main.py desde esta misma carpeta
REM ==========================================================
title Sistema de Biblioteca - Equipo 3
pushd "%~dp0" >nul 2>nul || (
    echo [ERROR] No se pudo acceder a la carpeta del proyecto.
    pause
    exit /b 1
)

REM ---- 1. buscar python 3.9+ (prioridad a entorno virtual local) ----
set "PY="
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>nul && set "PY=.venv\Scripts\python.exe"
)
if not defined PY if exist "venv\Scripts\python.exe" (
    "venv\Scripts\python.exe" -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>nul && set "PY=venv\Scripts\python.exe"
)
if not defined PY (
    py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>nul && set "PY=py -3"
)
if not defined PY (
    python -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>nul && set "PY=python"
)
if not defined PY (
    python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>nul && set "PY=python3"
)

if not defined PY goto :sin_python

REM ---- 2. verificar dependencias ----
%PY% -c "import PyQt6.QtWidgets, PyQt6.QtMultimedia" >nul 2>nul
if not errorlevel 1 goto :ejecutar

echo.
echo  Instalando dependencias, solo se hace la primera vez...
echo.

REM Si ya estamos en un entorno virtual, instalar ahi directamente
%PY% -c "import sys; sys.exit(0 if sys.prefix != sys.base_prefix else 1)" >nul 2>nul
if not errorlevel 1 (
    %PY% -m pip install -r requirements.txt
    goto :verificar_deps
)

REM Intentar crear un entorno virtual local (.venv) para no ensuciar Python global
%PY% -m venv .venv >nul 2>nul
if not errorlevel 1 if exist ".venv\Scripts\python.exe" (
    set "PY=.venv\Scripts\python.exe"
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    goto :verificar_deps
)

REM Respaldo si venv no esta disponible
%PY% -m pip install --user -r requirements.txt
if errorlevel 1 %PY% -m pip install -r requirements.txt

:verificar_deps
%PY% -c "import PyQt6.QtWidgets, PyQt6.QtMultimedia" >nul 2>nul
if errorlevel 1 goto :error_dependencias

REM ---- 3. ejecutar el programa ----
:ejecutar
%PY% main.py %*
set "EXIT_CODE=%errorlevel%"
if not "%EXIT_CODE%"=="0" (
    echo.
    echo  El programa se cerro con un error ^(codigo %EXIT_CODE%^). Revisa el mensaje de arriba.
    pause
)
popd >nul 2>nul
exit /b %EXIT_CODE%

:sin_python
echo.
echo  [ERROR] No se encontro Python 3.9 o superior en esta computadora.
echo.
echo  1. Descargalo de https://www.python.org/downloads/
echo  2. Durante la instalacion marca la casilla "Add python.exe to PATH"
echo  3. Vuelve a abrir este archivo
echo.
pause
popd >nul 2>nul
exit /b 1

:error_dependencias
echo.
echo  [ERROR] No se pudo instalar PyQt6.
echo  Verifica tu conexion a internet o ejecuta manualmente:
echo      python -m pip install -r requirements.txt
echo.
pause
popd >nul 2>nul
exit /b 1
