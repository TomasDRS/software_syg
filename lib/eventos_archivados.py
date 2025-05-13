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

class ARCHIVE(QMainWindow):
    def __init__(self, user, tabla, parent=None):
        super(ARCHIVE, self).__init__(parent)
        uic.loadUi(r"gui\gui_eventos_archivados.ui", self)  # Cargar la interfaz de Qt Designer

        self.setWindowTitle("Eventos Archivados")
        self.claseSQLite = SQLite(r"//192.168.10.5/syg/INGENIERIA/PRUEBA_SOFTWARE_MGM/db.db")

        tablas_por_sectores = {"events_syg_comex": "SYG Comex", "events_syg_gestion": "SYG Gestión", "events_syg_ingenieria": "SYG Ingeniería", 
        "events_syg_laboratorio": "SYG Laboratorio", "visitas_syg_ingenieria": "Visitas SYG Ingeniería", 
        "calibraciones_syg_ingenieria": "Calibraciones SYG Ingeniería", "events_syg_producto": "SYG Producto", "events_mgm_academia": "MGM Academia", 
        "events_mgm_calidad": "MGM Calidad", "events_mgm_comercial": "MGM Comercial", "events_mgm_gestion": "MGM Gestión",
        "events_mgm_ingenieria": "MGM Ingeniería", "events_mgm_laboratorio": "MGM Laboratorio", "events_mgm_producto": "MGM Producto", 
        "events_syg_comex": "SYG Comex", "events_syg_gestion": "SYG Gestión", "events_syg_ingenieria": "SYG Ingeniería", 
        "events_syg_laboratorio": "SYG Laboratorio", "visitas_syg_ingenieria": "Visitas SYG Ingeniería", 
        "calibraciones_syg_ingenieria": "Calibraciones SYG Ingeniería", "events_syg_producto": "SYG Producto", "events_mgm_academia": "MGM Academia", 
        "events_mgm_calidad": "MGM Calidad", "events_mgm_comercial": "MGM Comercial", "events_mgm_gestion": "MGM Gestión", 
        "events_mgm_ingenieria": "MGM Ingeniería", "events_mgm_laboratorio": "MGM Laboratorio", "events_mgm_producto": "MGM Producto"}

        self.tabla = tabla
        self.user = user
        self.titulo_eventos_archivados.setText(f"Eventos Archivados de {tablas_por_sectores[tabla]}")
        self.line_buscar_tabla_eventos_archivados.textChanged.connect(lambda _, l=self.line_buscar_tabla_eventos_archivados: self.buscar_evento_archivado(l))
        self.mostrar_eventos_archivados(self.tabla)
        
        self.tabla_eventos_archivados.doubleClicked.connect(self.llamar_editar_evento)

    def mostrar_eventos_archivados(self, tabla_db):
        tabla_widget = self.tabla_eventos_archivados
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
            if finalizado_interno_num == "1":
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

    def buscar_evento_archivado(self, line_buscar):
        """Busca eventos en la tabla seleccionada."""        
        if line_buscar.text() == '':
            self.mostrar_eventos_archivados(self.tabla)
        else:
            eventos_filtrados = self.claseSQLite.buscar_evento_por_keyword(self.tabla, line_buscar.text())
            self.mostrar_eventos_archivados_especificos(eventos_filtrados)          

    def mostrar_eventos_archivados_especificos(self, eventos):
        """Muestra los eventos en la tabla."""
        self.eventos = eventos
        tabla_widget = self.tabla_eventos_archivados
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
            if finalizado_interno_num == "1":
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

    def llamar_editar_evento(self):
        """Abre la ventana de edición de eventos."""
        datos_evento = self.tabla_eventos_archivados.selectedItems()
        fecha_carga = datos_evento[0].text()
        empresa = datos_evento[1].text()
        descripcion = datos_evento[2].text()
        encargado = datos_evento[3].text()
        fecha_evento = datos_evento[4].text()  
        evento = self.claseSQLite.buscar_evento_por_id(self.tabla, datos_evento[0].text())
        self.ventana_editar_evento = EDIT_EVENT(self.user, lambda: self.mostrar_eventos_archivados(self.tabla), self.tabla, evento[0])
        self.ventana_editar_evento.show()