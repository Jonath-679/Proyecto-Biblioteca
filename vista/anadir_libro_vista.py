from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QPushButton,
    QMessageBox
)

# ventana para anadir libros
class VistaAnadirLibro(QWidget):

    # inicia la interfaz
    def __init__(self):
        super().__init__()

        # titulo de ventana
        self.setWindowTitle("anadir nuevo libro")

        # tamano de ventana
        self.resize(350, 650)

        # estilos generales
        self.setStyleSheet("""
            QWidget {
                background-color: #141414;
                color: #ffffff;
                font-family: Arial, Helvetica, sans-serif;
            }

            QLineEdit, QComboBox, QSpinBox {
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

        # layout principal
        plantilla = QVBoxLayout()

        # etiqueta y entrada del titulo
        self.etiqueta_titulo = QLabel("titulo del libro")
        self.entrada_titulo = QLineEdit()

        # etiqueta y entrada del codigo
        self.etiqueta_codigo = QLabel("codigo")
        self.entrada_codigo = QLineEdit()

        # seleccion de ubicacion
        self.etiqueta_ubicacion = QLabel("lugar donde se colocara")
        self.combo_ubicacion = QComboBox()

        # cantidad de libros
        self.etiqueta_cantidad = QLabel("cantidad total")
        self.entrada_cantidad = QSpinBox()

        # minimo permitido
        self.entrada_cantidad.setMinimum(1)

        # numero de paginas
        self.etiqueta_paginas = QLabel("paginas")
        self.entrada_paginas = QSpinBox()

        # maximo permitido
        self.entrada_paginas.setMaximum(10000)

        # creador o autor
        self.etiqueta_creador = QLabel("creador o autor")
        self.entrada_creador = QLineEdit()

        # seccion de portada
        self.etiqueta_portada = QLabel("--- PORTADA DEL LIBRO ---")

        # fila para botones de portada
        fila_portada = QHBoxLayout()

        # boton para seleccionar imagen
        self.boton_seleccionar_portada = QPushButton("seleccionar imagen")

        # boton para quitar imagen
        self.boton_eliminar_portada = QPushButton("quitar imagen")

        # estilo del boton
        self.boton_eliminar_portada.setStyleSheet(
            "background-color: #333333;"
        )

        # agrega botones a la fila
        fila_portada.addWidget(self.boton_seleccionar_portada)
        fila_portada.addWidget(self.boton_eliminar_portada)

        # muestra nombre de imagen
        self.etiqueta_ruta_portada = QLabel(
            "ninguna imagen seleccionada"
        )

        # titulo de etiquetas
        self.etiqueta_seccion_tags = QLabel(
            "--- GESTION DE ETIQUETAS ---"
        )
        
        # fila para etiquetas existentes
        fila_existentes = QHBoxLayout()

        # combo de etiquetas
        self.combo_etiquetas = QComboBox()

        # boton para agregar etiqueta
        self.boton_anadir_existente = QPushButton("agregar")

        # estilo del boton
        self.boton_anadir_existente.setStyleSheet(
            "background-color: #333333;"
        )

        # agrega widgets a la fila
        fila_existentes.addWidget(self.combo_etiquetas)
        fila_existentes.addWidget(self.boton_anadir_existente)

        # fila para crear etiquetas
        fila_nuevas = QHBoxLayout()

        # entrada para nueva etiqueta
        self.entrada_nueva_etiqueta = QLineEdit()

        # texto de ejemplo
        self.entrada_nueva_etiqueta.setPlaceholderText("ej: #MAGIA")

        # boton para crear etiqueta
        self.boton_crear_nueva = QPushButton("crear nueva")

        # estilo del boton
        self.boton_crear_nueva.setStyleSheet(
            "background-color: #333333;"
        )

        # agrega widgets a la fila
        fila_nuevas.addWidget(self.entrada_nueva_etiqueta)
        fila_nuevas.addWidget(self.boton_crear_nueva)

        # etiquetas seleccionadas
        self.etiquetas_seleccionadas = QLabel(
            "etiquetas para este libro: ninguna"
        )

        # permite salto de linea
        self.etiquetas_seleccionadas.setWordWrap(True)

        # boton guardar
        self.boton_guardar = QPushButton(
            "guardar libro en sistema"
        )

        # agrega widgets al layout principal
        plantilla.addWidget(self.etiqueta_titulo)
        plantilla.addWidget(self.entrada_titulo)

        plantilla.addWidget(self.etiqueta_codigo)
        plantilla.addWidget(self.entrada_codigo)

        plantilla.addWidget(self.etiqueta_ubicacion)
        plantilla.addWidget(self.combo_ubicacion)

        plantilla.addWidget(self.etiqueta_cantidad)
        plantilla.addWidget(self.entrada_cantidad)

        plantilla.addWidget(self.etiqueta_paginas)
        plantilla.addWidget(self.entrada_paginas)

        plantilla.addWidget(self.etiqueta_creador)
        plantilla.addWidget(self.entrada_creador)
        
        # agrega seccion de portada
        plantilla.addWidget(self.etiqueta_portada)
        plantilla.addLayout(fila_portada)
        plantilla.addWidget(self.etiqueta_ruta_portada)

        # agrega seccion de etiquetas
        plantilla.addWidget(self.etiqueta_seccion_tags)
        plantilla.addLayout(fila_existentes)
        plantilla.addLayout(fila_nuevas)
        plantilla.addWidget(self.etiquetas_seleccionadas)

        # agrega boton guardar
        plantilla.addWidget(self.boton_guardar)

        # asigna layout a la ventana
        self.setLayout(plantilla)

    # muestra mensajes en pantalla
    def mostrar_mensaje(self, titulo, mensaje):

        # crea ventana de mensaje
        caja = QMessageBox(self)

        # titulo del mensaje
        caja.setWindowTitle(titulo)

        # texto del mensaje
        caja.setText(mensaje)

        # estilos del mensaje
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