#!/usr/bin/env bash
# Sistema de Biblioteca - Equipo 3
# Lanzador para Linux / macOS:  bash iniciar.sh  (o ./iniciar.sh)

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)" || exit 1
cd "$SCRIPT_DIR" || exit 1

check_python() {
    "$1" -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >/dev/null 2>&1
}

check_deps() {
    "$1" -c "import PyQt6.QtWidgets, PyQt6.QtMultimedia" >/dev/null 2>&1
}

# 1. Buscar Python 3.9+ (prioridad a entorno virtual local)
PY=""
if [ -x ".venv/bin/python" ] && check_python ".venv/bin/python"; then
    PY=".venv/bin/python"
elif [ -x "venv/bin/python" ] && check_python "venv/bin/python"; then
    PY="venv/bin/python"
elif command -v python3 >/dev/null 2>&1 && check_python "python3"; then
    PY="python3"
elif command -v python >/dev/null 2>&1 && check_python "python"; then
    PY="python"
fi

if [ -z "$PY" ]; then
    echo "[ERROR] No se encontro Python 3.9 o superior. Instalalo y vuelve a intentar."
    exit 1
fi

# 2. Verificar e instalar dependencias si faltan
if ! check_deps "$PY"; then
    echo "Instalando dependencias (solo la primera vez)..."

    in_venv=$("$PY" -c "import sys; print(1 if sys.prefix != sys.base_prefix else 0)" 2>/dev/null)
    if [ "$in_venv" = "1" ]; then
        "$PY" -m pip install -r requirements.txt || exit 1
    elif "$PY" -m venv .venv >/dev/null 2>&1 && [ -x ".venv/bin/python" ]; then
        PY=".venv/bin/python"
        "$PY" -m pip install -r requirements.txt || exit 1
    else
        # Respaldo si python3-venv no esta instalado
        if ! "$PY" -m pip install --user -r requirements.txt 2>/dev/null; then
            echo "[ERROR] No se pudo instalar PyQt6."
            echo "En Linux moderno (PEP 668), instala venv o PyQt6 desde tu gestor de paquetes:"
            echo "  Debian/Ubuntu: sudo apt install python3-venv python3-pyqt6 python3-pyqt6.qtmultimedia"
            echo "  Arch Linux:    sudo pacman -S python-pyqt6"
            echo "  Fedora:        sudo dnf install python3-pyqt6"
            exit 1
        fi
    fi

    if ! check_deps "$PY"; then
        echo "[ERROR] PyQt6 se instalo pero no pudo importarse correctamente."
        exit 1
    fi
fi

# 3. Ejecutar el programa
exec "$PY" main.py "$@"
