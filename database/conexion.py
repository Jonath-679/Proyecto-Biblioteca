import sqlite3
import os
import sys

# permite ejecutar este archivo directamente (python database/conexion.py)
try:
    from rutas import RUTA_DB
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from rutas import RUTA_DB

ruta_db = RUTA_DB

# crea la base de datos y las tablas si no existen
# se llama al iniciar el programa (main.py), por lo que si la base de datos
# no existe en la computadora nueva se genera automaticamente
def conectar():
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuarios_Admin (
            id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            contrasena TEXT,
            rol TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Lectores (
            id_lector INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_registro TEXT,
            identificacion TEXT,
            nombre_completo TEXT,
            carrera_o_extra TEXT,
            telefono TEXT,
            estado_castigo DATE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ubicaciones (
            id_ubicacion INTEGER PRIMARY KEY AUTOINCREMENT,
            estante TEXT,
            lado TEXT,
            separacion TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Libros (
            id_libro INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            codigo TEXT UNIQUE,
            id_ubicacion INTEGER,
            cantidad_total INTEGER,
            cantidad_disponible INTEGER,
            paginas INTEGER,
            creador TEXT,
            etiquetas TEXT,
            FOREIGN KEY (id_ubicacion) REFERENCES Ubicaciones(id_ubicacion)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Prestamos (
            id_prestamo INTEGER PRIMARY KEY AUTOINCREMENT,
            id_lector INTEGER,
            fecha_hora_salida DATETIME,
            estado TEXT,
            FOREIGN KEY (id_lector) REFERENCES Lectores(id_lector)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Detalle_Prestamos (
            id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
            id_prestamo INTEGER,
            id_libro INTEGER,
            dias_prestamo INTEGER,
            fecha_hora_limite DATETIME,
            devuelto BOOLEAN,
            fecha_hora_devolucion DATETIME,
            multa_pesos REAL,
            dias_retraso INTEGER,
            FOREIGN KEY (id_prestamo) REFERENCES Prestamos(id_prestamo),
            FOREIGN KEY (id_libro) REFERENCES Libros(id_libro)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Etiquetas (
            id_etiqueta INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_etiqueta TEXT UNIQUE
        )
    ''')

    cursor.execute("SELECT * FROM Usuarios_Admin WHERE usuario = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO Usuarios_Admin (usuario, contrasena, rol) VALUES ('admin', '1234', 'bibliotecario')")

    cursor.execute("SELECT * FROM Ubicaciones")
    if not cursor.fetchone():
        for estante in ['A', 'B']:
            for lado in ['1', '2']: 
                for separacion in range(1, 6):
                    cursor.execute(
                        "INSERT INTO Ubicaciones (estante, lado, separacion) VALUES (?, ?, ?)",
                        (estante, lado, str(separacion))
                    )

    cursor.execute("SELECT * FROM Etiquetas")
    if not cursor.fetchone():
        for tag in ['#TERROR', '#DIVERSION', '#CIENCIA', '#FICCION', '#ROMANCE']:
            cursor.execute("INSERT OR IGNORE INTO Etiquetas (nombre_etiqueta) VALUES (?)", (tag,))

    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    conectar()