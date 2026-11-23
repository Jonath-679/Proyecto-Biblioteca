from vista.principal_vista import VistaPrincipal
from modelo.modelos import ModeloLibros
from rutas import buscar_portada
from controlador.anadir_libro_controlador import ControladorAnadirLibro
from controlador.anadir_usuario_controlador import ControladorAnadirUsuario
from controlador.editar_usuario_controlador import ControladorEditarUsuario
from controlador.detalles_libro_controlador import ControladorDetallesLibro
from controlador.prestar_controlador import ControladorPrestar
from controlador.recibir_libros_controlador import ControladorRecibirLibros
from controlador.ubicaciones_controlador import ControladorUbicaciones
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ControladorPrincipal:
    def __init__(self):
        self.vista = VistaPrincipal()
        self.modelo_libros = ModeloLibros()
        
        self.carrito_libros = []
        
        self.vista.boton_buscar.clicked.connect(self.realizar_busqueda)
        self.vista.entrada_busqueda.textChanged.connect(self.realizar_busqueda)
        
        self.vista.boton_anadir_libro.clicked.connect(lambda: self.abrir_anadir_libro(None))
        self.vista.boton_anadir_usuario.clicked.connect(self.abrir_anadir_usuario)
        self.vista.boton_editar_usuario.clicked.connect(self.abrir_editar_usuario)
        self.vista.boton_ver_carrito.clicked.connect(self.abrir_carrito)
        self.vista.boton_recibir_libros.clicked.connect(self.abrir_recibir_libros)
        self.vista.boton_ubicaciones.clicked.connect(self.abrir_ubicaciones)
        
        self.cargar_libros_inicio()

    def cargar_libros_inicio(self):
        libros = self.modelo_libros.obtener_todos_los_libros()
        self.mostrar_libros_en_cuadricula(libros)

    def realizar_busqueda(self):
        texto = self.vista.entrada_busqueda.text()
        if texto:
            libros = self.modelo_libros.buscar_libros(texto.upper())
        else:
            libros = self.modelo_libros.obtener_todos_los_libros()
        self.mostrar_libros_en_cuadricula(libros)

    def mostrar_libros_en_cuadricula(self, libros):
        for i in reversed(range(self.vista.cuadricula_libros.count())): 
            widget_a_borrar = self.vista.cuadricula_libros.itemAt(i).widget()
            if widget_a_borrar is not None:
                widget_a_borrar.setParent(None)

        if not libros:
            etiqueta_vacia = QLabel("no se encontraron resultados")
            etiqueta_vacia.setStyleSheet("color: #777; font-size: 18px;")
            self.vista.cuadricula_libros.addWidget(etiqueta_vacia, 0, 0)
            return

        fila = 0
        columna = 0

        for libro in libros:
            tarjeta = QWidget()
            tarjeta.setFixedSize(200, 320)
            tarjeta.setStyleSheet("""
                QWidget {
                    background-color: #2F2F2F;
                    border-radius: 8px;
                }
            """)
            plantilla_tarjeta = QVBoxLayout()
            
            portada = QLabel("PORTADA")
            portada.setAlignment(Qt.AlignmentFlag.AlignCenter)
            portada.setStyleSheet("background-color: #1a1a1a; color: #555; border-radius: 4px;")
            portada.setFixedSize(175, 230)

            ruta_portada = buscar_portada(libro[2])
            if ruta_portada:
                pixmap = QPixmap(ruta_portada)
                portada.setPixmap(pixmap.scaled(175, 230, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                portada.setText("")

            titulo = QLabel(f"{libro[1]}")
            titulo.setStyleSheet("font-weight: bold; font-size: 14px;")
            titulo.setWordWrap(True)
            
            etiquetas = QLabel(f"{libro[8]}") if libro[8] else QLabel("")
            etiquetas.setStyleSheet("color: #aaa; font-size: 10px;")
            etiquetas.setWordWrap(True)

            boton_ver = QPushButton("ver detalles")
            boton_ver.clicked.connect(lambda checked, l=libro: self.abrir_detalles(l))
            
            plantilla_tarjeta.addWidget(portada)
            plantilla_tarjeta.addWidget(titulo)
            plantilla_tarjeta.addWidget(etiquetas)
            plantilla_tarjeta.addWidget(boton_ver)
            tarjeta.setLayout(plantilla_tarjeta)
            
            self.vista.cuadricula_libros.addWidget(tarjeta, fila, columna)
            
            columna += 1
            if columna > 3:
                columna = 0
                fila += 1

    def anadir_al_carrito(self, libro):
        if len(self.carrito_libros) >= 3:
            return False
        for l in self.carrito_libros:
            if l[0] == libro[0]:
                return False
        self.carrito_libros.append(libro)
        self.vista.boton_ver_carrito.setText(f"carrito de prestamos ({len(self.carrito_libros)})")
        return True

    def vaciar_carrito(self):
        self.carrito_libros = []
        self.vista.boton_ver_carrito.setText("carrito de prestamos (0)")

    def quitar_del_carrito(self, id_libro):
        # quita un libro del carrito (por ejemplo si se borro del sistema)
        self.carrito_libros = [l for l in self.carrito_libros if l[0] != id_libro]
        self.vista.boton_ver_carrito.setText(f"carrito de prestamos ({len(self.carrito_libros)})")

    def abrir_carrito(self):
        if not self.carrito_libros:
            QMessageBox.information(self.vista, "aviso", "el carrito esta vacio anade libros primero")
            return
        self.ventana_prestar = ControladorPrestar(self.carrito_libros, self)
        self.ventana_prestar.vista.show()

    def abrir_anadir_libro(self, libro_editar=None):
        self.ventana_anadir = ControladorAnadirLibro(self, libro_editar)
        self.ventana_anadir.vista.move(100, 100)
        self.ventana_anadir.vista.show()

    def abrir_anadir_usuario(self):
        self.ventana_usuario = ControladorAnadirUsuario()
        self.ventana_usuario.vista.move(500, 100)
        self.ventana_usuario.vista.show()

    def abrir_editar_usuario(self):
        self.ventana_editar_usuario = ControladorEditarUsuario()
        self.ventana_editar_usuario.vista.move(500, 100)
        self.ventana_editar_usuario.vista.show()

    def abrir_detalles(self, libro):
        self.ventana_detalles = ControladorDetallesLibro(libro, self)
        self.ventana_detalles.vista.show()

    def abrir_recibir_libros(self):
        self.ventana_recibir = ControladorRecibirLibros(self)
        self.ventana_recibir.vista.show()

    def abrir_ubicaciones(self):
        self.ventana_ubicaciones = ControladorUbicaciones()
        self.ventana_ubicaciones.vista.show()