from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QScrollArea, QGridLayout, QLabel, QApplication
from PyQt6.QtCore import Qt

class VistaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equipo 3 Proyecto Biblioteca")
        self.showMaximized()
        
        self.setStyleSheet("""
            QWidget {
                background-color: #141414;
                color: #ffffff;
                font-family: Arial, Helvetica, sans-serif;
            }
            QLineEdit {
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
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
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                background: #141414;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #333;
                border-radius: 6px;
            }
        """)

        plantilla_principal = QVBoxLayout()

        self.etiqueta_logo = QLabel("BIBLIOTECA ADMINISTRADOR")
        self.etiqueta_logo.setStyleSheet("color: #E50914; font-size: 28px; font-weight: 900; letter-spacing: 2px;")
        self.etiqueta_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        plantilla_principal.addWidget(self.etiqueta_logo)

        plantilla_superior = QHBoxLayout()
        self.entrada_busqueda = QLineEdit()
        self.entrada_busqueda.setPlaceholderText("buscar por titulo codigo o #etiqueta...")
        self.boton_buscar = QPushButton("buscar")
        self.boton_ver_carrito = QPushButton("carrito de prestamos (0)")
        plantilla_superior.addWidget(self.entrada_busqueda)
        plantilla_superior.addWidget(self.boton_buscar)
        plantilla_superior.addWidget(self.boton_ver_carrito)

        plantilla_botones = QHBoxLayout()
        self.boton_anadir_libro = QPushButton("anadir libro")
        self.boton_anadir_usuario = QPushButton("anadir usuario")
        self.boton_editar_usuario = QPushButton("editar usuario")
        self.boton_recibir_libros = QPushButton("recibir libros")
        self.boton_ubicaciones = QPushButton("gestionar ubicaciones")
        
        estilo_admin = "background-color: #333; color: white;"
        self.boton_anadir_libro.setStyleSheet(estilo_admin)
        self.boton_anadir_usuario.setStyleSheet(estilo_admin)
        self.boton_editar_usuario.setStyleSheet(estilo_admin)
        self.boton_recibir_libros.setStyleSheet(estilo_admin)
        self.boton_ubicaciones.setStyleSheet(estilo_admin)

        plantilla_botones.addWidget(self.boton_anadir_libro)
        plantilla_botones.addWidget(self.boton_anadir_usuario)
        plantilla_botones.addWidget(self.boton_editar_usuario)
        plantilla_botones.addWidget(self.boton_recibir_libros)
        plantilla_botones.addWidget(self.boton_ubicaciones)

        self.area_scroll = QScrollArea()
        self.area_scroll.setWidgetResizable(True)
        self.contenedor_libros = QWidget()
        self.cuadricula_libros = QGridLayout()
        self.cuadricula_libros.setSpacing(20)
        self.contenedor_libros.setLayout(self.cuadricula_libros)
        self.area_scroll.setWidget(self.contenedor_libros)

        plantilla_principal.addLayout(plantilla_superior)
        plantilla_principal.addLayout(plantilla_botones)
        plantilla_principal.addWidget(self.area_scroll)

        self.setLayout(plantilla_principal)

    def closeEvent(self, event):
        QApplication.quit()