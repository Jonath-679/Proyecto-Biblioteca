from vista.login_vista import VistaLogin
from modelo.modelos import ModeloLogin
from controlador.principal_controlador import ControladorPrincipal

# clase que controla el inicio de sesion
class ControladorLogin:

    # inicia vista y modelo
    def __init__(self):
        self.vista = VistaLogin()
        self.modelo = ModeloLogin()
        
        # conecta boton con funcion
        self.vista.boton_ingresar.clicked.connect(self.verificar_ingreso)

        # permite ingresar presionando enter
        self.vista.entrada_usuario.returnPressed.connect(self.verificar_ingreso)
        self.vista.entrada_contrasena.returnPressed.connect(self.verificar_ingreso)

        # variable para el controlador principal
        self.controlador_principal = None

    # verifica los datos de ingreso
    def verificar_ingreso(self):

        # obtiene usuario y contrasena
        usuario = self.vista.entrada_usuario.text().strip()
        contrasena = self.vista.entrada_contrasena.text()

        # verifica que no haya campos vacios
        if not usuario or not contrasena:
            self.vista.mostrar_mensaje("error", "llena todos los campos")
            return

        # revisa si el usuario existe
        usuario_valido = self.modelo.verificar_usuario(usuario, contrasena)

        # verifica si el acceso es correcto
        if usuario_valido:

            # cierra ventana de login
            self.vista.close()

            # abre ventana principal
            self.controlador_principal = ControladorPrincipal()
            self.controlador_principal.vista.show()

        else:

            # muestra mensaje de error
            self.vista.mostrar_mensaje("error", "usuario o contrasena incorrectos")