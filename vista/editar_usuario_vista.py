from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox

class VistaEditarUsuario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("editar usuario")
        self.resize(300, 450)

        self.setStyleSheet("""
            QWidget {
                background-color: #141414;
                color: #ffffff;
                font-family: Arial, Helvetica, sans-serif;
            }
            QLineEdit, QComboBox {
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                color: white;
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
                font-size: 12px;
                font-weight: bold;
                color: #aaa;
            }
        """)

        plantilla = QVBoxLayout()

        self.etiqueta_buscar = QLabel("buscar usuario")
        self.entrada_buscar = QLineEdit()
        self.combo_usuarios = QComboBox()

        self.etiqueta_nombre = QLabel("nombre completo")
        self.entrada_nombre = QLineEdit()

        self.etiqueta_carrera = QLabel("carrera o curp")
        self.entrada_carrera = QLineEdit()

        self.etiqueta_telefono = QLabel("telefono")
        self.entrada_telefono = QLineEdit()
        self.entrada_telefono.setMaxLength(10)

        self.boton_guardar = QPushButton("guardar cambios")

        plantilla.addWidget(self.etiqueta_buscar)
        plantilla.addWidget(self.entrada_buscar)
        plantilla.addWidget(self.combo_usuarios)
        plantilla.addWidget(self.etiqueta_nombre)
        plantilla.addWidget(self.entrada_nombre)
        plantilla.addWidget(self.etiqueta_carrera)
        plantilla.addWidget(self.entrada_carrera)
        plantilla.addWidget(self.etiqueta_telefono)
        plantilla.addWidget(self.entrada_telefono)
        plantilla.addWidget(self.boton_guardar)

        self.setLayout(plantilla)

    def mostrar_mensaje(self, titulo, mensaje):
        caja = QMessageBox(self)
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