import sys
import traceback

from PyQt6.QtWidgets import (
    QApplication,
    QMessageBox
)

from controlador.login_controlador import (
    ControladorLogin
)

from database.conexion import conectar

# funcion para manejar errores
def manejador_errores(
    tipo_error,
    valor_error,
    traceback_obj
):

    # obtiene detalles del error
    mensaje = "".join(
        traceback.format_exception(
            tipo_error,
            valor_error,
            traceback_obj
        )
    )

    # crea ventana de error
    caja_error = QMessageBox()

    # titulo de ventana
    caja_error.setWindowTitle(
        "error critico en el sistema"
    )

    # mensaje principal
    caja_error.setText(
        "ocurrio un error inesperado toma captura de esto:"
    )

    # detalles completos del error
    caja_error.setDetailedText(
        mensaje
    )

    # estilos de la ventana
    caja_error.setStyleSheet("""
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

        QTextEdit {
            background-color: #141414;
            color: #ffcccc;
        }
    """)

    # muestra ventana de error
    caja_error.exec()

# punto de inicio del programa
if __name__ == "__main__":

    # activa manejador de errores
    sys.excepthook = manejador_errores

    # crea aplicacion
    aplicacion = QApplication(sys.argv)

    # crea la base de datos y tablas si no existen
    # (necesario al copiar el programa a otra computadora)
    conectar()

    # crea controlador login
    controlador = ControladorLogin()

    # muestra ventana login
    controlador.vista.show()

    # ejecuta aplicacion
    sys.exit(aplicacion.exec())