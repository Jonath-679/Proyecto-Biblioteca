from vista.ubicaciones_vista import VistaUbicaciones
from modelo.modelos import ModeloUbicaciones, ModeloLibros
from PyQt6.QtWidgets import QPushButton, QLabel, QDialog, QVBoxLayout, QComboBox, QMessageBox
from PyQt6.QtCore import Qt

class ControladorUbicaciones:
    def __init__(self):
        self.vista = VistaUbicaciones()
        self.modelo_ubicaciones = ModeloUbicaciones()
        self.modelo_libros = ModeloLibros()
        
        self.ubicaciones = []
        self.estantes = []

        self.vista.combo_estante.currentIndexChanged.connect(self.dibujar_mapa)
        self.vista.boton_nueva_separacion.clicked.connect(self.agregar_separacion)
        self.vista.boton_eliminar_separacion.clicked.connect(self.eliminar_separacion)
        self.vista.boton_nuevo_estante.clicked.connect(self.crear_estante)
        self.vista.boton_eliminar_estante.clicked.connect(self.eliminar_estante)

        self.cargar_datos()

    def cargar_datos(self, estante_mantener=None):
        if not estante_mantener:
            estante_mantener = self.vista.combo_estante.currentText()
            
        self.ubicaciones = self.modelo_ubicaciones.obtener_ubicaciones()
        estantes_set = set()
        for ubi in self.ubicaciones:
            estantes_set.add(ubi[1])
        
        self.estantes = sorted(list(estantes_set))
        
        self.vista.combo_estante.blockSignals(True)
        self.vista.combo_estante.clear()
        self.vista.combo_estante.addItems(self.estantes)
        
        if estante_mantener in self.estantes:
            self.vista.combo_estante.setCurrentText(estante_mantener)
            
        self.vista.combo_estante.blockSignals(False)
        
        if self.estantes:
            self.dibujar_mapa()
        else:
            for i in reversed(range(self.vista.cuadricula_mapa.count())): 
                widget = self.vista.cuadricula_mapa.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

    def dibujar_mapa(self):
        for i in reversed(range(self.vista.cuadricula_mapa.count())): 
            widget = self.vista.cuadricula_mapa.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        estante_actual = self.vista.combo_estante.currentText()
        if not estante_actual:
            return

        eti_lado1 = QLabel("LADO 1 (IZQUIERDO)")
        eti_lado1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        eti_lado2 = QLabel("LADO 2 (DERECHO)")
        eti_lado2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.vista.cuadricula_mapa.addWidget(eti_lado1, 0, 0)
        self.vista.cuadricula_mapa.addWidget(eti_lado2, 0, 1)

        ubis_estante = [u for u in self.ubicaciones if u[1] == estante_actual]
        
        for ubi in ubis_estante:
            lado = int(ubi[2])
            separacion = int(ubi[3])
            
            texto_boton = f"{estante_actual}{lado}-{separacion}"
            boton = QPushButton(texto_boton)
            boton.setFixedSize(150, 60)
            boton.setStyleSheet("background-color: #d0e8f2; color: black; font-weight: bold; border-radius: 5px; border: 2px solid #8ca8b3;")
            
            columna_grid = 0 if lado == 1 else 1
            self.vista.cuadricula_mapa.addWidget(boton, separacion, columna_grid)

    def agregar_separacion(self):
        estante_actual = self.vista.combo_estante.currentText()
        if not estante_actual:
            return
        
        ubis_estante = [u for u in self.ubicaciones if u[1] == estante_actual]
        separaciones = [int(u[3]) for u in ubis_estante]
        
        nueva_sep = 1
        if separaciones:
            nueva_sep = max(separaciones) + 1

        self.modelo_ubicaciones.anadir_ubicacion(estante_actual, '1', nueva_sep)
        self.modelo_ubicaciones.anadir_ubicacion(estante_actual, '2', nueva_sep)
        
        self.cargar_datos(estante_actual)

    def eliminar_separacion(self):
        estante_actual = self.vista.combo_estante.currentText()
        if not estante_actual:
            return
            
        ubis_estante = [u for u in self.ubicaciones if u[1] == estante_actual]
        if not ubis_estante:
            return
            
        separaciones = [int(u[3]) for u in ubis_estante]
        max_sep = max(separaciones)
        
        ids_viejas = self.modelo_ubicaciones.obtener_ids_separacion(estante_actual, max_sep)
        libros_afectados = self.modelo_libros.obtener_libros_por_ubicaciones(ids_viejas)
        
        if libros_afectados:
            dialogo = QDialog(self.vista)
            dialogo.setWindowTitle("libros detectados")
            dialogo.setStyleSheet(self.vista.styleSheet())
            layout = QVBoxLayout()
            layout.addWidget(QLabel(f"hay {len(libros_afectados)} libros en esta fila. a donde los movemos?"))
            
            combo = QComboBox()
            todas = self.modelo_ubicaciones.obtener_ubicaciones()
            for u in todas:
                if u[0] not in ids_viejas:
                    combo.addItem(f"Estante {u[1]} Lado {u[2]} Sep {u[3]}", u[0])
            layout.addWidget(combo)
            
            btn_mover = QPushButton("mover y borrar fila")
            btn_ignorar = QPushButton("ignorar y borrar (quedaran sin ubicacion)")
            btn_ignorar.setStyleSheet("background-color: #7a0000;")

            if combo.count() == 0:
                combo.addItem("no hay otras ubicaciones disponibles", None)
                btn_mover.setEnabled(False)
            
            def mover():
                destino = combo.currentData()
                if destino is None:
                    return
                self.modelo_libros.mover_libros_masivo(ids_viejas, destino)
                self.modelo_ubicaciones.eliminar_ultima_separacion(estante_actual)
                dialogo.accept()
                self.cargar_datos(estante_actual)
                self.vista.mostrar_mensaje("exito", "fila borrada y libros reubicados")
                
            def ignorar():
                self.modelo_libros.mover_libros_masivo(ids_viejas, None)
                self.modelo_ubicaciones.eliminar_ultima_separacion(estante_actual)
                dialogo.accept()
                self.cargar_datos(estante_actual)
                self.vista.mostrar_mensaje("exito", "fila borrada. libros quedaron sin ubicacion")
                
            btn_mover.clicked.connect(mover)
            btn_ignorar.clicked.connect(ignorar)
            layout.addWidget(btn_mover)
            layout.addWidget(btn_ignorar)
            dialogo.setLayout(layout)
            dialogo.exec()
        else:
            self.modelo_ubicaciones.eliminar_ultima_separacion(estante_actual)
            self.cargar_datos(estante_actual)

    def crear_estante(self):
        if not self.estantes:
            nuevo_nombre = "A"
        else:
            ultimo_estante = self.estantes[-1]
            # los estantes se nombran con letras A-Z
            if ultimo_estante >= "Z":
                self.vista.mostrar_mensaje("aviso", "ya se llego al estante Z, no se pueden crear mas")
                return
            nuevo_nombre = chr(ord(ultimo_estante) + 1)
        
        self.modelo_ubicaciones.anadir_ubicacion(nuevo_nombre, '1', 1)
        self.modelo_ubicaciones.anadir_ubicacion(nuevo_nombre, '2', 1)
        self.cargar_datos(nuevo_nombre)

    def eliminar_estante(self):
        estante_actual = self.vista.combo_estante.currentText()
        if not estante_actual:
            return

        # pide confirmacion (antes se borraba sin preguntar)
        libros = self.modelo_ubicaciones.contar_libros_estante(estante_actual)
        texto = f"seguro que quieres borrar el estante {estante_actual}?"
        if libros:
            texto += f"\n\n{libros} libro(s) quedaran sin ubicacion asignada"

        caja = QMessageBox(self.vista)
        caja.setWindowTitle("confirmar")
        caja.setText(texto)
        caja.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
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
        if caja.exec() != int(QMessageBox.StandardButton.Yes):
            return
            
        self.modelo_ubicaciones.eliminar_estante(estante_actual)
        self.vista.mostrar_mensaje("exito", f"se elimino el estante {estante_actual} con todos sus espacios")
        self.cargar_datos()