from vista.editar_usuario_vista import VistaEditarUsuario
from modelo.modelos import ModeloLectores

class ControladorEditarUsuario:
    def __init__(self):
        self.vista = VistaEditarUsuario()
        self.modelo_lectores = ModeloLectores()
        
        self.vista.entrada_buscar.textChanged.connect(self.buscar_usuario)
        self.vista.combo_usuarios.currentIndexChanged.connect(self.cargar_datos_usuario)
        self.vista.boton_guardar.clicked.connect(self.guardar_cambios)
        
        self.buscar_usuario()

    def buscar_usuario(self):
        texto = self.vista.entrada_buscar.text().upper()
        usuarios = self.modelo_lectores.buscar_lectores(texto)
        self.vista.combo_usuarios.blockSignals(True)
        self.vista.combo_usuarios.clear()
        for u in usuarios:
            self.vista.combo_usuarios.addItem(f"{u[3]} - {u[2]}", u)
        self.vista.combo_usuarios.blockSignals(False)
        self.cargar_datos_usuario()

    def cargar_datos_usuario(self):
        usuario = self.vista.combo_usuarios.currentData()
        if usuario:
            self.vista.entrada_nombre.setText(usuario[3] or "")
            self.vista.entrada_carrera.setText(usuario[4] or "")
            self.vista.entrada_telefono.setText(usuario[5] or "")
        else:
            self.vista.entrada_nombre.clear()
            self.vista.entrada_carrera.clear()
            self.vista.entrada_telefono.clear()

    def guardar_cambios(self):
        usuario = self.vista.combo_usuarios.currentData()
        if not usuario:
            return
            
        nombre = self.vista.entrada_nombre.text().strip().upper()
        carrera = self.vista.entrada_carrera.text().strip().upper()
        telefono = self.vista.entrada_telefono.text().strip()
        
        if not nombre or not telefono:
            self.vista.mostrar_mensaje("error", "llena los datos principales")
            return
            
        if any(letra.isdigit() for letra in nombre):
            self.vista.mostrar_mensaje("error", "el nombre no puede contener numeros")
            return
            
        if len(telefono) != 10 or not telefono.isdigit():
            self.vista.mostrar_mensaje("error", "el telefono debe tener exactamente 10 numeros")
            return
            
        try:
            self.modelo_lectores.actualizar_lector(usuario[0], nombre, carrera, telefono)
            self.vista.mostrar_mensaje("exito", "actualizado con exito")
            self.buscar_usuario()
        except Exception:
            self.vista.mostrar_mensaje("error", "hubo un problema")