import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QMessageBox, QTreeWidgetItem
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import QDate, QPoint, Qt
from PyQt5 import uic
from lib.sql import SQLite
from datetime import datetime
import ast

class EDIT_EVENT(QMainWindow):
    def __init__(self, user, callback, tabla_seleccionada, evento, parent=None):
        super(EDIT_EVENT, self).__init__(parent)
        uic.loadUi("gui\gui_editar_evento.ui", self)  # Cargar la interfaz de Qt Designer

        self.user = user
        self.evento = evento
        self.callback = callback
        self.tabla_seleccionada = tabla_seleccionada
        self.flag_fecha = False
        self.flag_estado_interno = False
        self.flag_estado_admin = False
        self.claseSQLite = SQLite(r"//192.168.10.5/syg/INGENIERIA/PRUEBA_SOFTWARE_MGM/db.db")
        self.setWindowTitle("Modificar Evento")
        if self.user == "German Roldan" or self.user == "Matias Roldan":
            self.desbloquear_admin()
            self.button_edit.clicked.connect(self.editar_evento_admin)
        else:
            self.button_edit.clicked.connect(self.check_datos_user)
        self.button_cancelar.clicked.connect(self.close)
        self.check_interno.stateChanged.connect(self.check_interno_changed)
        self.combo_encargado_sector.currentIndexChanged.connect(self.mostrar_usuarios)

        self.button_check.clicked.connect(lambda: self.check_all_items())
        self.button_uncheck.clicked.connect(lambda: self.uncheck_all_items())

        self.check_finalizado_interno.clicked.connect(lambda: setattr(self, 'flag_estado_interno', True))
        self.check_finalizado.clicked.connect(lambda: setattr(self, 'flag_estado_admin', True))
        # sectores = ast.literal_eval(self.claseSQLite.buscar_usuario(user)[4])
        # self.determinar_sectores(sectores)
        self.mostrar_evento()

        self.msg_modificado = QMessageBox()
        self.msg_modificado.setIcon(QMessageBox.Information)
        self.msg_modificado.setText("Se ha modificado el evento.")
        self.msg_modificado.setWindowTitle("Evento modificado.")

        self.msg_faltan_datos = QMessageBox()
        self.msg_faltan_datos.setIcon(QMessageBox.Warning)
        self.msg_faltan_datos.setText("¡No se ha modificado ningún dato!")
        self.msg_faltan_datos.setWindowTitle("No se modificaron datos.")

    def mostrar_evento(self):
        sectores_index = {"syg_comex": 0, "syg_gestion": 1, "syg_ingenieria": 2, "syg_laboratorio": 3, "syg_visitas_ingenieria": 4,
                          "syg_calibraciones_ingenieria": 5, "syg_producto": 6, "mgm_academia": 7, "mgm_calidad": 8, 
                          "mgm_comercial": 9, "mgm_gestion": 10, "mgm_ingenieria": 11, "mgm_laboratorio": 12, "mgm_producto": 13,
                          "admin_administracion": 14}
        self.combo_empresa.setCurrentText(self.evento[1])
        self.label_usuario.setText(self.evento[8])
        self.label_fecha.setText(self.evento[4])
        self.line_descripcion.setPlainText(self.evento[2])
        self.line_descripcion_empresa.setPlainText(self.evento[7])
        # self.line_archivos.setText(self.evento[3])
        self.encargados = ast.literal_eval(self.evento[10])
        try:
            for encargado in self.encargados:
                item = QTreeWidgetItem(self.treeWidget, [encargado])
                item.setCheckState(0, Qt.Checked)
        except:
            print("[ERROR] No se pudo cargar el encargado")
        info_estado = ast.literal_eval(self.evento[11])

        lista_fechas_anteriores = ast.literal_eval(self.evento[9])
        for fecha in reversed(lista_fechas_anteriores[:-1]):
            self.combo_fechas_anteriores.addItems([fecha[1] + " - " + fecha[0]])
        
        self.date_fecha.setDate(QDate.fromString(lista_fechas_anteriores[-1][0], "yyyy/MM/dd"))
        
        self.date_fecha.dateChanged.connect(lambda: setattr(self, 'flag_fecha', True))

        self.check_finalizado_interno.setChecked(info_estado[0][0][0] == "1")
        self.check_finalizado.setChecked(info_estado[0][1][0] == "1")

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
        
        if self.line_actualizacion.toPlainText() != "":
            descripcion_nueva = self.line_descripcion.toPlainText() + "\n" + str(fecha_actualizacion) + " - " + self.user + "\n" + self.line_actualizacion.toPlainText()
        else:
            descripcion_nueva = self.line_descripcion.toPlainText()

        if self.flag_fecha:
            fechas_viejas = ast.literal_eval(self.evento[9])
            fechas_viejas.append([self.date_fecha.date().toString("yyyy/MM/dd"), self.user])
            fecha_nueva = fechas_viejas
        else:
            fecha_nueva = self.evento[9]

        if self.flag_estado_interno:
            if self.check_finalizado_interno.isChecked():
                estado_encargado = "1"
            else:
                estado_encargado = "0"
            estado_viejo = ast.literal_eval(self.evento[11])
            estado_nuevo = estado_viejo
            estado_nuevo[0][0] = estado_encargado
            estado_nuevo[0][1] = fecha_actualizacion
            estado_nuevo[0][2] = self.user
        else:
            estado_nuevo = self.evento[11]

        descripcion_empresa_nueva = self.line_descripcion_empresa.toPlainText()

        data = [str(self.evento[4]), str(self.evento[1]), str(self.line_descripcion.toPlainText()), 
            str(descripcion_nueva), str(descripcion_empresa_nueva),str(self.evento[9]),
            str(fecha_nueva), str(self.evento[10]), str(estado_nuevo)]
        
        self.claseSQLite.modificar_evento_user(self.tabla_seleccionada, *data)

        self.msg_modificado.exec_()
        
        self.callback()

    def editar_evento_admin(self):
        fecha_actualizacion = datetime.now().strftime("%Y/%m/%d")
        hora_carga = datetime.now().strftime("%H:%M:%S")

        if self.line_actualizacion.toPlainText() != "":
            descripcion_nueva = self.line_descripcion.toPlainText() + "\n" + str(fecha_actualizacion) + " - " + self.user + "\n" + self.line_actualizacion.toPlainText()
        else:
            descripcion_nueva = self.line_descripcion.toPlainText()

        if self.flag_fecha:
            fechas_viejas = ast.literal_eval(self.evento[9])
            fechas_viejas.append([self.date_fecha.date().toString("yyyy/MM/dd"), self.user])
            fecha_nueva = fechas_viejas
        else:
            fecha_nueva = self.evento[9]
        
        if self.flag_estado_interno:
            if self.check_finalizado_interno.isChecked():
                estado_encargado = "1"
            else:
                estado_encargado = "0"
            estado_viejo = ast.literal_eval(self.evento[11])
            estado_nuevo = estado_viejo
            estado_nuevo[0][0] = estado_encargado
            estado_nuevo[0][1] = fecha_actualizacion
            estado_nuevo[0][2] = self.user
        else:
            estado_nuevo = self.evento[11]

        if self.flag_estado_admin:
            if self.check_finalizado.isChecked():
                estado_admin = "1"
            else:
                estado_admin = "0"
            estado_viejo = ast.literal_eval(self.evento[11])
            estado_nuevo = estado_viejo
            estado_nuevo[1][0] = estado_admin
            estado_nuevo[1][1] = fecha_actualizacion
            estado_nuevo[1][2] = self.user
        else:
            estado_nuevo = self.evento[11]
        
        data_empresa = "Interno" if self.check_interno.isChecked() else self.combo_empresa.currentText()
        
        lista_encargados_nuevos = self.get_checked_items(self.treeWidget)

        descripcion_empresa_nueva = self.line_descripcion_empresa.toPlainText()

        data = [str(self.evento[4]), str(self.evento[1]), data_empresa, str(self.line_descripcion.toPlainText()), 
            str(descripcion_nueva), str(descripcion_empresa_nueva), str(self.evento[9]), str(fecha_nueva), str(self.evento[10]),
            str(lista_encargados_nuevos), str(self.evento[11]), str(estado_nuevo)]

        self.claseSQLite.modificar_evento_admin(self.tabla_seleccionada, *data)

        self.msg_modificado.exec_()

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

    def check_interno_changed(self):
        if self.check_interno.isChecked():
            self.combo_empresa.setEnabled(False)
        else:
            self.combo_empresa.setEnabled(True)

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

    def desbloquear_admin(self):
        widgets_to_enable = [self.combo_empresa, self.line_descripcion, self.treeWidget,
                             self.combo_encargado_sector, self.button_check, self.button_uncheck,
                             self.check_finalizado]

        for widget in widgets_to_enable:
            widget.setEnabled(True)

    def check_datos_user(self):
        if self.line_actualizacion.toPlainText() != '' or self.flag_fecha == True or self.flag_estado_interno == True:
            self.editar_evento_user()
        else:
            self.msg_faltan_datos.exec_()