import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import QDate, QPoint, Qt
from PyQt5 import uic
from lib.sql import SQLite
from datetime import datetime

class ADD_EVENT(QMainWindow):
    def __init__(self, user, parent=None):
        super(ADD_EVENT, self).__init__(parent)
        uic.loadUi("gui\gui_agregar_evento.ui", self)  # Cargar la interfaz de Qt Designer