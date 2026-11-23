# Sistema de Gestión de Biblioteca Universitaria — Equipo 3

Aplicación de escritorio desarrollada en **Python 3** con **PyQt6** y **SQLite** para la administración integral de una biblioteca universitaria: catálogo visual de libros con portadas, búsqueda inteligente con recomendaciones por etiquetas, control de lectores (estudiantes y público general), mapa físico de estanterías, carrito de préstamos y recepción de devoluciones con cálculo automático de multas y sanciones.

---

## Características principales

- **Control de acceso administrativo**: inicio de sesión para personal bibliotecario (admite inicio con la tecla `Enter`).
- **Catálogo visual y búsqueda inteligente**: vista en cuadrícula con portadas; busca por título, código o `#etiqueta` y sugiere automáticamente libros similares que compartan etiquetas.
- **Gestión completa de libros y portadas**: alta, edición, eliminación protegida (no permite borrar ejemplares con préstamos activos), etiquetas personalizadas y carga/reemplazo/eliminación de portadas (`.png`, `.jpg`, `.jpeg`).
- **Control de lectores**: registro diferenciado para comunidad universitaria (`escuela`: código de estudiante y carrera) y `publico general` (CURP), con validación de duplicados y teléfono a 10 dígitos.
- **Carrito de préstamos**: hasta **3 libros** por operación, plazo configurable de **1 a 30 días** por libro, verificación en tiempo real de inventario y bloqueo automático a lectores sancionados.
- **Recepción de devoluciones, multas y castigos**:
  - Tolerancia de **5 horas** adicionales sobre los días de préstamo.
  - Multa automática de **\$20.00 MXN** por día (o fracción) de retraso.
  - Bloqueo automático del lector por **7 días** cuando el retraso supera los **2 días**.
- **Mapa físico de ubicaciones**: administración visual de estantes (`A`–`Z`), lados (`1` izquierdo / `2` derecho) y separaciones, con asistente para reubicar libros en masa al eliminar una fila.
- **100 % portable**: todas las rutas son relativas al directorio del proyecto (`rutas.py`) y la base de datos se inicializa automáticamente al arrancar si no existe.

---

## Acceso por defecto

| Campo | Valor |
| :--- | :--- |
| **Usuario** | `admin` |
| **Contraseña** | `1234` |
| **Rol** | `bibliotecario` |

---

## Cómo portar y ejecutar el programa en otra computadora

El proyecto está preparado para copiarse completo (mediante USB, carpeta comprimida o red local) a cualquier otra computadora sin necesidad de reconfigurar rutas.

### Opción 1: Copiar la carpeta (equipo con Python 3.9 o superior)

1. Copia la **carpeta completa** `proyecto_biblioteca` a la otra PC (incluyendo `biblioteca.db` y la carpeta `recursos/` si deseas conservar los libros, portadas y registros existentes).
2. En **Windows**, haz doble clic en **`iniciar.bat`**:
   - Detecta automáticamente Python.
   - La primera vez instala `PyQt6` desde `requirements.txt` (requiere conexión a internet únicamente en esa primera ejecución).
   - Inicia la aplicación directamente.
3. En **Linux / macOS**, abre una terminal dentro de la carpeta y ejecuta:
   ```bash
   bash iniciar.sh
   ```
4. También puedes ejecutarlo manualmente desde terminal:
   ```bash
   python -m pip install -r requirements.txt
   python main.py
   ```

> **Nota sobre instalaciones limpias:** Si copias el proyecto sin el archivo `biblioteca.db`, el programa creará automáticamente una base de datos nueva al abrirse con el usuario `admin` (`1234`), los estantes iniciales `A` y `B` (lados 1 y 2, separaciones 1 a 5) y las etiquetas base.

### Opción 2: Crear un ejecutable `.exe` (para PCs SIN Python instalado)

1. En una computadora Windows que tenga Python, haz doble clic en **`construir_exe.bat`**.
2. El script instalará PyInstaller, compilará el programa y copiará `biblioteca.db` y `recursos/` junto al ejecutable.
3. Copia la carpeta generada **`dist\Biblioteca\`** completa a la otra PC y ejecuta **`Biblioteca.exe`**.

---

## Estructura del proyecto

```text
proyecto_biblioteca/
├── main.py                         # Punto de entrada, manejador global de errores e inicio de BD
├── rutas.py                        # Módulo central de rutas portables (Python y PyInstaller)
├── biblioteca.db                   # Base de datos SQLite (se crea sola si no existe)
├── requirements.txt                # Dependencias del proyecto (PyQt6)
├── iniciar.bat                     # Lanzador automático para Windows
├── iniciar.sh                      # Lanzador automático para Linux / macOS
├── construir_exe.bat               # Generador de ejecutable standalone (.exe)
├── README.md                       # Guía rápida del proyecto
├── docs/
│   └── DOCUMENTACION_COMPLETA.md   # Documentación técnica, arquitectura y manual de usuario
├── database/
│   ├── __init__.py
│   └── conexion.py                 # Creación de tablas SQLite y datos iniciales
├── modelo/
│   ├── __init__.py
│   └── modelos.py                  # Acceso a datos y lógica transaccional SQLite
├── controlador/
│   ├── __init__.py
│   ├── login_controlador.py
│   ├── principal_controlador.py
│   ├── anadir_libro_controlador.py
│   ├── detalles_libro_controlador.py
│   ├── anadir_usuario_controlador.py
│   ├── editar_usuario_controlador.py
│   ├── prestar_controlador.py
│   ├── recibir_libros_controlador.py
│   └── ubicaciones_controlador.py
├── vista/
│   ├── __init__.py
│   ├── login_vista.py
│   ├── principal_vista.py
│   ├── anadir_libro_vista.py
│   ├── detalles_libro_vista.py
│   ├── anadir_usuario_vista.py
│   ├── editar_usuario_vista.py
│   ├── prestar_vista.py
│   ├── recibir_libros_vista.py
│   └── ubicaciones_vista.py
└── recursos/
    ├── imagenes/                   # Portadas de libros (<CODIGO>.png / .jpg / .jpeg)
    └── sonidos/
        └── exito.wav               # Efecto de sonido en préstamos y devoluciones
```

---

## Documentación completa

Consulta el documento profesional completo con introducción, objetivos, requisitos funcionales y no funcionales, arquitectura MVC, diagrama entidad-relación, diccionario de datos, manual de usuario, guía de portabilidad y bitácora de pruebas/correcciones en:

- **[Documentación Completa del Sistema (`docs/DOCUMENTACION_COMPLETA.md`)](docs/DOCUMENTACION_COMPLETA.md)**
