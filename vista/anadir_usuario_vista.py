from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox

class VistaAnadirUsuario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("anadir nuevo usuario")
        self.resize(300, 400)

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

        self.etiqueta_tipo = QLabel("tipo de registro")
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["escuela", "publico general"])

        self.etiqueta_identificacion = QLabel("codigo de estudiante")
        self.entrada_identificacion = QLineEdit()

        self.etiqueta_nombre = QLabel("nombre completo")
        self.entrada_nombre = QLineEdit()

        self.etiqueta_carrera = QLabel("carrera")
        self.entrada_carrera = QLineEdit()

        self.etiqueta_telefono = QLabel("telefono")
        self.entrada_telefono = QLineEdit()
        self.entrada_telefono.setMaxLength(10)

        self.boton_guardar = QPushButton("guardar usuario")

        plantilla.addWidget(self.etiqueta_tipo)
        plantilla.addWidget(self.combo_tipo)
        plantilla.addWidget(self.etiqueta_identificacion)
        plantilla.addWidget(self.entrada_identificacion)
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