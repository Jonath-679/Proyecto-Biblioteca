import os
from vista.prestar_vista import VistaPrestar
from modelo.modelos import ModeloLectores, ModeloPrestamos
from rutas import RUTA_SONIDO_EXITO
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSpinBox, QWidget, QPushButton
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl

# clase que controla la ventana de prestamos
class ControladorPrestar:

    # inicia vista modelos y datos
    def __init__(self, libros_a_prestar, controlador_principal):
        self.vista = VistaPrestar()
        self.libros_a_prestar = libros_a_prestar
        self.controlador_principal = controlador_principal
        self.modelo_lectores = ModeloLectores()
        self.modelo_prestamos = ModeloPrestamos()

        # lista para guardar spinbox de dias
        self.spinboxes_dias = []

        # crea sonido de exito
        self.sonido_exito = QSoundEffect()

        # carga sonido (ruta portable) solo si el archivo existe
        if os.path.exists(RUTA_SONIDO_EXITO):
            self.sonido_exito.setSource(QUrl.fromLocalFile(RUTA_SONIDO_EXITO))

        # conecta botones y eventos
        self.vista.boton_buscar.clicked.connect(self.buscar_usuario)
        self.vista.entrada_buscar.textChanged.connect(self.buscar_usuario)
        self.vista.boton_confirmar.clicked.connect(self.confirmar_prestamo)
        self.vista.boton_vaciar.clicked.connect(self.vaciar_carrito)

        # carga libros y usuarios
        self.cargar_libros_ui()
        self.buscar_usuario()

    # carga libros en la interfaz
    def cargar_libros_ui(self):

        # recorre libros seleccionados
        for libro in self.libros_a_prestar:

            # contenedor de la fila (permite quitarla despues)
            contenedor_fila = QWidget()

            # crea fila horizontal
            fila = QHBoxLayout(contenedor_fila)
            fila.setContentsMargins(0, 0, 0, 0)

            # crea etiqueta con nombre del libro
            etiqueta = QLabel(f"{libro[1]}")

            # crea selector de dias
            spinbox = QSpinBox()

            # configura valores del selector
            spinbox.setMinimum(1)
            spinbox.setMaximum(30)
            spinbox.setPrefix("dias: ")

            # guarda id del libro
            spinbox.setProperty("id_libro", libro[0])

            # boton para quitar este libro del carrito
            boton_quitar = QPushButton("quitar")
            boton_quitar.setStyleSheet("background-color: #333333;")
            boton_quitar.clicked.connect(
                lambda checked, id_l=libro[0], c=contenedor_fila, s=spinbox: self.quitar_libro(id_l, c, s)
            )

            # agrega elementos a la fila
            fila.addWidget(etiqueta)
            fila.addWidget(spinbox)
            fila.addWidget(boton_quitar)

            # agrega fila al contenedor
            self.vista.contenedor_libros.addWidget(contenedor_fila)

            # guarda spinbox en la lista
            self.spinboxes_dias.append(spinbox)

    # quita un libro del carrito desde esta ventana
    def quitar_libro(self, id_libro, contenedor_fila, spinbox):
        self.controlador_principal.quitar_del_carrito(id_libro)
        if spinbox in self.spinboxes_dias:
            self.spinboxes_dias.remove(spinbox)
        contenedor_fila.setParent(None)

        # si ya no quedan libros se cierra la ventana
        if not self.spinboxes_dias:
            self.vista.close()

    # vacia el carrito completo y cierra la ventana
    def vaciar_carrito(self):
        self.controlador_principal.vaciar_carrito()
        self.vista.close()

    # busca usuarios en la base de datos
    def buscar_usuario(self):

        # obtiene texto de busqueda
        texto = self.vista.entrada_buscar.text().upper()

        # busca usuarios
        usuarios = self.modelo_lectores.buscar_lectores(texto)
        
        # bloquea señales del combo
        self.vista.combo_usuarios.blockSignals(True)

        # limpia combo
        self.vista.combo_usuarios.clear()

        # verifica si encontro usuarios
        if usuarios:

            # agrega usuarios encontrados
            for u in usuarios:
                self.vista.combo_usuarios.addItem(f"{u[3]} - {u[2]}", u[0])

        else:

            # mensaje si no hay usuarios
            self.vista.combo_usuarios.addItem("no se encontraron usuarios", None)

        # desbloquea señales
        self.vista.combo_usuarios.blockSignals(False)

    # confirma el prestamo de libros
    def confirmar_prestamo(self):

        # obtiene id del lector
        id_lector = self.vista.combo_usuarios.currentData()

        # verifica usuario valido
        if not id_lector:
            self.vista.mostrar_mensaje("error", "selecciona un usuario valido primero")
            return

        # verifica que el usuario no este castigado
        # (el castigo se guardaba al devolver con retraso pero nunca se revisaba)
        castigo = self.modelo_lectores.obtener_castigo(id_lector)
        if castigo:
            self.vista.mostrar_mensaje(
                "usuario bloqueado",
                f"este usuario esta castigado hasta el {castigo} por entregar con retraso, no puede pedir libros"
            )
            return

        # lista para guardar prestamos
        lista_prestamo = []

        # recorre spinbox de dias
        for spin in self.spinboxes_dias:

            # obtiene id del libro
            id_libro = spin.property("id_libro")

            # obtiene dias seleccionados
            dias = spin.value()

            # agrega datos a la lista
            lista_prestamo.append((id_libro, dias))

        try:

            # registra prestamo en la base de datos
            self.modelo_prestamos.registrar_prestamo(id_lector, lista_prestamo)

        # error de validacion (sin copias, libro borrado, etc.)
        except ValueError as e:
            self.vista.mostrar_mensaje("error", f"no se pudo registrar el prestamo: {e}")
            return

        # muestra error si algo falla
        except Exception:
            self.vista.mostrar_mensaje("error", "hubo un error al registrar el prestamo")
            return

        # reproduce sonido de exito
        self.sonido_exito.play()

        # muestra mensaje
        self.vista.mostrar_mensaje("exito", "prestamo registrado el tiempo comenzo a correr")

        # limpia carrito
        self.controlador_principal.vaciar_carrito()

        # actualiza libros
        self.controlador_principal.cargar_libros_inicio()

        # cierra ventana
        self.vista.close()