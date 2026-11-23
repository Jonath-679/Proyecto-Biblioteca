from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QGridLayout,
    QScrollArea,
    QMessageBox
)

# ventana para gestionar ubicaciones
class VistaUbicaciones(QWidget):

    # inicia la interfaz
    def __init__(self):
        super().__init__()

        # titulo de ventana
        self.setWindowTitle(
            "gestionar mapa de ubicaciones"
        )

        # tamano de ventana
        self.resize(700, 600)

        # estilos generales
        self.setStyleSheet("""
            QWidget {
                background-color: #141414;
                color: #ffffff;
                font-family: Arial, Helvetica, sans-serif;
            }

            QComboBox {
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                color: white;
            }

            QPushButton {
                background-color: #333333;
                color: white;
                font-weight: bold;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #444444;
            }

            QScrollArea {
                border: none;
            }
        """)

        # layout principal
        self.plantilla = QVBoxLayout()

        # layout de controles
        self.controles = QHBoxLayout()

        # etiqueta de estante
        self.etiqueta_estante = QLabel(
            "estante actual"
        )

        # lista de estantes
        self.combo_estante = QComboBox()

        # boton para agregar separacion
        self.boton_nueva_separacion = QPushButton(
            "anadir separacion"
        )

        # boton para borrar separacion
        self.boton_eliminar_separacion = QPushButton(
            "borrar ultima separacion"
        )

        # boton para crear estante
        self.boton_nuevo_estante = QPushButton(
            "crear nuevo estante"
        )

        # boton para eliminar estante
        self.boton_eliminar_estante = QPushButton(
            "borrar estante"
        )

        # cambia color del boton eliminar
        self.boton_eliminar_estante.setStyleSheet(
            "background-color: #7a0000;"
        )

        # agrega widgets al layout
        self.controles.addWidget(
            self.etiqueta_estante
        )

        self.controles.addWidget(
            self.combo_estante
        )

        self.controles.addWidget(
            self.boton_nueva_separacion
        )

        self.controles.addWidget(
            self.boton_eliminar_separacion
        )

        self.controles.addWidget(
            self.boton_nuevo_estante
        )

        self.controles.addWidget(
            self.boton_eliminar_estante
        )

        # agrega controles al layout principal
        self.plantilla.addLayout(
            self.controles
        )

        # area con scroll
        self.area_scroll = QScrollArea()

        # permite ajustar contenido
        self.area_scroll.setWidgetResizable(True)

        # contenedor del mapa
        self.contenedor_mapa = QWidget()

        # cuadricula del mapa
        self.cuadricula_mapa = QGridLayout()

        # coloca layout en contenedor
        self.contenedor_mapa.setLayout(
            self.cuadricula_mapa
        )

        # coloca contenedor en scroll
        self.area_scroll.setWidget(
            self.contenedor_mapa
        )

        # agrega scroll al layout
        self.plantilla.addWidget(
            self.area_scroll
        )

        # coloca layout principal
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