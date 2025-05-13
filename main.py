import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QHeaderView
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import QDate, QPoint, Qt, QTimer
from PyQt5 import QtWidgets
from PyQt5 import uic
from lib.sql import SQLite
from lib.agregar_evento import ADD_EVENT
from lib.editar_evento import EDIT_EVENT
from lib.agregar_empresa import ADD_COMPANY
from lib.eventos_archivados import ARCHIVE
from datetime import datetime, date, timedelta
import ast

class UI(QMainWindow):
    def __init__(self, user, parent=None):
        super(UI, self).__init__(parent)
        uic.loadUi(r"gui\gui.ui", self)  # Cargar la interfaz de Qt Designer
        
        self.user = user
        self.claseSQLite = SQLite(r"//192.168.10.5/syg/INGENIERIA/PRUEBA_SOFTWARE_MGM/db.db")
        self.ventana_agregar_evento = ADD_EVENT(user, self.refrescar_tabla)
        # self.ventana_agregar_empresa = ADD_COMPANY()

        self.msg_login = QMessageBox()
        self.msg_login.setIcon(QMessageBox.Information)
        self.msg_login.setText("Se ha iniciado sesión como " + user + ".")
        self.msg_login.setWindowTitle("Sesion iniciada.")
        self.msg_login.exec_()

        # VERSION DEL PROGRAMA
        self.action_version.setText("Versión 1.2.0 test build")

        botones_agregar = [self.boton_agregar_syg_comex, self.boton_agregar_syg_gestion, self.boton_agregar_syg_ingenieria,
                            self.boton_agregar_syg_laboratorio, self.boton_agregar_syg_visitas_ingenieria, self.boton_agregar_syg_calibraciones_ingenieria,
                            self.boton_agregar_syg_producto, self.boton_agregar_mgm_academia, self.boton_agregar_mgm_calidad, 
                            self.boton_agregar_mgm_comercial, self.boton_agregar_mgm_gestion, self.boton_agregar_mgm_ingenieria, 
                            self.boton_agregar_mgm_laboratorio, self.boton_agregar_mgm_producto]

        botones_eliminar = [self.boton_eliminar_syg_comex, self.boton_eliminar_syg_gestion, self.boton_eliminar_syg_ingenieria,
                            self.boton_eliminar_syg_laboratorio, self.boton_eliminar_syg_visitas_ingenieria, self.boton_eliminar_syg_calibraciones_ingenieria,
                            self.boton_eliminar_syg_producto, self.boton_eliminar_mgm_academia, self.boton_eliminar_mgm_calidad,
                            self.boton_eliminar_mgm_comercial, self.boton_eliminar_mgm_gestion, self.boton_eliminar_mgm_ingenieria, 
                            self.boton_eliminar_mgm_laboratorio, self.boton_eliminar_mgm_producto]

        botones_refresh = [self.boton_refrescar_syg_comex, self.boton_refrescar_syg_gestion, self.boton_refrescar_syg_ingenieria,
                            self.boton_refrescar_syg_laboratorio, self.boton_refrescar_syg_visitas_ingenieria, self.boton_refrescar_syg_calibraciones_ingenieria,
                            self.boton_refrescar_syg_producto, self.boton_refrescar_mgm_academia, self.boton_refrescar_mgm_calidad, 
                            self.boton_refrescar_mgm_comercial, self.boton_refrescar_mgm_gestion, self.boton_refrescar_mgm_ingenieria, 
                            self.boton_refrescar_mgm_laboratorio, self.boton_refrescar_mgm_producto]
        
        botones_archivo = [self.boton_archivo_syg_comex, self.boton_archivo_syg_gestion, self.boton_archivo_syg_ingenieria,
                            self.boton_archivo_syg_laboratorio, self.boton_archivo_syg_visitas_ingenieria, self.boton_archivo_syg_calibraciones_ingenieria,
                            self.boton_archivo_syg_producto, self.boton_archivo_mgm_academia, self.boton_archivo_mgm_calidad, 
                            self.boton_archivo_mgm_comercial, self.boton_archivo_mgm_gestion, self.boton_archivo_mgm_ingenieria, 
                            self.boton_archivo_mgm_laboratorio, self.boton_archivo_mgm_producto]

        lines_buscar = [self.line_buscar_tabla_syg_comex, self.line_buscar_tabla_syg_gestion, self.line_buscar_tabla_syg_ingenieria,
                        self.line_buscar_tabla_syg_laboratorio, self.line_buscar_tabla_syg_visitas_ingenieria, self.line_buscar_tabla_syg_calibraciones_ingenieria,
                        self.line_buscar_tabla_syg_producto, self.line_buscar_tabla_mgm_academia, self.line_buscar_tabla_mgm_calidad,
                        self.line_buscar_tabla_mgm_comercial, self.line_buscar_tabla_mgm_gestion, self.line_buscar_tabla_mgm_ingenieria, 
                        self.line_buscar_tabla_mgm_laboratorio, self.line_buscar_tabla_mgm_producto]

        for boton in botones_agregar:
            boton.clicked.connect(self.ventana_agregar_evento.show)

        for boton in botones_refresh:
            boton.clicked.connect(self.refrescar_tabla)

        for line in lines_buscar:
            line.textChanged.connect(lambda _, l=line: self.buscar_evento(l))

        for boton in botones_archivo:
            boton.clicked.connect(lambda _, b=boton: self.mostrar_tabla_archivo(b))

        self.refrescar_tabla()

        tablas_eventos = [self.tabla_eventos_syg_comex, self.tabla_eventos_syg_gestion, self.tabla_eventos_syg_ingenieria,
                        self.tabla_eventos_syg_laboratorio, self.tabla_visitas_syg_ingenieria, self.tabla_calibraciones_syg_ingenieria,
                        self.tabla_eventos_syg_producto, self.tabla_eventos_mgm_academia, self.tabla_eventos_mgm_calidad, 
                        self.tabla_eventos_mgm_comercial, self.tabla_eventos_mgm_gestion, self.tabla_eventos_mgm_ingenieria, 
                        self.tabla_eventos_mgm_laboratorio, self.tabla_eventos_mgm_producto]

        for tabla in tablas_eventos:
            tabla.doubleClicked.connect(lambda _, t=tabla: self.llamar_editar_evento(t))

        self.combo_syg_tabla_estadisticas.currentIndexChanged.connect(self.actualizar_estadisticas_syg)
        self.combo_mgm_tabla_estadisticas.currentIndexChanged.connect(self.actualizar_estadisticas_mgm)

        self.desbloquear_tabs()

        if self.user == "German Roldan" or self.user == "Matias Roldan":
            self.actualizar_estadisticas_syg()
            self.actualizar_estadisticas_mgm()
            self.desbloquear_admin()
            self.mostrar_eventos_tabla_admin("todo", self.tabla_eventos_todo_admin)
            self.mostrar_eventos_tabla_admin("syg", self.tabla_eventos_syg_admin)
            self.mostrar_eventos_tabla_admin("mgm", self.tabla_eventos_mgm_admin)

        # self.action_agregar_empresa.triggered.connect(self.ventana_agregar_empresa.show)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refrescar_tabla)
        self.timer.start(60000)  # refresca las tablas cada 15 segundos

    def desbloquear_admin(self):
        # self.tabWidget_2.setTabEnabled(2, True)
        [self.tabWidget.setTabEnabled(i, True) for i in range(7, -1, -1)]
        [self.tabWidget_2.setTabEnabled(i, True) for i in range(2, -1, -1)]
        [self.tabWidget_3.setTabEnabled(i, True) for i in range(7, -1, -1)]

    def desbloquear_tabs(self):
        sectores = ast.literal_eval(self.claseSQLite.buscar_usuario(self.user)[4])
        """Desbloquea las tabs según los sectores del usuario."""
        [self.tabWidget.setTabEnabled(i, False) for i in range(7, -1, -1)]
        [self.tabWidget_2.setTabEnabled(i, False) for i in range(2, -1, -1)]
        [self.tabWidget_3.setTabEnabled(i, False) for i in range(7, -1, -1)]

        # Diccionario que mapea los sectores a los índices de las pestañas
        sectores_map = {"mgm_producto": (1, 6), "mgm_laboratorio": (1, 5), "mgm_ingenieria": (1, 4),
                        "mgm_gestion": (1, 3), "mgm_comercial": (1, 2), "mgm_calidad": (1, 1),
                        "mgm_academia": (1, 0), "syg_producto": (0, 6), "syg_calibraciones_ingenieria": (0, 5),
                        "syg_visitas_ingenieria": (0, 4), "syg_laboratorio": (0, 3), "syg_ingenieria": (0, 2), 
                        "syg_gestion": (0, 1), "syg_comex": (0, 0),}

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

    def refrescar_tabla(self):
        sectores = ast.literal_eval(self.claseSQLite.buscar_usuario(self.user)[4])
        tablas_por_sectores = {'syg_comex': ["events_syg_comex", self.tabla_eventos_syg_comex], 
                            'syg_gestion': ["events_syg_gestion", self.tabla_eventos_syg_gestion], 
                            'syg_ingenieria': ["events_syg_ingenieria", self.tabla_eventos_syg_ingenieria], 
                            'syg_laboratorio': ["events_syg_laboratorio", self.tabla_eventos_syg_laboratorio],
                            'syg_visitas_ingenieria': ["visitas_syg_ingenieria", self.tabla_visitas_syg_ingenieria],
                            'syg_calibraciones_ingenieria': ["calibraciones_syg_ingenieria", self.tabla_calibraciones_syg_ingenieria],
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
        def ordenar_por_ultima_fecha(lista):
            """ Ordena la lista en base a la última fecha agregada en la casilla 9 """
            
            def get_last_added_date(entry):
                """ Extrae la última fecha agregada de la casilla 9 """
                try:
                    dates_list = ast.literal_eval(entry[9])  # Convierte el string en lista de listas
                    last_added_date = dates_list[-1][0]  # Toma la fecha del último elemento
                    return last_added_date
                except (ValueError, SyntaxError, IndexError):
                    return "1900/01/01"  # En caso de error, usa una fecha muy antigua

            # Ordena la lista por la última fecha agregada en orden descendente
            return sorted(lista, key=get_last_added_date, reverse=False)
        
        """Muestra los eventos en la tabla."""

        self.eventos = self.claseSQLite.leer_eventos(tabla_db)
        
        self.eventos = ordenar_por_ultima_fecha(self.eventos)
        # self.eventos.sort(key=lambda x: (x[9]))
        
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
        menos = 0

        for i, row in enumerate(self.eventos):
            lista_finalizado = ast.literal_eval(row[11])  # Convierte la cadena en lista, ejemplo lista_finalizado = [["1", "2025/03/11", "Juan Doe"], ["0", "2025/03/11", "Juan Doe"]]

            # Desempaquetamos las listas internas
            finalizado_interno_num, fecha_interno, encargado_interno = lista_finalizado[0]
            if finalizado_interno_num == "0":
                finalizado_num, fecha, encargado = lista_finalizado[1]
                fecha_interno_formateada = datetime.strptime(fecha_interno, "%Y/%m/%d").strftime("%d/%m/%Y")
                fecha_formateada = datetime.strptime(fecha, "%Y/%m/%d").strftime("%d/%m/%Y")
                # Formateamos los strings con "\n". Usamos f-strings para mayor claridad
                finalizado_interno = f"{finalizado_interno_num}\n{fecha_interno_formateada}\n{encargado_interno}"
                finalizado = f"{finalizado_num}\n{fecha_formateada}\n{encargado}"

                lista_encargados = ast.literal_eval(row[10]) # ejemplo lista_encargados = ["Tomás Draese", "Nicolas Errigo", "Facundo Astrada"]
                encargados_formateado = "\n".join(lista_encargados)

                lista_fechas_limite = ast.literal_eval(row[9])
                ultima_fecha, ultimo_nombre = lista_fechas_limite[-1]

                # Format the datetime object into the desired format
                ultima_fecha_formateada = datetime.strptime(ultima_fecha, "%Y/%m/%d").strftime("%d/%m/%Y")
                # Formatear el string con salto de línea
                fecha_limite_formateada = f"""{ultima_fecha_formateada}\n{ultimo_nombre}"""

                fecha_carga_formateada = datetime.strptime(row[4], "%Y/%m/%d").strftime("%d/%m/%Y")

                fmt = "%Y/%m/%d"  # Formato de la fecha
                hoy = datetime.today().date()
                fecha_obj = datetime.strptime(ultima_fecha, fmt).date()  # Convertimos directamente a date

                for colindex, value in enumerate([row[0], fecha_carga_formateada, row[1], row[7], row[2], encargados_formateado, fecha_limite_formateada, finalizado_interno, finalizado]):
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
                tableindex += 1
            else:    
                menos += 1
                tabla_widget.setRowCount(len(self.eventos) - menos)

        # Diccionario con los índices de columna y sus modos de ajuste
        resize_modes = {0: QHeaderView.ResizeMode.Interactive, 1: QHeaderView.ResizeMode.Interactive,
                    2: QHeaderView.ResizeMode.Interactive, 3: QHeaderView.ResizeMode.Interactive,
                    4: QHeaderView.ResizeMode.Stretch, 5: QHeaderView.ResizeMode.Interactive,            
                    6: QHeaderView.ResizeMode.Interactive, 7: QHeaderView.ResizeMode.Fixed, 
                    8: QHeaderView.ResizeMode.Fixed}
        # Aplicar los modos en un bucle
        for col, mode in resize_modes.items():
            tabla_widget.horizontalHeader().setSectionResizeMode(col, mode)

    def mostrar_eventos_tabla_admin(self, tabla, tabla_widget):
        """Muestra los eventos en la tabla."""
        tablas_por_sectores = {'syg': [["events_syg_comex", "Eventos SYG Comex"], ["events_syg_gestion", "Eventos SYG Gestión"], 
                                    ["events_syg_ingenieria", "Eventos SYG Ingeniería"], ["events_syg_laboratorio", "Eventos SYG Laboratorio"],
                                    ["visitas_syg_ingenieria", "Visitas SYG Ingeniería"], ["calibraciones_syg_ingenieria", "Calibraciones SYG Ingeniería"],
                                    ["events_syg_producto", "Eventos SYG Producto"]],
                                'mgm': [["events_mgm_academia", "Eventos MGM Academia"], ["events_mgm_calidad", "Eventos MGM Calidad"], 
                                    ["events_mgm_comercial", "Eventos MGM Comercial"], ["events_mgm_gestion", "Eventos MGM Gestión"], 
                                    ["events_mgm_ingenieria", "Eventos MGM Ingeniería"], ["events_mgm_laboratorio", "Eventos MGM Laboratorio"], 
                                    ["events_mgm_producto", "Eventos MGM Producto"]],
                                'todo': [["events_syg_comex", "Eventos SYG Comex"], ["events_syg_gestion", "Eventos SYG Gestión"],
                                    ["events_syg_ingenieria", "Eventos SYG Ingeniería"], ["events_syg_laboratorio", "Eventos SYG Laboratorio"],
                                    ["visitas_syg_ingenieria", "Visitas SYG Ingeniería"], ["calibraciones_syg_ingenieria", "Calibraciones SYG Ingeniería"], 
                                    ["events_syg_producto", "Eventos SYG Producto"], ["events_mgm_academia", "Eventos MGM Academia"], 
                                    ["events_mgm_calidad", "Eventos MGM Calidad"], ["events_mgm_comercial", "Eventos MGM Comercial"], 
                                    ["events_mgm_gestion", "Eventos MGM Gestión"], ["events_mgm_ingenieria", "Eventos MGM Ingeniería"], 
                                    ["events_mgm_laboratorio", "Eventos MGM Laboratorio"], ["events_mgm_producto", "Eventos MGM Producto"]]}
        
        tabla_widget.clear()
        tableindex = 0
        menos = 0
        tabla_widget.setRowCount(sum(len(self.claseSQLite.leer_eventos(tabla[0])) for tabla in tablas_por_sectores[tabla]))

        for tabla_info in tablas_por_sectores[tabla]:
            self.eventos = self.claseSQLite.leer_eventos(tabla_info[0])
            # self.eventos.sort(key=lambda x: (x[7], x[10]))

            tabla_widget.horizontalHeader().setVisible(True)
            tabla_widget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            tabla_widget.setColumnCount(10)

            column_width = [100, 30, 100, 100, 200, 500, 180, 120, 120, 120]
            headers = ["Tabla", "id", "Fecha Carga", "Empresa", "Empresa", "Descripción", "Encargado/s", "Fecha Límite", "Terminado", "Finalizado"]
            for i, header in enumerate(headers):
                tabla_widget.setColumnWidth(i, column_width[i])
            tabla_widget.setHorizontalHeaderLabels(headers)
            if self.eventos:
                for i, row in enumerate(self.eventos):
                    lista_finalizado = ast.literal_eval(row[11])  # Convierte la cadena en lista, ejemplo lista_finalizado = [["1", "2025/03/11", "Juan Doe"], ["0", "2025/03/11", "Juan Doe"]]

                    # Desempaquetamos las listas internas
                    finalizado_interno_num, fecha_interno, encargado_interno = lista_finalizado[0]
                    # if finalizado_interno_num == "0":
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

                    for colindex, value in enumerate([tabla_info[1], row[0], row[4], row[1], row[7], row[2], encargados_formateado, fecha_limite_formateada, finalizado_interno, finalizado]):
                        try:                            
                            item = QtWidgets.QTableWidgetItem(str(value))  # Crear el item
                            tabla_widget.setItem(tableindex, colindex, item)  # Asignarlo a la tabla
                            
                            if item is not None:  # Verificar que el item no es None
                                item.setTextAlignment(Qt.AlignCenter)
                            else:
                                print(f"[WARNING] No se pudo agregar el item en ({tableindex}, {colindex})")
                        
                        except Exception as e:
                            print("[ERROR] Error al agregar item o no existen items: ", e)
                            
                    num_saltos = row[2].count("\n")
                    tabla_widget.setRowHeight(tableindex, 30 + 25*num_saltos)

                    colors = {"0": QColor(255, 0, 0, 100),
                            "1": QColor(0, 255, 0, 100),}
                    
                    # Calcular la diferencia en días
                    diferencia = (fecha_obj - hoy).days
                    if diferencia <= 7:
                        tabla_widget.item(tableindex, 7).setBackground(QColor(255, 0, 0, 100))
                    elif 7 < diferencia <= 14:
                        tabla_widget.item(tableindex, 7).setBackground(QColor(255, 120, 0, 100))
                    elif 14 < diferencia <= 21:
                        tabla_widget.item(tableindex, 7).setBackground(QColor(255, 255, 0, 100))
                    elif diferencia > 21:
                        tabla_widget.item(tableindex, 7).setBackground(QColor(0, 255, 0, 100))

                    if finalizado_interno_num in colors:
                        tabla_widget.item(tableindex, 8).setBackground(colors[finalizado_interno_num])
                    if finalizado_num in colors:
                        tabla_widget.item(tableindex, 9).setBackground(colors[finalizado_num])
                        
                    tableindex += 1

            # Diccionario con los índices de columna y sus modos de ajuste
            resize_modes = {0: QHeaderView.ResizeMode.Interactive, 1: QHeaderView.ResizeMode.Interactive, 2: QHeaderView.ResizeMode.Interactive, 
                            3: QHeaderView.ResizeMode.Interactive, 4: QHeaderView.ResizeMode.Stretch, 5: QHeaderView.ResizeMode.Interactive,            
                        6: QHeaderView.ResizeMode.Interactive, 7: QHeaderView.ResizeMode.Fixed, 8: QHeaderView.ResizeMode.Fixed}
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
        menos = 0

        for i, row in enumerate(self.eventos):

            lista_finalizado = ast.literal_eval(row[11])  # Convierte la cadena en lista, ejemplo lista_finalizado = [["1", "2025/03/11", "Juan Doe"], ["0", "2025/03/11", "Juan Doe"]]

            # Desempaquetamos las listas internas
            finalizado_interno_num, fecha_interno, encargado_interno = lista_finalizado[0]
            if finalizado_interno_num == "0":
                finalizado_num, fecha, encargado = lista_finalizado[1]
                fecha_interno_formateada = datetime.strptime(fecha_interno, "%Y/%m/%d").strftime("%d/%m/%Y")
                fecha_formateada = datetime.strptime(fecha, "%Y/%m/%d").strftime("%d/%m/%Y")
                # Formateamos los strings con "\n". Usamos f-strings para mayor claridad
                finalizado_interno = f"{finalizado_interno_num}\n{fecha_interno_formateada}\n{encargado_interno}"
                finalizado = f"{finalizado_num}\n{fecha_formateada}\n{encargado}"

                lista_encargados = ast.literal_eval(row[10]) # ejemplo lista_encargados = ["Tomás Draese", "Nicolas Errigo", "Facundo Astrada"]
                encargados_formateado = "\n".join(lista_encargados)

                lista_fechas_limite = ast.literal_eval(row[9])
                ultima_fecha, ultimo_nombre = lista_fechas_limite[-1]

                # Format the datetime object into the desired format
                ultima_fecha_formateada = datetime.strptime(ultima_fecha, "%Y/%m/%d").strftime("%d/%m/%Y")
                # Formatear el string con salto de línea
                fecha_limite_formateada = f"""{ultima_fecha_formateada}\n{ultimo_nombre}"""

                fecha_carga_formateada = datetime.strptime(row[4], "%Y/%m/%d").strftime("%d/%m/%Y")

                fmt = "%Y/%m/%d"  # Formato de la fecha
                hoy = datetime.today().date()
                fecha_obj = datetime.strptime(ultima_fecha, fmt).date()  # Convertimos directamente a date

                for colindex, value in enumerate([row[0], fecha_carga_formateada, row[1], row[7], row[2], encargados_formateado, fecha_limite_formateada, finalizado_interno, finalizado]):
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
                tableindex += 1
            else:
                menos += 1
                tabla_widget.setRowCount(len(self.eventos) - menos)
        # Diccionario con los índices de columna y sus modos de ajuste
        resize_modes = {0: QHeaderView.ResizeMode.Interactive, 1: QHeaderView.ResizeMode.Interactive,
                    2: QHeaderView.ResizeMode.Interactive, 3: QHeaderView.ResizeMode.Interactive,
                    4: QHeaderView.ResizeMode.Stretch, 5: QHeaderView.ResizeMode.Interactive,            
                    6: QHeaderView.ResizeMode.Interactive, 7: QHeaderView.ResizeMode.Fixed, 
                    8: QHeaderView.ResizeMode.Fixed}
        # Aplicar los modos en un bucle
        for col, mode in resize_modes.items():
            tabla_widget.horizontalHeader().setSectionResizeMode(col, mode)

    def mostrar_tabla_archivo(self, boton):
        sector_table_map = {self.boton_archivo_syg_comex: ["events_syg_comex", self.tabla_eventos_syg_comex],
                            self.boton_archivo_syg_gestion: ["events_syg_gestion", self.tabla_eventos_syg_gestion], 
                            self.boton_archivo_syg_ingenieria: ["events_syg_ingenieria", self.tabla_eventos_syg_ingenieria], 
                            self.boton_archivo_syg_laboratorio: ["events_syg_laboratorio", self.tabla_eventos_syg_laboratorio],
                            self.boton_archivo_syg_visitas_ingenieria: ["visitas_syg_ingenieria", self.tabla_visitas_syg_ingenieria], 
                            self.boton_archivo_syg_calibraciones_ingenieria: ["calibraciones_syg_ingenieria", self.tabla_calibraciones_syg_ingenieria],
                            self.boton_archivo_syg_producto: ["events_syg_producto", self.tabla_eventos_syg_producto],
                            self.boton_archivo_mgm_academia: ["events_mgm_academia", self.tabla_eventos_mgm_academia], 
                            self.boton_archivo_mgm_calidad: ["events_mgm_calidad", self.tabla_eventos_mgm_calidad], 
                            self.boton_archivo_mgm_comercial: ["events_mgm_comercial", self.tabla_eventos_mgm_comercial], 
                            self.boton_archivo_mgm_gestion: ["events_mgm_gestion", self.tabla_eventos_mgm_gestion], 
                            self.boton_archivo_mgm_ingenieria: ["events_mgm_ingenieria", self.tabla_eventos_mgm_ingenieria], 
                            self.boton_archivo_mgm_laboratorio: ["events_mgm_laboratorio", self.tabla_eventos_mgm_laboratorio], 
                            self.boton_archivo_mgm_producto: ["events_mgm_producto", self.tabla_eventos_mgm_producto]}
        
        self.ventana_archivo = ARCHIVE(self.user, sector_table_map[boton][0])
        self.ventana_archivo.show()

    def llamar_editar_evento(self, tabla_seleccionada):
        """Abre la ventana de edición de eventos."""
        sector_table_map = {self.tabla_eventos_syg_comex: "events_syg_comex", self.tabla_eventos_syg_gestion: "events_syg_gestion", 
                    self.tabla_eventos_syg_ingenieria: "events_syg_ingenieria", self.tabla_eventos_syg_laboratorio: "events_syg_laboratorio",
                    self.tabla_visitas_syg_ingenieria: "visitas_syg_ingenieria", self.tabla_eventos_syg_producto: "events_syg_producto",
                    self.tabla_eventos_mgm_academia: "events_mgm_academia", self.tabla_eventos_mgm_calidad: "events_mgm_calidad", 
                    self.tabla_eventos_mgm_comercial: "events_mgm_comercial", self.tabla_eventos_mgm_gestion: "events_mgm_gestion",
                    self.tabla_eventos_mgm_ingenieria: "events_mgm_ingenieria", self.tabla_eventos_mgm_laboratorio: "events_mgm_laboratorio", 
                    self.tabla_eventos_mgm_producto: "events_mgm_producto", self.tabla_calibraciones_syg_ingenieria: "calibraciones_syg_ingenieria",
                    12: "events_admin_administracion"}
        datos_evento = tabla_seleccionada.selectedItems()
        fecha_carga = datos_evento[0].text()
        empresa = datos_evento[1].text()
        descripcion = datos_evento[2].text()
        encargado = datos_evento[3].text()
        fecha_evento = datos_evento[4].text()  
        evento = self.claseSQLite.buscar_evento_por_id(sector_table_map[tabla_seleccionada], datos_evento[0].text())
        self.ventana_editar_evento = EDIT_EVENT(self.user, self.refrescar_tabla, sector_table_map[tabla_seleccionada], evento[0])
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

    def actualizar_estadisticas_syg(self):
        fecha_hoy = datetime.today().date()
        fecha_hoy_str = fecha_hoy.strftime("%Y/%m/%d")
        fechas_semana = [fecha_hoy - timedelta(days=i) for i in range(7)]
        fecha_semana_str = [fecha.strftime("%Y/%m/%d") for fecha in fechas_semana]
        fechas_mes = [fecha_hoy - timedelta(days=i) for i in range(30)]
        fecha_mes_str = [fecha.strftime("%Y/%m/%d") for fecha in fechas_mes]

        tablas_eventos_syg = ["events_syg_comex", "events_syg_gestion", "events_syg_ingenieria", "events_syg_laboratorio", 
                              "visitas_syg_ingenieria", "calibraciones_syg_ingenieria", "events_syg_producto"]

        eventos_syg_hoy = eventos_syg_semana = eventos_syg_mes = eventos_syg_total = eventos_syg_terminados = eventos_syg_editados_hoy = eventos_syg_editados_semana = eventos_syg_editados_mes = 0

        if self.combo_syg_tabla_estadisticas.currentIndex() == 0:
            for tabla in tablas_eventos_syg:
                eventos_syg_hoy = eventos_syg_hoy + len(self.claseSQLite.buscar_registros_por_fecha_creacion(tabla, fecha_hoy_str))
                eventos_syg_editados_hoy = eventos_syg_editados_hoy + len(self.claseSQLite.buscar_registros_por_fecha_modificacion(tabla, fecha_hoy_str))
                for fecha in fecha_semana_str:
                    eventos_syg_semana = eventos_syg_semana + len(self.claseSQLite.buscar_registros_por_fecha_creacion(tabla, fecha))
                    eventos_syg_editados_semana = eventos_syg_editados_semana + len(self.claseSQLite.buscar_registros_por_fecha_modificacion(tabla, fecha))
                for fecha in fecha_mes_str:
                    eventos_syg_mes = eventos_syg_mes + len(self.claseSQLite.buscar_registros_por_fecha_creacion(tabla, fecha))
                    eventos_syg_editados_mes = eventos_syg_editados_mes + len(self.claseSQLite.buscar_registros_por_fecha_modificacion(tabla, fecha))
                total_eventos = self.claseSQLite.leer_eventos(tabla)
                eventos_syg_total = eventos_syg_total + len(total_eventos)
                finalizados = [ast.literal_eval(evento[11]) for evento in total_eventos]

                for lista_finalizado in finalizados:
                    for finalizado in lista_finalizado:
                        if finalizado[0] == "1":
                            eventos_syg_terminados += 1
        else:
            tabla = tablas_eventos_syg[self.combo_syg_tabla_estadisticas.currentIndex() - 1]
            eventos_syg_hoy = eventos_syg_hoy + len(self.claseSQLite.buscar_registros_por_fecha_creacion(tabla, fecha_hoy_str))
            eventos_syg_editados_hoy = eventos_syg_editados_hoy + len(self.claseSQLite.buscar_registros_por_fecha_modificacion(tabla, fecha_hoy_str))
            for fecha in fecha_semana_str:
                eventos_syg_semana = eventos_syg_semana + len(self.claseSQLite.buscar_registros_por_fecha_creacion(tabla, fecha))
                eventos_syg_editados_semana = eventos_syg_editados_semana + len(self.claseSQLite.buscar_registros_por_fecha_modificacion(tabla, fecha))
            for fecha in fecha_mes_str:
                eventos_syg_mes = eventos_syg_mes + len(self.claseSQLite.buscar_registros_por_fecha_creacion(tabla, fecha))
                eventos_syg_editados_mes = eventos_syg_editados_mes + len(self.claseSQLite.buscar_registros_por_fecha_modificacion(tabla, fecha))
            total_eventos = self.claseSQLite.leer_eventos(tabla)
            eventos_syg_total = eventos_syg_total + len(total_eventos)
            finalizados = [ast.literal_eval(evento[11]) for evento in total_eventos]

            for lista_finalizado in finalizados:
                for finalizado in lista_finalizado:
                    if finalizado[0] == "1":
                        eventos_syg_terminados += 1

        # Suponiendo que tienes estos labels definidos para syg en tu GUI
        self.label_syg_eventos_cargados_hoy.setText(str(eventos_syg_hoy))
        self.label_syg_eventos_cargados_semana.setText(str(eventos_syg_semana))
        self.label_syg_eventos_cargados_mes.setText(str(eventos_syg_mes))
        self.label_syg_eventos_totales.setText(str(eventos_syg_total))
        self.label_syg_eventos_terminados.setText(str(eventos_syg_terminados))
        self.label_syg_eventos_editados_hoy.setText(str(eventos_syg_editados_hoy))
        self.label_syg_eventos_editados_semana.setText(str(eventos_syg_editados_semana))
        self.label_syg_eventos_editados_mes.setText(str(eventos_syg_editados_mes))

    def actualizar_estadisticas_mgm(self):
        fecha_hoy = datetime.today().date()
        fecha_hoy_str = fecha_hoy.strftime("%Y/%m/%d")
        fechas_semana = [fecha_hoy - timedelta(days=i) for i in range(7)]
        fecha_semana_str = [fecha.strftime("%Y/%m/%d") for fecha in fechas_semana]
        fechas_mes = [fecha_hoy - timedelta(days=i) for i in range(30)]
        fecha_mes_str = [fecha.strftime("%Y/%m/%d") for fecha in fechas_mes]

        tablas_eventos_mgm = ["events_mgm_academia", "events_mgm_calidad", "events_mgm_comercial", "events_mgm_gestion",
                            "events_mgm_ingenieria", "events_mgm_laboratorio", "events_mgm_producto"]

        eventos_mgm_hoy = eventos_mgm_semana = eventos_mgm_mes = eventos_mgm_total = eventos_mgm_terminados = eventos_mgm_editados_hoy = eventos_mgm_editados_semana = eventos_mgm_editados_mes = 0

        if self.combo_mgm_tabla_estadisticas.currentIndex() == 0:
            for tabla in tablas_eventos_mgm:
                eventos_mgm_hoy += len(self.claseSQLite.buscar_registros_por_fecha_creacion(tabla, fecha_hoy_str))
                eventos_mgm_editados_hoy += len(self.claseSQLite.buscar_registros_por_fecha_modificacion(tabla, fecha_hoy_str))
                for fecha in fecha_semana_str:
                    eventos_mgm_semana += len(self.claseSQLite.buscar_registros_por_fecha_creacion(tabla, fecha))
                    eventos_mgm_editados_semana += len(self.claseSQLite.buscar_registros_por_fecha_modificacion(tabla, fecha))
                for fecha in fecha_mes_str:
                    eventos_mgm_mes += len(self.claseSQLite.buscar_registros_por_fecha_creacion(tabla, fecha))
                    eventos_mgm_editados_mes += len(self.claseSQLite.buscar_registros_por_fecha_modificacion(tabla, fecha))

                total_eventos = self.claseSQLite.leer_eventos(tabla)
                eventos_mgm_total += len(total_eventos)

                finalizados = [ast.literal_eval(evento[11]) for evento in total_eventos]
                for lista_finalizado in finalizados:
                    for finalizado in lista_finalizado:
                        if finalizado[0] == "1":
                            eventos_mgm_terminados += 1
        else:
            tabla = tablas_eventos_mgm[self.combo_mgm_tabla_estadisticas.currentIndex() - 1]
            eventos_mgm_hoy += len(self.claseSQLite.buscar_registros_por_fecha_creacion(tabla, fecha_hoy_str))
            eventos_mgm_editados_hoy += len(self.claseSQLite.buscar_registros_por_fecha_modificacion(tabla, fecha_hoy_str))
            for fecha in fecha_semana_str:
                eventos_mgm_semana += len(self.claseSQLite.buscar_registros_por_fecha_creacion(tabla, fecha))
                eventos_mgm_editados_semana += len(self.claseSQLite.buscar_registros_por_fecha_modificacion(tabla, fecha))
            for fecha in fecha_mes_str:
                eventos_mgm_mes += len(self.claseSQLite.buscar_registros_por_fecha_creacion(tabla, fecha))
                eventos_mgm_editados_mes += len(self.claseSQLite.buscar_registros_por_fecha_modificacion(tabla, fecha))

            total_eventos = self.claseSQLite.leer_eventos(tabla)
            eventos_mgm_total += len(total_eventos)

            finalizados = [ast.literal_eval(evento[11]) for evento in total_eventos]
            for lista_finalizado in finalizados:
                for finalizado in lista_finalizado:
                    if finalizado[0] == "1":
                        eventos_mgm_terminados += 1

        # Suponiendo que tienes estos labels definidos para mgm en tu GUI
        self.label_mgm_eventos_cargados_hoy.setText(str(eventos_mgm_hoy))
        self.label_mgm_eventos_cargados_semana.setText(str(eventos_mgm_semana))
        self.label_mgm_eventos_cargados_mes.setText(str(eventos_mgm_mes))
        self.label_mgm_eventos_totales.setText(str(eventos_mgm_total))
        self.label_mgm_eventos_terminados.setText(str(eventos_mgm_terminados))
        self.label_mgm_eventos_editados_hoy.setText(str(eventos_mgm_editados_hoy))
        self.label_mgm_eventos_editados_semana.setText(str(eventos_mgm_editados_semana))
        self.label_mgm_eventos_editados_mes.setText(str(eventos_mgm_editados_mes))