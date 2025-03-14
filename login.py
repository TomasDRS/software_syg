import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import QDate, QPoint, Qt
from PyQt5 import uic
from lib.sql import SQLite
from datetime import datetime

from main import UI  # Absolute import

class LOGIN(QMainWindow):
    def __init__(self, parent=None): 
        super(LOGIN, self).__init__(parent)
        uic.loadUi("gui\gui_login.ui", self)  # Cargar la interfaz de Qt Designer

        self.claseSQLite = SQLite(r"//192.168.10.5/syg/INGENIERIA/PRUEBA_SOFTWARE_MGM/db_test.db")
        self.setWindowTitle("Iniciar sesión")
        self.cargar_usuarios()
        self.line_password.returnPressed.connect(self.iniciar_sesion)
        self.button_login.clicked.connect(self.iniciar_sesion)
        self.button_salir.clicked.connect(self.close)
        self.line_password.setEchoMode(2)

    def cargar_usuarios(self):
        usuarios = self.claseSQLite.obtener_usuarios()
        for usuario in usuarios:
            self.combo_user.addItem(usuario[0])
        self.combo_user.setCurrentIndex(-1)

    def iniciar_sesion(self):
        usuario = self.combo_user.currentText()
        contrasena = self.line_password.text()
        if self.claseSQLite.buscar_usuario(usuario):
            if self.claseSQLite.buscar_usuario(usuario)[1] == contrasena:
                self.close()
                self.main = UI(usuario)
                self.main.show()
            else:
                self.label_error.setText("Usuario o contraseña incorrecta.")
        else:
            self.label_error.setText("Usuario o contraseña incorrecta.")

# Iniciar aplicación PyQt
app = QApplication(sys.argv)

main = LOGIN()
main.show()

sys.exit(app.exec())