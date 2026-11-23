from vista.detalles_libro_vista import VistaDetallesLibro
from modelo.modelos import ModeloUbicaciones, ModeloLibros
from rutas import buscar_portada, borrar_portadas, guardar_portada
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ControladorDetallesLibro:
    def __init__(self, libro, controlador_principal):
        self.vista = VistaDetallesLibro()
        self.libro = libro
        self.controlador_principal = controlador_principal
        self.modelo_ubicaciones = ModeloUbicaciones()
        self.modelo_libros = ModeloLibros()
        
        self.vista.boton_cambiar_portada.clicked.connect(self.cambiar_portada)
        self.vista.boton_borrar_portada.clicked.connect(self.borrar_portada)
        self.vista.boton_editar.clicked.connect(self.abrir_edicion)
        self.vista.boton_anadir_carrito.clicked.connect(self.anadir_a_lista)
        self.vista.boton_prestar.clicked.connect(self.prestar_directo)
        self.vista.boton_eliminar.clicked.connect(self.eliminar_libro_sistema)
        
        self.llenar_datos()
        self.cargar_imagen()

    def mostrar_alerta(self, titulo, mensaje):
        caja = QMessageBox(self.vista)
        caja.setWindowTitle(titulo)
        caja.setText(mensaje)
        caja.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #E50914;
                color: white;
                font-weight: bold;
                border-radius: 4px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #f40612;
            }
        """)
        caja.exec()

    def llenar_datos(self):
        self.vista.etiqueta_titulo.setText(f"titulo: {self.libro[1]}")
        self.vista.etiqueta_codigo.setText(f"codigo: {self.libro[2]}")
        
        datos_ubi = self.modelo_ubicaciones.obtener_ubicacion_por_id(self.libro[3])
        if datos_ubi:
            texto_ubi = f"ubicacion: {datos_ubi[0]}{datos_ubi[1]}-{datos_ubi[2]} (Estante {datos_ubi[0]}, Lado {datos_ubi[1]}, Separacion {datos_ubi[2]})"
        else:
            texto_ubi = "ubicacion: no asignada"
            
        self.vista.etiqueta_ubicacion.setText(texto_ubi)
        self.vista.etiqueta_disponible.setText(f"cantidad para prestar: {self.libro[5]} de {self.libro[4]}")
        self.vista.etiqueta_paginas.setText(f"paginas: {self.libro[6]}")
        self.vista.etiqueta_creador.setText(f"creador: {self.libro[7]}")
        self.vista.etiqueta_etiquetas.setText(f"etiquetas: {self.libro[8] or 'ninguna'}")

    def cargar_imagen(self):
        ruta_portada = buscar_portada(self.libro[2])
        if ruta_portada:
            pixmap = QPixmap(ruta_portada)
            self.vista.etiqueta_portada.setPixmap(pixmap.scaled(175, 230, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.vista.etiqueta_portada.setText("")
        else:
            self.vista.etiqueta_portada.clear()
            self.vista.etiqueta_portada.setText("PORTADA")

    def abrir_edicion(self):
        # se usan los datos mas recientes del libro
        self.refrescar_libro()
        self.controlador_principal.abrir_anadir_libro(self.libro)
        self.vista.close()

    def refrescar_libro(self):
        # vuelve a leer el libro de la base de datos para no trabajar con
        # datos viejos (por ejemplo, copias disponibles que ya cambiaron)
        actualizado = self.modelo_libros.obtener_libro_por_id(self.libro[0])
        if actualizado:
            self.libro = actualizado
        return actualizado is not None

    def cambiar_portada(self):
        archivo, _ = QFileDialog.getOpenFileName(self.vista, "seleccionar nueva portada", "", "imagenes (*.png *.jpg *.jpeg)")
        if archivo:
            guardar_portada(archivo, self.libro[2])
            self.cargar_imagen()
            self.controlador_principal.cargar_libros_inicio()
            self.mostrar_alerta("exito", "guardada con exito")

    def borrar_portada(self):
        if borrar_portadas(self.libro[2]):
            self.cargar_imagen()
            self.controlador_principal.cargar_libros_inicio()
            self.mostrar_alerta("exito", "portada eliminada")
        else:
            self.mostrar_alerta("aviso", "no habia portada para borrar")

    def anadir_a_lista(self):
        self.refrescar_libro()
        if self.libro[5] <= 0:
            self.mostrar_alerta("aviso", "no hay copias disponibles de este libro")
            return

        exito = self.controlador_principal.anadir_al_carrito(self.libro)
        if exito:
            self.mostrar_alerta("exito", "libro anadido a la lista")
            self.vista.close()
        else:
            self.mostrar_alerta("aviso", "el libro ya esta en la lista o el carrito esta lleno (max 3)")

    def prestar_directo(self):
        self.refrescar_libro()
        if self.libro[5] <= 0:
            self.mostrar_alerta("aviso", "no hay copias disponibles de este libro")
            return

        # si el carrito esta lleno y el libro no esta en el, se avisa
        # (antes se abria el carrito sin el libro sin decir nada)
        ya_en_carrito = any(l[0] == self.libro[0] for l in self.controlador_principal.carrito_libros)
        if not ya_en_carrito and not self.controlador_principal.anadir_al_carrito(self.libro):
            self.mostrar_alerta("aviso", "el carrito esta lleno (max 3), presta o quita libros primero")
            return

        self.vista.close()
        self.controlador_principal.abrir_carrito()

    def eliminar_libro_sistema(self):
        caja = QMessageBox(self.vista)
        caja.setWindowTitle("confirmar")
        caja.setText("seguro que quieres borrar este libro por completo?")
        caja.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        caja.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #E50914;
                color: white;
                font-weight: bold;
                border-radius: 4px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #f40612;
            }
        """)
        
        if caja.exec() == int(QMessageBox.StandardButton.Yes):
            # no se puede borrar un libro con copias prestadas
            if not self.modelo_libros.eliminar_libro(self.libro[0]):
                self.mostrar_alerta(
                    "aviso",
                    "no se puede borrar: este libro tiene copias prestadas. recibelas primero"
                )
                return

            # borra la portada sin mostrar mensajes extra
            borrar_portadas(self.libro[2])

            # si estaba en el carrito se quita
            self.controlador_principal.quitar_del_carrito(self.libro[0])

            self.mostrar_alerta("exito", "libro borrado del sistema")
            self.controlador_principal.cargar_libros_inicio()
            self.vista.close()