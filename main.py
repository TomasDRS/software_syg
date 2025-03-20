import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QMessageBox, QHeaderView
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import QDate, QPoint, Qt, QTimer
from PyQt5 import QtWidgets
from PyQt5 import uic
from lib.sql import SQLite
from lib.agregar_evento import ADD_EVENT
from lib.editar_evento import EDIT_EVENT
from lib.agregar_empresa import ADD_COMPANY
from datetime import datetime, date
import ast

class UI(QMainWindow):
    def __init__(self, user, parent=None):
        super(UI, self).__init__(parent)
        uic.loadUi(r"gui\gui.ui", self)  # Cargar la interfaz de Qt Designer
        
        self.user = user
        self.claseSQLite = SQLite(r"//192.168.10.5/syg/INGENIERIA/PRUEBA_SOFTWARE_MGM/db.db")
        self.ventana_agregar_evento = ADD_EVENT(user)
        # self.ventana_agregar_empresa = ADD_COMPANY()

        self.msg_login = QMessageBox()
        self.msg_login.setIcon(QMessageBox.Information)
        self.msg_login.setText("Se ha iniciado sesión como " + user + ".")
        self.msg_login.setWindowTitle("Sesion iniciada.")
        self.msg_login.exec_()

        # VERSION DEL PROGRAMA
        self.action_version.setText("Versión 1.1.2 test build")

        botones_agregar = [self.boton_agregar_syg_comex, self.boton_agregar_syg_gestion, self.boton_agregar_syg_ingenieria,
                            self.boton_agregar_syg_laboratorio, self.boton_agregar_syg_visitas_ingenieria, self.boton_agregar_syg_producto, 
                            self.boton_agregar_mgm_academia, self.boton_agregar_mgm_calidad, self.boton_agregar_mgm_comercial, 
                            self.boton_agregar_mgm_gestion, self.boton_agregar_mgm_ingenieria, self.boton_agregar_mgm_laboratorio, 
                            self.boton_agregar_mgm_producto]
        
        botones_eliminar = [self.boton_eliminar_syg_comex, self.boton_eliminar_syg_gestion, self.boton_eliminar_syg_ingenieria,
                            self.boton_eliminar_syg_laboratorio, self.boton_eliminar_syg_visitas_ingenieria, self.boton_eliminar_syg_producto, 
                            self.boton_eliminar_mgm_academia, self.boton_eliminar_mgm_calidad, self.boton_eliminar_mgm_comercial, 
                            self.boton_eliminar_mgm_gestion, self.boton_eliminar_mgm_ingenieria, self.boton_eliminar_mgm_laboratorio, 
                            self.boton_eliminar_mgm_producto]
        
        botones_refresh = [self.boton_refrescar_syg_comex, self.boton_refrescar_syg_gestion, self.boton_refrescar_syg_ingenieria,
                            self.boton_refrescar_syg_laboratorio, self.boton_refrescar_syg_visitas_ingenieria, self.boton_refrescar_syg_producto, 
                            self.boton_refrescar_mgm_academia, self.boton_refrescar_mgm_calidad, self.boton_refrescar_mgm_comercial, 
                            self.boton_refrescar_mgm_gestion, self.boton_refrescar_mgm_ingenieria, self.boton_refrescar_mgm_laboratorio, 
                            self.boton_refrescar_mgm_producto]
        
        lines_buscar = [self.line_buscar_tabla_syg_comex, self.line_buscar_tabla_syg_gestion, self.line_buscar_tabla_syg_ingenieria,
                        self.line_buscar_tabla_syg_laboratorio, self.line_buscar_tabla_syg_visitas_ingenieria, self.line_buscar_tabla_syg_producto, 
                        self.line_buscar_tabla_mgm_academia, self.line_buscar_tabla_mgm_calidad, self.line_buscar_tabla_mgm_comercial, 
                        self.line_buscar_tabla_mgm_gestion, self.line_buscar_tabla_mgm_ingenieria, self.line_buscar_tabla_mgm_laboratorio, 
                        self.line_buscar_tabla_mgm_producto]

        for boton in botones_agregar:
            boton.clicked.connect(self.ventana_agregar_evento.show)

        for boton in botones_refresh:
            boton.clicked.connect(self.refrescar_tabla)

        for line in lines_buscar:
            line.textChanged.connect(lambda _, l=line: self.buscar_evento(l))

        self.refrescar_tabla()
        self.calendarWidget.clicked.connect(self.mostrar_eventos_lista)
        self.calendarWidget.clicked.connect(lambda: self.mostrar_eventos_calendario(self.tabla_user))

        tablas_eventos = [self.tabla_eventos_syg_comex, self.tabla_eventos_syg_gestion, self.tabla_eventos_syg_ingenieria,
                        self.tabla_eventos_syg_laboratorio, self.tabla_visitas_syg_ingenieria, self.tabla_eventos_syg_producto, 
                        self.tabla_eventos_mgm_academia, self.tabla_eventos_mgm_calidad, self.tabla_eventos_mgm_comercial, 
                        self.tabla_eventos_mgm_gestion, self.tabla_eventos_mgm_ingenieria, self.tabla_eventos_mgm_laboratorio, 
                        self.tabla_eventos_mgm_producto]

        for tabla in tablas_eventos:
            tabla.doubleClicked.connect(lambda _, t=tabla: self.llamar_editar_evento(t))

        self.desbloquear_tabs()
        # self.action_agregar_empresa.triggered.connect(self.ventana_agregar_empresa.show)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refrescar_tabla)
        self.timer.start(60000)  # refresca las tablas cada 15 segundos

    def desbloquear_tabs(self):
        sectores = ast.literal_eval(self.claseSQLite.buscar_usuario(self.user)[4])
        """Desbloquea las tabs según los sectores del usuario."""
        [self.tabWidget.setTabEnabled(i, False) for i in range(6, -1, -1)]
        [self.tabWidget_2.setTabEnabled(i, False) for i in range(1, -1, -1)]
        [self.tabWidget_3.setTabEnabled(i, False) for i in range(7, -1, -1)]
        # Diccionario que mapea los sectores a los índices de las pestañas
        sectores_map = {"mgm_producto": (1, 6), "mgm_laboratorio": (1, 5), "mgm_ingenieria": (1, 4),
                        "mgm_gestion": (1, 3), "mgm_comercial": (1, 2), "mgm_calidad": (1, 1),
                        "mgm_academia": (1, 0), "syg_producto": (0, 5), "syg_visitas_ingenieria": (0,4),
                        "syg_laboratorio": (0, 3), "syg_ingenieria": (0, 2), "syg_gestion": (0, 1),
                        "syg_comex": (0, 0),}

        # Iterar sobre los sectores y aplicar las configuraciones
        for sector in sectores:
            if sector in sectores_map:
                tab_2_index, tab_3_or_tab_index = sectores_map[sector]
                self.tabWidget_2.setTabEnabled(tab_2_index, True)
                
                # Determinar qué tabWidget usar
                if sector.startswith("mgm"):
                    self.tabWidget_3.setTabEnabled(tab_3_or_tab_index, True)
                else:
                    self.tabWidget.setTabEnabled(tab_3_or_tab_index, True)

    def mostrar_eventos_calendario(self, tabla):
        self.eventos_formateados = {}
        self.eventos = self.claseSQLite.leer_eventos(tabla) 
        # Personalizar el calendarWidget ya existente
        for evento in self.eventos:
            fecha = QDate(*list(map(int, evento[7].split("/"))))
            titulo = evento[1]
            descripcion = evento[2]
            prioridad = evento[10]
            estado = evento[11]
            # Si ya tiene un evento, agregar otro
            if fecha in self.eventos_formateados:
                self.eventos_formateados[fecha].append([titulo, prioridad, estado])
            else:
                # O si quieres agregar un nuevo evento a una fecha que no está en el diccionario, simplemente lo asignas
                self.eventos_formateados[fecha] = [[titulo, prioridad, estado]]
                
        self.calendarWidget.paintCell = self.paintCell  # Sobrescribir el método paintCell
        # Refrescar el calendario para aplicar cambios
        self.calendarWidget.updateCells()

    def paintCell(self, painter, rect, date):
        """Dibuja círculos en los días con eventos."""
        # Llamar al método original de QCalendarWidget para pintar la celda
        QCalendarWidget.paintCell(self.calendarWidget, painter, rect, date)

        if date in self.eventos_formateados:
            prioridades = [0] * 5
            nro_eventos = 0
            for evento in self.eventos_formateados[date]:
                if 1 <= int(evento[1]) <= 5:
                    prioridades[int(evento[1]) - 1] += 1
            colors = [Qt.red, QColor(255, 120, 0),  Qt.yellow, Qt.blue, Qt.green]
            positions = [11, 27, 43, 59, 75]
            for i in range(5):
                if prioridades[i] > 0:
                    painter.setPen(Qt.black)
                    painter.setBrush(QColor(colors[i]))
                    painter.drawEllipse(rect.topLeft() + QPoint(positions[nro_eventos], 11), 9, 9)
                    if colors[i] == Qt.blue:
                        painter.setPen(Qt.white)
                    painter.setFont(QFont("Arial", 10, QFont.Bold))
                    painter.drawText(rect.topLeft() + QPoint(positions[nro_eventos] - 3, 16), str(prioridades[i]))
                    nro_eventos += 1

    def mostrar_eventos_lista(self, date):
        """Muestra los eventos del día seleccionado."""
        fecha_seleccionada = self.calendarWidget.selectedDate().toString("yyyy/MM/dd")
        self.label_fecha_seleccionada.setText(fecha_seleccionada)
        self.lista_eventos.clear()
        for event in self.claseSQLite.buscar_evento(self.tabla_user, fecha_seleccionada):
            self.lista_eventos.addItem(f"{event[1]} - {event[2]}")
        self.calendarWidget.paintCell = self.paintCell  # Sobrescribir el método paintCell
        # Refrescar el calendario para aplicar cambios
        self.calendarWidget.updateCells()

    def refrescar_tabla(self):
        sectores = ast.literal_eval(self.claseSQLite.buscar_usuario(self.user)[4])
        tablas_por_sectores = {'syg_comex': ["events_syg_comex", self.tabla_eventos_syg_comex], 
                            'syg_gestion': ["events_syg_gestion", self.tabla_eventos_syg_gestion], 
                            'syg_ingenieria': ["events_syg_ingenieria", self.tabla_eventos_syg_ingenieria], 
                            'syg_laboratorio': ["events_syg_laboratorio", self.tabla_eventos_syg_laboratorio],
                            'syg_visitas_ingenieria': ["visitas_syg_ingenieria", self.tabla_visitas_syg_ingenieria],
                            'syg_producto': ["events_syg_producto", self.tabla_eventos_syg_producto], 
                            'mgm_academia': ["events_mgm_academia", self.tabla_eventos_mgm_academia], 
                            'mgm_calidad': ["events_mgm_calidad", self.tabla_eventos_mgm_calidad], 
                            'mgm_comercial': ["events_mgm_comercial", self.tabla_eventos_mgm_comercial], 
                            'mgm_gestion': ["events_mgm_gestion", self.tabla_eventos_mgm_gestion], 
                            'mgm_ingenieria': ["events_mgm_ingenieria", self.tabla_eventos_mgm_ingenieria],
                            'mgm_laboratorio': ["events_mgm_laboratorio", self.tabla_eventos_mgm_laboratorio], 
                            'mgm_producto': ["events_mgm_producto", self.tabla_eventos_mgm_producto]}

        for sector in sectores:
            data = tablas_por_sectores[sector]
            tabla_widget = data[1]
            
            # Save the selected row
            selected_row = tabla_widget.currentRow() 
            
            self.mostrar_eventos_tabla(*data)
            
            # Re-select the previously selected row
            if selected_row >= 0 and selected_row < tabla_widget.rowCount():
                tabla_widget.selectRow(selected_row)
        print("[INFO] Tablas refrescadas.")

    def mostrar_eventos_tabla(self, tabla_db, tabla_widget):
        """Muestra los eventos en la tabla."""

        self.eventos = self.claseSQLite.leer_eventos(tabla_db)
        # self.eventos.sort(key=lambda x: (x[7], x[10]))
        tabla_widget.clear()

        tabla_widget.horizontalHeader().setVisible(True)
        tabla_widget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        tabla_widget.setRowCount(len(self.eventos))
        tabla_widget.setColumnCount(9)
        
        column_width = [30, 100, 100, 200, 500, 180, 120, 120, 120]
        headers = ["id", "Fecha Carga", "Empresa", "Empresa", "Descripción", "Encargado/s", "Fecha Límite", "Terminado", "Finalizado"]
        for i, header in enumerate(headers):
            tabla_widget.setColumnWidth(i, column_width[i])
        tabla_widget.setHorizontalHeaderLabels(headers)

        tableindex = 0

        for tableindex, row in enumerate(self.eventos):

            lista_finalizado = ast.literal_eval(row[11])  # Convierte la cadena en lista, ejemplo lista_finalizado = [["1", "2025/03/11", "Juan Doe"], ["0", "2025/03/11", "Juan Doe"]]

            # Desempaquetamos las listas internas
            finalizado_interno_num, fecha_interno, encargado_interno = lista_finalizado[0]
            finalizado_num, fecha, encargado = lista_finalizado[1]

            # Formateamos los strings con "\n". Usamos f-strings para mayor claridad
            finalizado_interno = f"{finalizado_interno_num}\n{fecha_interno}\n{encargado_interno}"
            finalizado = f"{finalizado_num}\n{fecha}\n{encargado}"

            lista_encargados = ast.literal_eval(row[10]) # ejemplo lista_encargados = ["Tomás Draese", "Nicolas Errigo", "Facundo Astrada"]
            encargados_formateado = "\n".join(lista_encargados)

            lista_fechas_limite = ast.literal_eval(row[9])
            ultima_fecha, ultimo_nombre = lista_fechas_limite[-1]
            # Formatear el string con salto de línea
            fecha_limite_formateada = f"""{ultima_fecha}\n{ultimo_nombre}"""
            
            fmt = "%Y/%m/%d"  # Formato de la fecha
            hoy = datetime.today().date()
            fecha_obj = datetime.strptime(ultima_fecha, fmt).date()  # Convertimos directamente a date

            for colindex, value in enumerate([row[0], row[4], row[1], row[7], row[2], encargados_formateado, fecha_limite_formateada, finalizado_interno, finalizado]):
                try:
                    tabla_widget.setItem(tableindex, colindex, QtWidgets.QTableWidgetItem(str(value)))
                    tabla_widget.item(tableindex, colindex).setTextAlignment(Qt.AlignCenter)
                except:
                    print("[ERROR] Error al agregar item o no existen items")
            num_saltos = row[2].count("\n")
            tabla_widget.setRowHeight(tableindex, 30 + 25*num_saltos)
        
            colors = {"0": QColor(255, 0, 0, 100),
                    "1": QColor(0, 255, 0, 100),}
            
            # Calcular la diferencia en días
            diferencia = (fecha_obj - hoy).days
            if diferencia <= 7:
                tabla_widget.item(tableindex, 6).setBackground(QColor(255, 0, 0, 100))
            elif 7 < diferencia <= 14:
                tabla_widget.item(tableindex, 6).setBackground(QColor(255, 120, 0, 100))
            elif 14 < diferencia <= 21:
                tabla_widget.item(tableindex, 6).setBackground(QColor(255, 255, 0, 100))
            elif diferencia > 21:
                tabla_widget.item(tableindex, 6).setBackground(QColor(0, 255, 0, 100))

            if finalizado_interno_num in colors:
                tabla_widget.item(tableindex, 7).setBackground(colors[finalizado_interno_num])
            if finalizado_num in colors:
                tabla_widget.item(tableindex, 8).setBackground(colors[finalizado_num])

        # Diccionario con los índices de columna y sus modos de ajuste
        resize_modes = {0: QHeaderView.ResizeMode.Interactive, 1: QHeaderView.ResizeMode.Interactive,
                    2: QHeaderView.ResizeMode.Interactive, 3: QHeaderView.ResizeMode.Interactive,
                    4: QHeaderView.ResizeMode.Stretch, 5: QHeaderView.ResizeMode.Interactive,            
                    6: QHeaderView.ResizeMode.Interactive, 7: QHeaderView.ResizeMode.Fixed, 
                    8: QHeaderView.ResizeMode.Fixed}
        # Aplicar los modos en un bucle
        for col, mode in resize_modes.items():
            tabla_widget.horizontalHeader().setSectionResizeMode(col, mode)

    def mostrar_eventos_especificos(self, tabla_widget, eventos):   
        """Muestra los eventos en la tabla."""
        self.eventos = eventos
        # self.eventos.sort(key=lambda x: (x[7], x[10]))
        tabla_widget.clear()

        tabla_widget.horizontalHeader().setVisible(True)
        tabla_widget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        tabla_widget.setRowCount(len(self.eventos))
        tabla_widget.setColumnCount(9)
        
        column_width = [30, 100, 100, 200, 500, 180, 120, 120, 120]
        headers = ["id", "Fecha Carga", "Empresa", "Empresa", "Descripción", "Encargado/s", "Fecha Límite", "Terminado", "Finalizado"]
        for i, header in enumerate(headers):
            tabla_widget.setColumnWidth(i, column_width[i])
        tabla_widget.setHorizontalHeaderLabels(headers)

        tableindex = 0

        for tableindex, row in enumerate(self.eventos):

            lista_finalizado = ast.literal_eval(row[11])  # Convierte la cadena en lista, ejemplo lista_finalizado = [["1", "2025/03/11", "Juan Doe"], ["0", "2025/03/11", "Juan Doe"]]

            # Desempaquetamos las listas internas
            finalizado_interno_num, fecha_interno, encargado_interno = lista_finalizado[0]
            finalizado_num, fecha, encargado = lista_finalizado[1]

            # Formateamos los strings con "\n". Usamos f-strings para mayor claridad
            finalizado_interno = f"{finalizado_interno_num}\n{fecha_interno}\n{encargado_interno}"
            finalizado = f"{finalizado_num}\n{fecha}\n{encargado}"

            lista_encargados = ast.literal_eval(row[10]) # ejemplo lista_encargados = ["Tomás Draese", "Nicolas Errigo", "Facundo Astrada"]
            encargados_formateado = "\n".join(lista_encargados)

            lista_fechas_limite = ast.literal_eval(row[9])
            ultima_fecha, ultimo_nombre = lista_fechas_limite[-1]
            # Formatear el string con salto de línea
            fecha_limite_formateada = f"""{ultima_fecha}\n{ultimo_nombre}"""

            fmt = "%Y/%m/%d"  # Formato de la fecha
            hoy = datetime.today().date()
            fecha_obj = datetime.strptime(ultima_fecha, fmt).date()

            for colindex, value in enumerate([row[0], row[4], row[1], row[7], row[2], encargados_formateado, fecha_limite_formateada, finalizado_interno, finalizado]):
                try:
                    tabla_widget.setItem(tableindex, colindex, QtWidgets.QTableWidgetItem(str(value)))
                    tabla_widget.item(tableindex, colindex).setTextAlignment(Qt.AlignCenter)
                except:
                    print("[ERROR] Error al agregar item o no existen items")
            num_saltos = row[2].count("\n")
            tabla_widget.setRowHeight(tableindex, 30 + 25*num_saltos)

            colors = {"0": QColor(255, 0, 0, 100),
                    "1": QColor(0, 255, 0, 100),}

            # Calcular la diferencia en días
            diferencia = (fecha_obj - hoy).days
            if diferencia <= 7:
                tabla_widget.item(tableindex, 6).setBackground(QColor(255, 0, 0, 100))
            elif 7 < diferencia <= 14:
                tabla_widget.item(tableindex, 6).setBackground(QColor(255, 120, 0, 100))
            elif 14 < diferencia <= 21:
                tabla_widget.item(tableindex, 6).setBackground(QColor(255, 255, 0, 100))
            elif diferencia > 21:
                tabla_widget.item(tableindex, 6).setBackground(QColor(0, 255, 0, 100))

            if finalizado_interno_num in colors:
                tabla_widget.item(tableindex, 7).setBackground(colors[finalizado_interno_num])
            if finalizado_num in colors:
                tabla_widget.item(tableindex, 8).setBackground(colors[finalizado_num])

        # Diccionario con los índices de columna y sus modos de ajuste
        resize_modes = {0: QHeaderView.ResizeMode.Interactive, 1: QHeaderView.ResizeMode.Interactive,
                    2: QHeaderView.ResizeMode.Interactive, 3: QHeaderView.ResizeMode.Interactive,
                    4: QHeaderView.ResizeMode.Stretch, 5: QHeaderView.ResizeMode.Interactive,            
                    6: QHeaderView.ResizeMode.Interactive, 7: QHeaderView.ResizeMode.Fixed, 
                    8: QHeaderView.ResizeMode.Fixed}
        # Aplicar los modos en un bucle
        for col, mode in resize_modes.items():
            tabla_widget.horizontalHeader().setSectionResizeMode(col, mode)

    def llamar_editar_evento(self, tabla_seleccionada):
        """Abre la ventana de edición de eventos."""
        sector_table_map = {self.tabla_eventos_syg_comex: "events_syg_comex", self.tabla_eventos_syg_gestion: "events_syg_gestion", 
                    self.tabla_eventos_syg_ingenieria: "events_syg_ingenieria", self.tabla_eventos_syg_laboratorio: "events_syg_laboratorio",
                    self.tabla_visitas_syg_ingenieria: "visitas_syg_ingenieria", self.tabla_eventos_syg_producto: "events_syg_producto",
                    self.tabla_eventos_mgm_academia: "events_mgm_academia", self.tabla_eventos_mgm_calidad: "events_mgm_calidad", 
                    self.tabla_eventos_mgm_comercial: "events_mgm_comercial", self.tabla_eventos_mgm_gestion: "events_mgm_gestion",
                    self.tabla_eventos_mgm_ingenieria: "events_mgm_ingenieria", self.tabla_eventos_mgm_laboratorio: "events_mgm_laboratorio", 
                    self.tabla_eventos_mgm_producto: "events_mgm_producto", 12: "events_admin_administracion"}
        datos_evento = tabla_seleccionada.selectedItems()
        fecha_carga = datos_evento[0].text()
        empresa = datos_evento[1].text()
        descripcion = datos_evento[2].text()
        encargado = datos_evento[3].text()
        fecha_evento = datos_evento[4].text()  
        evento = self.claseSQLite.buscar_evento_por_id(sector_table_map[tabla_seleccionada], datos_evento[0].text())
        self.ventana_editar_evento = EDIT_EVENT(self.user, sector_table_map[tabla_seleccionada], evento[0])
        self.ventana_editar_evento.show()

    def buscar_evento(self, line_buscar):
        """Busca eventos en la tabla seleccionada."""
        sector_table_map = {self.line_buscar_tabla_syg_comex: ["events_syg_comex", self.tabla_eventos_syg_comex], 
                            self.line_buscar_tabla_syg_gestion: ["events_syg_gestion", self.tabla_eventos_syg_gestion], 
                            self.line_buscar_tabla_syg_ingenieria: ["events_syg_ingenieria", self.tabla_eventos_syg_ingenieria], 
                            self.line_buscar_tabla_syg_laboratorio: ["events_syg_laboratorio", self.tabla_eventos_syg_laboratorio],
                            self.line_buscar_tabla_syg_visitas_ingenieria: ["visitas_syg_ingenieria", self.tabla_visitas_syg_ingenieria], 
                            self.line_buscar_tabla_syg_producto: ["events_syg_producto", self.tabla_eventos_syg_producto],
                            self.line_buscar_tabla_mgm_academia: ["events_mgm_academia", self.tabla_eventos_mgm_academia], 
                            self.line_buscar_tabla_mgm_calidad: ["events_mgm_calidad", self.tabla_eventos_mgm_calidad], 
                            self.line_buscar_tabla_mgm_comercial: ["events_mgm_comercial", self.tabla_eventos_mgm_comercial], 
                            self.line_buscar_tabla_mgm_gestion: ["events_mgm_gestion", self.tabla_eventos_mgm_gestion], 
                            self.line_buscar_tabla_mgm_ingenieria: ["events_mgm_ingenieria", self.tabla_eventos_mgm_ingenieria], 
                            self.line_buscar_tabla_mgm_laboratorio: ["events_mgm_laboratorio", self.tabla_eventos_mgm_laboratorio], 
                            self.line_buscar_tabla_mgm_producto: ["events_mgm_producto", self.tabla_eventos_mgm_producto]}
        
        if line_buscar.text() == '':
            self.refrescar_tabla()
        else:
            eventos_filtrados = self.claseSQLite.buscar_evento_por_keyword(sector_table_map[line_buscar][0], line_buscar.text())
            self.mostrar_eventos_especificos(sector_table_map[line_buscar][1], eventos_filtrados)