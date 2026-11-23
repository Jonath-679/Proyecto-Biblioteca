from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox
)

# ventana para recibir libros
class VistaRecibirLibros(QWidget):

    # inicia la interfaz
    def __init__(self):
        super().__init__()

        # titulo de ventana
        self.setWindowTitle(
            "recibir libros prestados"
        )

        # tamano de ventana
        self.resize(400, 500)

        # estilos generales
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
                font-size: 14px;
            }

            QCheckBox {
                font-size: 14px;
                padding: 5px;
            }
        """)

        # layout principal
        self.plantilla = QVBoxLayout()

        # etiqueta de busqueda
        self.etiqueta_buscar = QLabel(
            "buscar usuario (nombre curp o tel)"
        )

        # entrada de busqueda
        self.entrada_buscar = QLineEdit()

        # boton buscar
        self.boton_buscar = QPushButton(
            "buscar usuario"
        )

        # cambia color del boton
        self.boton_buscar.setStyleSheet(
            "background-color: #333333;"
        )

        # lista de usuarios
        self.combo_usuarios = QComboBox()

        # agrega widgets al layout
        self.plantilla.addWidget(
            self.etiqueta_buscar
        )

        self.plantilla.addWidget(
            self.entrada_buscar
        )

        self.plantilla.addWidget(
            self.boton_buscar
        )

        self.plantilla.addWidget(
            self.combo_usuarios
        )

        # etiqueta de libros prestados
        self.etiqueta_libros = QLabel(
            "libros que tiene prestados (marca para devolver):"
        )

        # estilo de etiqueta
        self.etiqueta_libros.setStyleSheet(
            "color: #aaa; margin-top: 15px;"
        )

        # agrega etiqueta
        self.plantilla.addWidget(
            self.etiqueta_libros
        )

        # contenedor de libros
        self.contenedor_libros = QVBoxLayout()

        # agrega contenedor
        self.plantilla.addLayout(
            self.contenedor_libros
        )

        # boton devolver libros
        self.boton_devolver = QPushButton(
            "confirmar devolucion seleccionada"
        )

        # agrega boton
        self.plantilla.addWidget(
            self.boton_devolver
        )

        # coloca layout en ventana
        self.setLayout(self.plantilla)

    # muestra mensajes emergentes
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