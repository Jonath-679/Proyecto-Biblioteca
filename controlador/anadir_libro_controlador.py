import os
import sqlite3
from PyQt6.QtWidgets import QFileDialog
from vista.anadir_libro_vista import VistaAnadirLibro
from modelo.modelos import ModeloLibros, ModeloUbicaciones, ModeloEtiquetas
from rutas import guardar_portada

class ControladorAnadirLibro:
    def __init__(self, controlador_padre, libro_editar=None):
        self.vista = VistaAnadirLibro()
        self.modelo_libros = ModeloLibros()
        self.modelo_ubicaciones = ModeloUbicaciones()
        self.modelo_etiquetas = ModeloEtiquetas()
        self.controlador_padre = controlador_padre
        
        self.libro_editar = libro_editar
        self.lista_etiquetas_libro = []
        self.ruta_imagen_temporal = None

        self.cargar_ubicaciones()
        self.cargar_etiquetas()
        
        if self.libro_editar:
            self.vista.setWindowTitle("editar libro")
            self.vista.boton_guardar.setText("guardar cambios")
            self.llenar_datos_edicion()
        
        self.vista.boton_seleccionar_portada.clicked.connect(self.seleccionar_portada)
        self.vista.boton_eliminar_portada.clicked.connect(self.quitar_portada)
        self.vista.boton_anadir_existente.clicked.connect(self.agregar_etiqueta_existente)
        self.vista.boton_crear_nueva.clicked.connect(self.crear_nueva_etiqueta)
        self.vista.boton_guardar.clicked.connect(self.guardar_libro)

    def llenar_datos_edicion(self):
        self.vista.entrada_titulo.setText(self.libro_editar[1])
        self.vista.entrada_codigo.setText(self.libro_editar[2])
        self.vista.entrada_codigo.setDisabled(True)
        
        index_ubi = self.vista.combo_ubicacion.findData(self.libro_editar[3]) if self.libro_editar[3] is not None else -1
        if index_ubi >= 0:
            self.vista.combo_ubicacion.setCurrentIndex(index_ubi)
        else:
            # libro sin ubicacion (se borro su estante o separacion)
            self.vista.combo_ubicacion.setCurrentIndex(self.vista.combo_ubicacion.count() - 1)
            
        self.vista.entrada_cantidad.setValue(self.libro_editar[4])
        self.vista.entrada_paginas.setValue(self.libro_editar[6])
        self.vista.entrada_creador.setText(self.libro_editar[7])
        if self.libro_editar[8]:
            self.lista_etiquetas_libro = self.libro_editar[8].split()
            self.actualizar_texto_etiquetas()

    def seleccionar_portada(self):
        archivo, _ = QFileDialog.getOpenFileName(self.vista, "seleccionar portada", "", "imagenes (*.png *.jpg *.jpeg)")
        if archivo:
            self.ruta_imagen_temporal = archivo
            nombre_archivo = os.path.basename(archivo)
            self.vista.etiqueta_ruta_portada.setText(f"imagen: {nombre_archivo}")

    def quitar_portada(self):
        self.ruta_imagen_temporal = None
        self.vista.etiqueta_ruta_portada.setText("ninguna imagen seleccionada")

    def cargar_ubicaciones(self):
        ubicaciones = self.modelo_ubicaciones.obtener_ubicaciones()
        for ubi in ubicaciones:
            id_ubi = ubi[0]
            texto_ubi = f"Estante {ubi[1]} Lado {ubi[2]} Sep {ubi[3]} ({ubi[1]}{ubi[2]}-{ubi[3]})"
            self.vista.combo_ubicacion.addItem(texto_ubi, id_ubi)
        # opcion para libros que aun no tienen lugar asignado
        self.vista.combo_ubicacion.addItem("sin ubicacion asignada", None)

    def cargar_etiquetas(self):
        etiquetas = self.modelo_etiquetas.obtener_etiquetas()
        self.vista.combo_etiquetas.clear()
        self.vista.combo_etiquetas.addItems(etiquetas)

    def actualizar_texto_etiquetas(self):
        if not self.lista_etiquetas_libro:
            self.vista.etiquetas_seleccionadas.setText("etiquetas para este libro: ninguna")
        else:
            texto = " ".join(self.lista_etiquetas_libro)
            self.vista.etiquetas_seleccionadas.setText(f"etiquetas para este libro: {texto}")

    def agregar_etiqueta_existente(self):
        etiqueta = self.vista.combo_etiquetas.currentText()
        if etiqueta and etiqueta not in self.lista_etiquetas_libro:
            self.lista_etiquetas_libro.append(etiqueta)
            self.actualizar_texto_etiquetas()

    def crear_nueva_etiqueta(self):
        nueva = self.vista.entrada_nueva_etiqueta.text().strip().upper().replace(" ", "_")
        if not nueva:
            return
        if not nueva.startswith("#"):
            nueva = "#" + nueva
            
        if nueva != "#":
            self.modelo_etiquetas.anadir_etiqueta(nueva)
            self.cargar_etiquetas()
            self.vista.entrada_nueva_etiqueta.clear()
            
            if nueva not in self.lista_etiquetas_libro:
                self.lista_etiquetas_libro.append(nueva)
                self.actualizar_texto_etiquetas()

    def guardar_libro(self):
        titulo = self.vista.entrada_titulo.text().strip().upper()
        codigo = self.vista.entrada_codigo.text().strip().upper()
        id_ubicacion = self.vista.combo_ubicacion.currentData()
        cantidad = self.vista.entrada_cantidad.value()
        paginas = self.vista.entrada_paginas.value()
        creador = self.vista.entrada_creador.text().strip().upper()
        
        etiquetas_str = " ".join(self.lista_etiquetas_libro)

        if not titulo or not codigo or not creador:
            self.vista.mostrar_mensaje("error", "llena los datos importantes")
            return

        # el codigo se usa como nombre de archivo para la portada
        caracteres_invalidos = set('/\\:*?"<>|')
        if any(c in caracteres_invalidos for c in codigo):
            self.vista.mostrar_mensaje("error", "el codigo no puede contener caracteres especiales como / \\ : * ? \" < > |")
            return

        try:
            if self.libro_editar:
                self.modelo_libros.actualizar_libro(self.libro_editar[0], titulo, codigo, id_ubicacion, cantidad, paginas, creador, etiquetas_str)
            else:
                self.modelo_libros.anadir_libro(titulo, codigo, id_ubicacion, cantidad, paginas, creador, etiquetas_str)
            
            if self.ruta_imagen_temporal:
                # guarda la portada con el codigo del libro como nombre
                guardar_portada(self.ruta_imagen_temporal, codigo)

            self.vista.mostrar_mensaje("exito", "guardado con exito")
            self.controlador_padre.cargar_libros_inicio()
            
            if not self.libro_editar:
                self.vista.entrada_titulo.clear()
                self.vista.entrada_codigo.clear()
                self.vista.entrada_cantidad.setValue(1)
                self.vista.entrada_paginas.setValue(0)
                self.vista.entrada_creador.clear()
                self.lista_etiquetas_libro.clear()
                self.actualizar_texto_etiquetas()
                self.quitar_portada()
            else:
                self.vista.close()

        # el codigo del libro ya existe (columna UNIQUE)
        except sqlite3.IntegrityError:
            self.vista.mostrar_mensaje("error", f"ya existe un libro con el codigo {codigo}")

        # cantidad total menor que las copias prestadas
        except ValueError as e:
            self.vista.mostrar_mensaje("error", str(e))

        except Exception:
            self.vista.mostrar_mensaje("error", "hubo un problema al guardar")