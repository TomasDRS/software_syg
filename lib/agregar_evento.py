import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QMessageBox, QTreeWidgetItem
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import QDate, QPoint, Qt
from PyQt5 import uic
from lib.sql import SQLite
from datetime import datetime
import ast

class ADD_EVENT(QMainWindow):
    def __init__(self, user, callback, parent=None):
        super(ADD_EVENT, self).__init__(parent)
        uic.loadUi("gui\gui_agregar_evento.ui", self)  # Cargar la interfaz de Qt Designer

        self.callback = callback
        self.user = user
        self.claseSQLite = SQLite(r"//192.168.10.5/syg/INGENIERIA/PRUEBA_SOFTWARE_MGM/db.db")
        self.setWindowTitle("Agregar Evento")
        self.combo_empresa.setEditable(True)
        self.combo_empresa.setCurrentText("Seleccionar empresa")
        # self.button_crear.clicked.connect(self.crear_evento)
        self.button_crear.clicked.connect(self.check_datos)
        self.button_cancelar.clicked.connect(self.close)
        self.check_interno.stateChanged.connect(self.check_interno_changed)
        self.combo_encargado_sector.currentIndexChanged.connect(self.mostrar_usuarios)

        self.button_check.clicked.connect(lambda: self.check_all_items())
        self.button_uncheck.clicked.connect(lambda: self.uncheck_all_items())
        
        sectores = ast.literal_eval(self.claseSQLite.buscar_usuario(user)[4])
        self.determinar_sectores(sectores)
    
        # Establecer la fecha actual
        self.date_fecha.setDate(QDate.currentDate())

        self.msg_creado = QMessageBox()
        self.msg_creado.setIcon(QMessageBox.Information)
        self.msg_creado.setText("Se ha creado el evento.")
        self.msg_creado.setWindowTitle("Evento creado.")

        self.msg_faltan_datos = QMessageBox()
        self.msg_faltan_datos.setIcon(QMessageBox.Warning)
        self.msg_faltan_datos.setText("¡Faltan datos para crear el evento!")
        self.msg_faltan_datos.setWindowTitle("Faltan datos.")

    def determinar_sectores(self, lista_sectores):
        sectores_index = {"syg_comex": 0, "syg_gestion": 1, "syg_ingenieria": 2, "syg_laboratorio": 3, "syg_visitas_ingenieria": 4,
                        "syg_producto": 5, "mgm_academia": 6, "mgm_calidad": 7, "mgm_comercial": 8, "mgm_gestion": 9, 
                        "mgm_ingenieria": 10, "mgm_laboratorio": 11, "mgm_producto": 12, "admin_administracion": 13}

        # Desactivar todos los elementos en el combo_sector
        model = self.combo_sector.model()
        for i in range(len(sectores_index)):  
            model.item(i).setEnabled(False)

        # Activar los sectores del encargado
        for sector in lista_sectores:
            model.item(sectores_index[sector]).setEnabled(True)

        # Determinar los sectores únicos (syg, mgm)
        sectores_presentes = {sector.split('_')[0] for sector in lista_sectores}

        # Diccionario para seleccionar las empresas según el sector
        empresas_dict = {"syg": "empresas_syg",
                        "mgm": "empresas_mgm"}

        # Obtener empresas según sector
        if sectores_presentes in [{"syg"}, {"mgm"}]:  
            sector_clave = list(sectores_presentes)[0]  # Obtiene "syg" o "mgm"
            empresas = self.claseSQLite.leer_empresas(empresas_dict[sector_clave])
        elif sectores_presentes == {"syg", "mgm"}:
            empresas = (self.claseSQLite.leer_empresas("empresas_syg")
                    + [["      --------------------"]]
                    + self.claseSQLite.leer_empresas("empresas_mgm"))
        else:
            print("Sectores desconocidos")

        # Agregar empresas al combo_empresa
        for empresa in empresas:
            self.combo_empresa.addItem(empresa[0])

    def mostrar_usuarios(self):
        self.treeWidget.clear()
        id_sector = self.combo_encargado_sector.currentIndex()
        if id_sector == 0:
            usuarios = self.claseSQLite.buscar_usuario_sector("syg")
            for usuario in usuarios:
                item = QTreeWidgetItem(self.treeWidget, [usuario[0]])
                item.setCheckState(0, Qt.Checked)
        elif id_sector == 1:
            usuarios = self.claseSQLite.buscar_usuario_sector("mgm")
            for usuario in usuarios:
                item = QTreeWidgetItem(self.treeWidget, [usuario[0]])
                item.setCheckState(0, Qt.Checked)

    def get_checked_items(self, tree_widget):
        checked_items = []

        def check_item(item):
            if item.checkState(0) == 2:  # Qt.Checked (2) significa que está marcado
                checked_items.append(item.text(0))
            for i in range(item.childCount()):
                check_item(item.child(i))

        for i in range(tree_widget.topLevelItemCount()):
            check_item(tree_widget.topLevelItem(i))

        return checked_items

    def uncheck_all_items(self):
        def uncheck_item(item):
            item.setCheckState(0, Qt.Unchecked)  # Desmarcar el item
            for i in range(item.childCount()):  # Recorrer hijos si los hay
                uncheck_item(item.child(i))

        for i in range(self.treeWidget.topLevelItemCount()):
            uncheck_item(self.treeWidget.topLevelItem(i))

    def check_all_items(self):
        def check_item(item):
            item.setCheckState(0, Qt.Checked)  # Desmarcar el item
            for i in range(item.childCount()):  # Recorrer hijos si los hay
                check_item(item.child(i))

        for i in range(self.treeWidget.topLevelItemCount()):
            check_item(self.treeWidget.topLevelItem(i))

    def crear_evento(self):
        
        self.button_crear.setEnabled(False)
        
        fecha_carga = datetime.now().strftime("%Y/%m/%d")
        hora_carga = datetime.now().strftime("%H:%M:%S")

        lista_encargados = self.get_checked_items(self.treeWidget)
        lista_encargados = "[" + ", ".join(f'"{item}"' for item in lista_encargados) + "]"

        descripcion = str(fecha_carga) + " - " + str(self.user) + "\n" + self.line_descripcion.toPlainText()

        data_empresa = "Interno" if self.check_interno.isChecked() else self.combo_empresa.currentText()
        sector_table_map = {0: "events_syg_comex", 1: "events_syg_gestion", 2: "events_syg_ingenieria", 3: "events_syg_laboratorio",
                            4: "visitas_syg_ingenieria", 5: "events_syg_producto", 6: "events_mgm_academia", 7: "events_mgm_calidad",
                            8: "events_mgm_comercial", 9: "events_mgm_gestion", 10: "events_mgm_ingenieria", 11: "events_mgm_laboratorio", 
                            12: "events_mgm_producto", 13: "events_admin_administracion"}
        fecha = self.date_fecha.date().toString("yyyy/MM/dd")
        data_fecha = f"""[["{fecha}", "{self.user}"]]"""
        estado = [['0', fecha_carga, str(self.user)], ['0', fecha_carga, str(self.user)]]

        descripcion_empresa = str(fecha_carga) + " - " + str(self.user) + "\n" + self.line_descripcion_empresa.toPlainText()
        data = [data_empresa, descripcion, self.line_archivos.text(), fecha_carga, hora_carga,
                "", descripcion_empresa, self.user, data_fecha, lista_encargados, str(estado)]
        sector = self.combo_sector.currentIndex()
        if sector in sector_table_map:
            self.claseSQLite.crear_evento(sector_table_map[sector], *data)

        self.msg_creado.exec_()
        self.limpiar_datos()
        self.button_crear.setEnabled(True)
        self.callback()

    def check_interno_changed(self):
        if self.check_interno.isChecked():
            self.combo_empresa.setEnabled(False)
        else:
            self.combo_empresa.setEnabled(True)

    def check_datos(self):
        datos_completados = [0, 0, 0, 0]
        if self.combo_sector.currentIndex() != -1:
            datos_completados[0] = 1
        if self.combo_empresa.currentText() != '' or self.check_interno.isChecked():
            datos_completados[1] = 1
        if self.line_descripcion.toPlainText() != '':
            datos_completados[2] = 1
        if self.get_checked_items(self.treeWidget) != []:
            datos_completados[3] = 1
        
        if datos_completados[0] == 1 and datos_completados[1] == 1 and datos_completados[2] == 1 and datos_completados[3] == 1:
            self.crear_evento()
        else:
            self.msg_faltan_datos.exec_()

    def limpiar_datos(self):
        self.combo_sector.setCurrentIndex(-1)
        self.combo_empresa.setCurrentIndex(-1)
        self.check_interno.setChecked(False)
        self.line_descripcion_empresa.setText('')
        self.line_descripcion.setText('')
        self.line_archivos.setText('')
        self.date_fecha.setDate(QDate.currentDate())
        self.combo_encargado_sector.setCurrentIndex(-1)
        self.treeWidget.clear()