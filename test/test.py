import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QMessageBox, QTreeWidgetItem
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import QDate, QPoint, Qt
from PyQt5 import uic
from lib.sql import SQLite
from datetime import datetime
import ast

class ADD_EVENT(QMainWindow):
    def __init__(self, user, boton_index, parent=None):
        super(ADD_EVENT, self).__init__(parent)
        uic.loadUi("gui\gui_agregar_evento.ui", self)  # Cargar la interfaz de Qt Designer

        self.user = user
        self.claseSQLite = SQLite(r"C:\Users\Tomás\Desktop\software_mgm\db.db")
        self.setWindowTitle("Agregar Evento")
        self.combo_empresa.setEditable(True)
        self.combo_empresa.setCurrentText("Seleccionar empresa")
        self.button_crear.clicked.connect(self.crear_evento)
        self.button_cancelar.clicked.connect(self.close)
        self.check_interno.stateChanged.connect(self.check_interno_changed)
        self.combo_encargado_sector.currentIndexChanged.connect(self.mostrar_usuarios)
        
        sectores = ast.literal_eval(self.claseSQLite.buscar_usuario(user)[4])
        self.determinar_sectores(sectores)

        self.combo_sector.setCurrentIndex(boton_index)

        self.msg_creado = QMessageBox()
        self.msg_creado.setIcon(QMessageBox.Information)
        self.msg_creado.setText("Se ha creado el evento.")
        self.msg_creado.setWindowTitle("Evento creado.")

    def determinar_sectores(self, lista_sectores):
        sectores_index = {
            "syg_comex": 0, "syg_gestion": 1, "syg_ingenieria": 2, "syg_laboratorio": 3, "syg_producto": 4,
            "mgm_academia": 5, "mgm_calidad": 6, "mgm_comercial": 7, "mgm_gestion": 8, "mgm_ingenieria": 9,
            "mgm_laboratorio": 10, "mgm_producto": 11, "admin_administracion": 12
        }

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
        if id_sector == 1:
            usuarios = self.claseSQLite.buscar_usuario_sector("syg")
            for usuario in usuarios:
                item = QTreeWidgetItem(self.treeWidget, [usuario[0]])
                item.setCheckState(0, Qt.Checked)
        elif id_sector == 2:
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

    def crear_evento(self):
        fecha_carga = datetime.now().strftime("%Y/%m/%d")
        hora_carga = datetime.now().strftime("%H:%M:%S")
        
        lista_encargados = self.get_checked_items(self.treeWidget)
        lista_encargados = "[" + ", ".join(f'"{item}"' for item in lista_encargados) + "]"

        data_empresa = "Interno" if self.check_interno.isChecked() else self.combo_empresa.currentText()
        sector_table_map = {0: "events_syg_comex", 1: "events_syg_gestion", 2: "events_syg_ingenieria", 3: "events_syg_laboratorio",
                            4: "events_syg_producto", 5: "events_mgm_academia", 6: "events_mgm_calidad", 7: "events_mgm_comercial", 
                            8: "events_mgm_gestion", 9: "events_mgm_ingenieria", 10: "events_mgm_laboratorio", 11: "events_mgm_producto", 
                            12: "events_admin_administracion"}

        data = [data_empresa, self.line_descripcion.toPlainText(), self.line_archivos.text(), 
                fecha_carga, hora_carga, "", "", self.user,
                self.date_fecha.date().toString("yyyy/MM/dd"), lista_encargados, 0]
        
        sector = self.combo_sector.currentIndex()
        if sector in sector_table_map:
            self.claseSQLite.crear_evento(sector_table_map[sector], *data)

        self.msg_creado.exec_()
        
    def check_interno_changed(self):
        if self.check_interno.isChecked():
            self.combo_empresa.setEnabled(False)
        else:
            self.combo_empresa.setEnabled(True)


# Iniciar aplicación PyQt
app = QApplication(sys.argv)

main = ADD_EVENT("Nicolas Errigo", 0)
main.show()

sys.exit(app.exec())
