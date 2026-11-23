import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta

from rutas import RUTA_DB

# ruta relativa a la carpeta del proyecto (portable)
ruta_db = RUTA_DB


@contextmanager
def abrir_conexion():
    """Abre una conexion SQLite segura: hace commit al terminar, rollback si hay error y siempre cierra."""
    conexion = sqlite3.connect(ruta_db)
    try:
        yield conexion
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


class ModeloLogin:
    def verificar_usuario(self, usuario, contrasena):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM Usuarios_Admin WHERE usuario = ? AND contrasena = ?",
                (usuario, contrasena)
            )
            return cursor.fetchone()


class ModeloEtiquetas:
    def obtener_etiquetas(self):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre_etiqueta FROM Etiquetas")
            return [fila[0] for fila in cursor.fetchall()]

    def anadir_etiqueta(self, nombre):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO Etiquetas (nombre_etiqueta) VALUES (?)",
                (nombre,)
            )


class ModeloLibros:
    def obtener_todos_los_libros(self):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Libros")
            return cursor.fetchall()

    def buscar_libros(self, texto_busqueda):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            busqueda = f"%{texto_busqueda}%"

            cursor.execute(
                "SELECT * FROM Libros WHERE titulo LIKE ? OR codigo LIKE ? OR etiquetas LIKE ?",
                (busqueda, busqueda, busqueda)
            )
            directos = cursor.fetchall()

            if not directos:
                return []

            etiquetas_encontradas = set()
            for libro in directos:
                if libro[8]:
                    etiquetas_libro = libro[8].split()
                    for et in etiquetas_libro:
                        etiquetas_encontradas.add(et)

            similares = []
            if etiquetas_encontradas:
                ids_directos = [str(libro[0]) for libro in directos]
                placeholders_ids = ",".join("?" for _ in ids_directos)
                
                query_similares = f"SELECT * FROM Libros WHERE id_libro NOT IN ({placeholders_ids}) AND ("
                condiciones_tags = []
                parametros_similares = list(ids_directos)

                for et in etiquetas_encontradas:
                    condiciones_tags.append("etiquetas LIKE ?")
                    parametros_similares.append(f"%{et}%")
                
                query_similares += " OR ".join(condiciones_tags) + ")"
                
                cursor.execute(query_similares, parametros_similares)
                similares = cursor.fetchall()

            return directos + similares

    def anadir_libro(self, titulo, codigo, id_ubicacion, cantidad, paginas, creador, etiquetas):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO Libros (titulo, codigo, id_ubicacion, cantidad_total, cantidad_disponible, paginas, creador, etiquetas) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (titulo, codigo, id_ubicacion, cantidad, cantidad, paginas, creador, etiquetas)
            )

    def contar_prestados(self, id_libro):
        # cuantas copias de este libro estan prestadas y sin devolver
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM Detalle_Prestamos WHERE id_libro = ? AND devuelto = 0",
                (id_libro,)
            )
            return cursor.fetchone()[0]

    def obtener_libro_por_id(self, id_libro):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Libros WHERE id_libro = ?", (id_libro,))
            return cursor.fetchone()

    def actualizar_libro(self, id_libro, titulo, codigo, id_ubicacion, cantidad, paginas, creador, etiquetas):
        # la cantidad disponible se recalcula restando las copias prestadas
        # (antes se igualaba a la cantidad total y se "perdian" los prestamos)
        prestados = self.contar_prestados(id_libro)
        if cantidad < prestados:
            raise ValueError(
                f"hay {prestados} copias prestadas, la cantidad total no puede ser menor"
            )
        disponibles = cantidad - prestados

        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE Libros SET titulo = ?, codigo = ?, id_ubicacion = ?, cantidad_total = ?, cantidad_disponible = ?, paginas = ?, creador = ?, etiquetas = ? WHERE id_libro = ?",
                (titulo, codigo, id_ubicacion, cantidad, disponibles, paginas, creador, etiquetas, id_libro)
            )

    def eliminar_libro(self, id_libro):
        # no se permite borrar un libro que tiene copias prestadas
        # (dejaria prestamos huerfanos imposibles de devolver)
        if self.contar_prestados(id_libro) > 0:
            return False
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Libros WHERE id_libro = ?", (id_libro,))
        return True

    def obtener_libros_por_ubicaciones(self, ids_ubicaciones):
        if not ids_ubicaciones:
            return []
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            placeholders = ",".join("?" for _ in ids_ubicaciones)
            cursor.execute(f"SELECT * FROM Libros WHERE id_ubicacion IN ({placeholders})", ids_ubicaciones)
            return cursor.fetchall()

    def mover_libros_masivo(self, ids_ubicaciones_viejas, id_nueva_ubicacion):
        if not ids_ubicaciones_viejas:
            return
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            placeholders = ",".join("?" for _ in ids_ubicaciones_viejas)
            parametros = [id_nueva_ubicacion] + list(ids_ubicaciones_viejas)
            cursor.execute(f"UPDATE Libros SET id_ubicacion = ? WHERE id_ubicacion IN ({placeholders})", parametros)


class ModeloUbicaciones:
    def obtener_ubicaciones(self):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_ubicacion, estante, lado, separacion FROM Ubicaciones")
            return cursor.fetchall()

    def obtener_ubicacion_por_id(self, id_ubicacion):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT estante, lado, separacion FROM Ubicaciones WHERE id_ubicacion = ?", (id_ubicacion,))
            return cursor.fetchone()

    def anadir_ubicacion(self, estante, lado, separacion):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO Ubicaciones (estante, lado, separacion) VALUES (?, ?, ?)", (estante, str(lado), str(separacion)))

    def contar_libros_estante(self, estante):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM Libros
                WHERE id_ubicacion IN (SELECT id_ubicacion FROM Ubicaciones WHERE estante = ?)
            ''', (estante,))
            return cursor.fetchone()[0]

    def eliminar_estante(self, estante):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            # los libros del estante quedan "sin ubicacion" en lugar de apuntar
            # a una ubicacion que ya no existe
            cursor.execute('''
                UPDATE Libros SET id_ubicacion = NULL
                WHERE id_ubicacion IN (SELECT id_ubicacion FROM Ubicaciones WHERE estante = ?)
            ''', (estante,))
            cursor.execute("DELETE FROM Ubicaciones WHERE estante = ?", (estante,))

    def eliminar_ultima_separacion(self, estante):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT MAX(CAST(separacion AS INTEGER)) FROM Ubicaciones WHERE estante = ?", (estante,))
            max_sep = cursor.fetchone()[0]
            if max_sep:
                cursor.execute("DELETE FROM Ubicaciones WHERE estante = ? AND separacion = ?", (estante, str(max_sep)))

    def obtener_ids_separacion(self, estante, separacion):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_ubicacion FROM Ubicaciones WHERE estante = ? AND separacion = ?", (estante, str(separacion)))
            return [fila[0] for fila in cursor.fetchall()]


class ModeloLectores:
    def anadir_lector(self, tipo_registro, identificacion, nombre_completo, carrera_o_extra, telefono):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO Lectores (tipo_registro, identificacion, nombre_completo, carrera_o_extra, telefono, estado_castigo) VALUES (?, ?, ?, ?, ?, NULL)",
                (tipo_registro, identificacion, nombre_completo, carrera_o_extra, telefono)
            )

    def existe_identificacion(self, identificacion, excluir_id=None):
        # evita registrar dos lectores con el mismo codigo / curp
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            if excluir_id is None:
                cursor.execute("SELECT 1 FROM Lectores WHERE identificacion = ?", (identificacion,))
            else:
                cursor.execute(
                    "SELECT 1 FROM Lectores WHERE identificacion = ? AND id_lector != ?",
                    (identificacion, excluir_id)
                )
            return cursor.fetchone() is not None

    def obtener_castigo(self, id_lector):
        # regresa la fecha (texto YYYY-MM-DD) hasta la que el lector esta
        # bloqueado, o None si no tiene castigo vigente
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT estado_castigo FROM Lectores WHERE id_lector = ?", (id_lector,))
            fila = cursor.fetchone()
        if not fila or not fila[0]:
            return None
        hoy = datetime.now().strftime("%Y-%m-%d")
        return fila[0] if fila[0] >= hoy else None

    def buscar_lectores(self, texto):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            busqueda = f"%{texto}%"
            cursor.execute(
                "SELECT * FROM Lectores WHERE nombre_completo LIKE ? OR identificacion LIKE ? OR telefono LIKE ?",
                (busqueda, busqueda, busqueda)
            )
            return cursor.fetchall()

    def buscar_lectores_con_prestamos(self, texto):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            busqueda = f"%{texto}%"
            # se une con Libros para no mostrar lectores cuyos unicos prestamos
            # pertenecen a libros que ya no existen
            cursor.execute('''
                SELECT DISTINCT l.* 
                FROM Lectores l
                JOIN Prestamos p ON l.id_lector = p.id_lector
                JOIN Detalle_Prestamos dp ON p.id_prestamo = dp.id_prestamo
                JOIN Libros lb ON dp.id_libro = lb.id_libro
                WHERE dp.devuelto = 0 AND (l.nombre_completo LIKE ? OR l.identificacion LIKE ? OR l.telefono LIKE ?)
            ''', (busqueda, busqueda, busqueda))
            return cursor.fetchall()

    def actualizar_lector(self, id_lector, nombre, carrera, telefono):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE Lectores SET nombre_completo = ?, carrera_o_extra = ?, telefono = ? WHERE id_lector = ?",
                (nombre, carrera, telefono, id_lector)
            )


class ModeloPrestamos:
    def registrar_prestamo(self, id_lector, lista_libros_dias):
        fecha_salida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO Prestamos (id_lector, fecha_hora_salida, estado) VALUES (?, ?, ?)",
                (id_lector, fecha_salida, "ACTIVO")
            )
            id_prestamo = cursor.lastrowid

            for libro_dias in lista_libros_dias:
                id_libro = libro_dias[0]
                dias = libro_dias[1]

                # se verifica la disponibilidad real en la base de datos
                # (el carrito pudo haberse llenado con datos viejos)
                cursor.execute(
                    "SELECT titulo, cantidad_disponible FROM Libros WHERE id_libro = ?",
                    (id_libro,)
                )
                fila = cursor.fetchone()
                if fila is None:
                    raise ValueError("uno de los libros del carrito ya no existe")
                if fila[1] <= 0:
                    raise ValueError(f"ya no hay copias disponibles de: {fila[0]}")

                # se agregan 5 horas de tolerancia a la fecha limite
                fecha_limite = (datetime.now() + timedelta(days=dias, hours=5)).strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute(
                    "INSERT INTO Detalle_Prestamos (id_prestamo, id_libro, dias_prestamo, fecha_hora_limite, devuelto, multa_pesos, dias_retraso) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (id_prestamo, id_libro, dias, fecha_limite, False, 0.0, 0)
                )

                cursor.execute(
                    "UPDATE Libros SET cantidad_disponible = cantidad_disponible - 1 WHERE id_libro = ?",
                    (id_libro,)
                )

    def obtener_prestamos_activos(self, id_lector):
        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                SELECT dp.id_detalle, l.id_libro, l.titulo, dp.fecha_hora_limite
                FROM Detalle_Prestamos dp
                JOIN Prestamos p ON dp.id_prestamo = p.id_prestamo
                JOIN Libros l ON dp.id_libro = l.id_libro
                WHERE p.id_lector = ? AND dp.devuelto = 0
            ''', (id_lector,))
            return cursor.fetchall()

    def devolver_libro(self, id_detalle, id_libro, multa, dias_retraso, id_lector, aplicar_castigo):
        fecha_devolucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with abrir_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE Detalle_Prestamos SET devuelto = 1, fecha_hora_devolucion = ?, multa_pesos = ?, dias_retraso = ? WHERE id_detalle = ?",
                (fecha_devolucion, multa, dias_retraso, id_detalle)
            )

            # nunca se supera la cantidad total
            cursor.execute(
                "UPDATE Libros SET cantidad_disponible = MIN(cantidad_total, cantidad_disponible + 1) WHERE id_libro = ?",
                (id_libro,)
            )

            # si ya se devolvieron todos los libros del prestamo se marca como finalizado
            cursor.execute('''
                UPDATE Prestamos SET estado = 'FINALIZADO'
                WHERE id_prestamo = (SELECT id_prestamo FROM Detalle_Prestamos WHERE id_detalle = ?)
                AND NOT EXISTS (
                    SELECT 1 FROM Detalle_Prestamos
                    WHERE id_prestamo = Prestamos.id_prestamo AND devuelto = 0
                )
            ''', (id_detalle,))

            if aplicar_castigo:
                fecha_castigo = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
                cursor.execute(
                    "UPDATE Lectores SET estado_castigo = ? WHERE id_lector = ?",
                    (fecha_castigo, id_lector)
                )