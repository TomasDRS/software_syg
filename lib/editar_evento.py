import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QMessageBox, QTreeWidgetItem
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import QDate, QPoint, Qt
from PyQt5 import uic
from lib.sql import SQLite
from datetime import datetime
import ast

class EDIT_EVENT(QMainWindow):
    def __init__(self, user, tabla_seleccionada, evento, parent=None):
        super(EDIT_EVENT, self).__init__(parent)
        uic.loadUi("gui\gui_editar_evento.ui", self)  # Cargar la interfaz de Qt Designer

        self.user = user
        self.evento = evento
        self.tabla_seleccionada = tabla_seleccionada
        self.claseSQLite = SQLite(r"//192.168.10.5/syg/INGENIERIA/PRUEBA_SOFTWARE_MGM/db.db")
        self.setWindowTitle("Modificar Evento")
        self.button_edit.clicked.connect(self.editar_evento_user)
        self.button_cancelar.clicked.connect(self.close)
        self.check_interno.stateChanged.connect(self.check_interno_changed)
        self.combo_encargado_sector.currentIndexChanged.connect(self.mostrar_usuarios)
        
        # sectores = ast.literal_eval(self.claseSQLite.buscar_usuario(user)[4])
        # self.determinar_sectores(sectores)

        self.mostrar_evento()

        self.msg_modificado = QMessageBox()
        self.msg_modificado.setIcon(QMessageBox.Information)
        self.msg_modificado.setText("Se ha modificado el evento.")
        self.msg_modificado.setWindowTitle("Evento modificado.")

    def mostrar_evento(self):
        sectores_index = {"syg_comex": 0, "syg_gestion": 1, "syg_ingenieria": 2, "syg_laboratorio": 3, "syg_visitas_ingenieria": 4,
                          "syg_producto": 5, "mgm_academia": 6, "mgm_calidad": 7, "mgm_comercial": 8, "mgm_gestion": 9, 
                          "mgm_ingenieria": 10, "mgm_laboratorio": 11, "mgm_producto": 12, "admin_administracion": 13}
        self.combo_empresa.setCurrentText(self.evento[1])
        self.label_usuario.setText(self.evento[8])
        self.label_fecha.setText(self.evento[4])
        self.line_descripcion.setPlainText(self.evento[2])
        self.line_archivos.setText(self.evento[3])
        self.date_fecha.setDate(QDate.fromString(self.evento[9], "yyyy/MM/dd"))
        self.encargados = ast.literal_eval(self.evento[10])
        try:
            for encargado in self.encargados:
                item = QTreeWidgetItem(self.treeWidget, [encargado])
                item.setCheckState(0, Qt.Checked)
        except:
            print("[ERROR] No se pudo cargar el encargado")
        self.check_finalizado.setChecked(int(self.evento[11]))

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

    def editar_evento_user(self):
        fecha_actualizacion = datetime.now().strftime("%Y/%m/%d")
        hora_carga = datetime.now().strftime("%H:%M:%S")
        
        descripcion_nueva = self.line_descripcion.toPlainText() + "\n" + str(fecha_actualizacion) + " - " + self.user + "\n" + self.line_actualizacion.toPlainText()

        data = [self.evento[4], self.evento[1], self.line_descripcion.toPlainText(), 
                descripcion_nueva, self.evento[10], self.evento[9]]

        self.claseSQLite.modificar_evento_user(self.tabla_seleccionada, *data)

        self.msg_modificado.exec_()
        
    def check_interno_changed(self):
        if self.check_interno.isChecked():
            self.combo_empresa.setEnabled(False)
        else:
            self.combo_empresa.setEnabled(True)

