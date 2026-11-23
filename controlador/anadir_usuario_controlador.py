from vista.anadir_usuario_vista import VistaAnadirUsuario
from modelo.modelos import ModeloLectores

class ControladorAnadirUsuario:
    def __init__(self):
        self.vista = VistaAnadirUsuario()
        self.modelo_lectores = ModeloLectores()
        
        self.vista.combo_tipo.currentIndexChanged.connect(self.cambiar_tipo_formulario)
        self.vista.boton_guardar.clicked.connect(self.guardar_usuario)

    def cambiar_tipo_formulario(self):
        tipo = self.vista.combo_tipo.currentText()
        if tipo == "escuela":
            self.vista.etiqueta_identificacion.setText("codigo de estudiante")
            self.vista.etiqueta_carrera.setText("carrera")
            self.vista.entrada_carrera.show()
            self.vista.etiqueta_carrera.show()
        else:
            self.vista.etiqueta_identificacion.setText("curp")
            self.vista.etiqueta_carrera.hide()
            self.vista.entrada_carrera.hide()
            self.vista.entrada_carrera.clear()

    def guardar_usuario(self):
        tipo = self.vista.combo_tipo.currentText()
        identificacion = self.vista.entrada_identificacion.text().strip().upper()
        nombre = self.vista.entrada_nombre.text().strip().upper()
        carrera = self.vista.entrada_carrera.text().strip().upper()
        telefono = self.vista.entrada_telefono.text().strip()

        if not identificacion or not nombre or not telefono:
            self.vista.mostrar_mensaje("error", "llena los datos principales")
            return

        if any(letra.isdigit() for letra in nombre):
            self.vista.mostrar_mensaje("error", "el nombre no puede contener numeros")
            return

        if len(telefono) != 10 or not telefono.isdigit():
            self.vista.mostrar_mensaje("error", "el telefono debe tener exactamente 10 numeros")
            return

        # evita lectores duplicados con el mismo codigo / curp
        if self.modelo_lectores.existe_identificacion(identificacion):
            self.vista.mostrar_mensaje("error", f"ya existe un usuario registrado con {identificacion}")
            return

        try:
            self.modelo_lectores.anadir_lector(tipo, identificacion, nombre, carrera, telefono)
            self.vista.mostrar_mensaje("exito", "guardado con exito")
            
            self.vista.entrada_identificacion.clear()
            self.vista.entrada_nombre.clear()
            self.vista.entrada_carrera.clear()
            self.vista.entrada_telefono.clear()
        except Exception:
            self.vista.mostrar_mensaje("error", "hubo un problema al guardar al usuario")