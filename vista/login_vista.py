from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

# ventana de inicio de sesion
class VistaLogin(QWidget):

    # inicia la interfaz
    def __init__(self):
        super().__init__()

        # titulo de ventana
        self.setWindowTitle("acceso al sistema")

        # tamano de ventana
        self.resize(300, 250)

        # estilos generales
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
        """)

        # layout principal
        plantilla = QVBoxLayout()

        # etiqueta de usuario
        self.etiqueta_usuario = QLabel("usuario")

        # entrada de usuario
        self.entrada_usuario = QLineEdit()

        # etiqueta de contrasena
        self.etiqueta_contrasena = QLabel("contrasena")

        # entrada de contrasena
        self.entrada_contrasena = QLineEdit()

        # oculta caracteres de contrasena
        self.entrada_contrasena.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        # boton ingresar
        self.boton_ingresar = QPushButton("ingresar")

        # agrega widgets al layout
        plantilla.addWidget(self.etiqueta_usuario)
        plantilla.addWidget(self.entrada_usuario)

        plantilla.addWidget(self.etiqueta_contrasena)
        plantilla.addWidget(self.entrada_contrasena)

        plantilla.addWidget(self.boton_ingresar)

        # asigna layout a la ventana
        self.setLayout(plantilla)

    # muestra mensajes en pantalla
    def mostrar_mensaje(self, titulo, mensaje):

        # crea caja de mensaje
        caja = QMessageBox(self)

        # coloca titulo
        caja.setWindowTitle(titulo)

        # coloca mensaje
        caja.setText(mensaje)

        # estilos de la caja
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

        # muestra mensaje
        caja.exec()