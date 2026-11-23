from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class VistaDetallesLibro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("detalles del libro")
        self.resize(350, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #141414;
                color: #ffffff;
                font-family: Arial, Helvetica, sans-serif;
            }
            QPushButton {
                background-color: #E50914;
                color: white;
                font-weight: bold;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f40612;
            }
            QLabel {
                font-size: 14px;
                color: #ddd;
            }
        """)

        plantilla = QVBoxLayout()

        self.etiqueta_portada = QLabel("PORTADA")
        self.etiqueta_portada.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.etiqueta_portada.setStyleSheet("background-color: #1a1a1a; color: #555; border-radius: 4px;")
        self.etiqueta_portada.setFixedSize(175, 230)

        fila_botones_portada = QHBoxLayout()
        self.boton_cambiar_portada = QPushButton("cambiar portada")
        self.boton_cambiar_portada.setStyleSheet("background-color: #333333;")
        self.boton_borrar_portada = QPushButton("borrar portada")
        self.boton_borrar_portada.setStyleSheet("background-color: #333333;")
        fila_botones_portada.addWidget(self.boton_cambiar_portada)
        fila_botones_portada.addWidget(self.boton_borrar_portada)

        self.etiqueta_titulo = QLabel()
        self.etiqueta_titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        self.etiqueta_codigo = QLabel()
        self.etiqueta_ubicacion = QLabel()
        self.etiqueta_disponible = QLabel()
        self.etiqueta_paginas = QLabel()
        self.etiqueta_creador = QLabel()
        self.etiqueta_etiquetas = QLabel()
        
        self.boton_editar = QPushButton("editar datos / cambiar lugar")
        self.boton_anadir_carrito = QPushButton("anadir a lista de prestamo")
        self.boton_prestar = QPushButton("prestar a usuario")
        self.boton_eliminar = QPushButton("eliminar libro del sistema")
        self.boton_eliminar.setStyleSheet("background-color: #7a0000;")

        plantilla.addWidget(self.etiqueta_portada, alignment=Qt.AlignmentFlag.AlignCenter)
        plantilla.addLayout(fila_botones_portada)
        plantilla.addWidget(self.etiqueta_titulo)
        plantilla.addWidget(self.etiqueta_codigo)
        plantilla.addWidget(self.etiqueta_creador)
        plantilla.addWidget(self.etiqueta_ubicacion)
        plantilla.addWidget(self.etiqueta_disponible)
        plantilla.addWidget(self.etiqueta_paginas)
        plantilla.addWidget(self.etiqueta_etiquetas)
        plantilla.addWidget(self.boton_editar)
        plantilla.addWidget(self.boton_anadir_carrito)
        plantilla.addWidget(self.boton_prestar)
        plantilla.addWidget(self.boton_eliminar)

        self.setLayout(plantilla)