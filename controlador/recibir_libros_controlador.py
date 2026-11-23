import os
from vista.recibir_libros_vista import VistaRecibirLibros
from modelo.modelos import ModeloLectores, ModeloPrestamos
from rutas import RUTA_SONIDO_EXITO
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
from datetime import datetime

# clase que controla la devolucion de libros
class ControladorRecibirLibros:

    # inicia vista modelos y datos
    def __init__(self, controlador_principal):
        self.vista = VistaRecibirLibros()
        self.controlador_principal = controlador_principal
        self.modelo_lectores = ModeloLectores()
        self.modelo_prestamos = ModeloPrestamos()

        # lista para guardar checkbox de libros
        self.checkboxes_libros = []

        # crea sonido de exito
        self.sonido_exito = QSoundEffect()

        # carga sonido (ruta portable) solo si el archivo existe
        if os.path.exists(RUTA_SONIDO_EXITO):
            self.sonido_exito.setSource(QUrl.fromLocalFile(RUTA_SONIDO_EXITO))

        # conecta eventos con funciones
        self.vista.boton_buscar.clicked.connect(self.buscar_usuario)
        self.vista.entrada_buscar.textChanged.connect(self.buscar_usuario)
        self.vista.combo_usuarios.currentIndexChanged.connect(self.cargar_libros_usuario)
        self.vista.boton_devolver.clicked.connect(self.procesar_devolucion)
        
        # carga usuarios al iniciar
        self.buscar_usuario()

    # busca usuarios con prestamos activos
    def buscar_usuario(self):

        # obtiene texto de busqueda
        texto = self.vista.entrada_buscar.text().upper()

        # busca usuarios
        usuarios = self.modelo_lectores.buscar_lectores_con_prestamos(texto)
        
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
            self.vista.combo_usuarios.addItem("nadie debe libros con ese dato", None)

        # desbloquea señales
        self.vista.combo_usuarios.blockSignals(False)
        
        # carga libros del usuario seleccionado
        self.cargar_libros_usuario()

    # carga libros prestados del usuario
    def cargar_libros_usuario(self):

        # elimina widgets anteriores
        for i in reversed(range(self.vista.contenedor_libros.count())): 
            widget = self.vista.contenedor_libros.itemAt(i).widget()

            if widget:
                widget.setParent(None)

        # limpia lista de checkbox
        self.checkboxes_libros.clear()

        # obtiene id del lector
        id_lector = self.vista.combo_usuarios.currentData()

        # verifica si existe lector
        if not id_lector:
            return

        # obtiene prestamos activos
        prestamos = self.modelo_prestamos.obtener_prestamos_activos(id_lector)

        # verifica si hay prestamos
        if prestamos:

            # lista de meses
            meses = [
                "enero",
                "febrero",
                "marzo",
                "abril",
                "mayo",
                "junio",
                "julio",
                "agosto",
                "septiembre",
                "octubre",
                "noviembre",
                "diciembre"
            ]

            # recorre prestamos
            for p in prestamos:

                # convierte fecha en objeto datetime
                fecha_obj = datetime.strptime(p[3], "%Y-%m-%d %H:%M:%S")

                # obtiene partes de la fecha
                dia = fecha_obj.day
                mes = meses[fecha_obj.month - 1]
                ano = fecha_obj.year
                hora = fecha_obj.strftime("%I:%M %p").lower()

                # crea texto de fecha
                texto_fecha = f"limite hasta el {dia} de {mes} de {ano}  --  {hora}"
                
                # crea checkbox del libro
                check = QCheckBox(f"{p[2]} ({texto_fecha})")

                # guarda propiedades del prestamo
                check.setProperty("id_detalle", p[0])
                check.setProperty("id_libro", p[1])
                check.setProperty("fecha_limite", p[3])

                # agrega checkbox al contenedor
                self.vista.contenedor_libros.addWidget(check)

                # guarda checkbox en lista
                self.checkboxes_libros.append(check)

        else:

            # mensaje si no hay prestamos
            self.vista.mostrar_mensaje(
                "aviso",
                "este usuario no tiene libros pendientes por devolver"
            )

    # procesa devolucion de libros
    def procesar_devolucion(self):

        # obtiene id del lector
        id_lector = self.vista.combo_usuarios.currentData()

        # verifica lector valido
        if not id_lector:
            return

        # obtiene libros seleccionados
        seleccionados = [cb for cb in self.checkboxes_libros if cb.isChecked()]

        # verifica si hay seleccionados
        if not seleccionados:
            self.vista.mostrar_mensaje(
                "aviso",
                "ponle palomita al menos a un libro para devolver"
            )
            return

        # variables de control
        total_multa = 0.0
        libros_devueltos = 0
        hubo_castigo = False

        # formato de fecha
        formato = "%Y-%m-%d %H:%M:%S"

        # obtiene fecha actual
        ahora = datetime.now()

        # recorre libros seleccionados
        for check in seleccionados:

            # obtiene datos del prestamo
            id_detalle = check.property("id_detalle")
            id_libro = check.property("id_libro")
            fecha_limite_str = check.property("fecha_limite")

            # convierte fecha limite
            limite = datetime.strptime(fecha_limite_str, formato)

            # variables de retraso
            dias_retraso = 0
            multa = 0.0
            aplicar_castigo = False

            # verifica si hay retraso
            if ahora > limite:

                # calcula diferencia
                diferencia = ahora - limite

                # obtiene dias de retraso
                dias_retraso = diferencia.days

                # suma un dia si hay segundos restantes
                if diferencia.seconds > 0:
                    dias_retraso += 1
                
                # calcula multa
                multa = dias_retraso * 20.0

                # suma multa total
                total_multa += multa
                
                # aplica castigo si supera 2 dias
                if dias_retraso > 2:
                    aplicar_castigo = True
                    hubo_castigo = True

            # registra devolucion
            self.modelo_prestamos.devolver_libro(
                id_detalle,
                id_libro,
                multa,
                dias_retraso,
                id_lector,
                aplicar_castigo
            )

            # suma libros devueltos
            libros_devueltos += 1

        # reproduce sonido
        self.sonido_exito.play()

        # crea mensaje de resumen
        mensaje = f"se devolvieron {libros_devueltos} libros con exito"

        # agrega informacion de multa
        if total_multa > 0:
            mensaje += f"\n\nATENCION multa total a pagar de ${total_multa:.2f} pesos"

        # agrega informacion de castigo
        if hubo_castigo:
            mensaje += "\n\nel usuario ha sido bloqueado por 1 semana por exceder 2 dias de retraso"

        # muestra mensaje final
        self.vista.mostrar_mensaje("resumen de devolucion", mensaje)

        # actualiza libros
        self.controlador_principal.cargar_libros_inicio()

        # cierra ventana
        self.vista.close()