import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QMessageBox, QTreeWidgetItem
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import QDate, QPoint, Qt
from PyQt5 import uic
from lib.sql import SQLite

class PRUEBA_CHECK(QMainWindow):
    def __init__(self, parent=None):
        super(PRUEBA_CHECK, self).__init__(parent)
        uic.loadUi("test\prueba_tree_checkbox.ui", self)  # Cargar la interfaz de Qt Designer
        
        
        self.claseSQLite = SQLite(r"C:\Users\tomas\Desktop\software_mg\db.db")

        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels(["Encargados"])
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.setAlternatingRowColors(True)
        # self.treeWidget.setCheckable(True)
        
        usuarios = self.claseSQLite.buscar_usuario_sector("syg")
        for usuario in usuarios:
            item = QTreeWidgetItem(self.treeWidget, [usuario[0]])
            item.setCheckState(0, Qt.Checked)
            
        # Connect the item selection signal to a slot
        self.treeWidget.itemClicked.connect(self.on_item_clicked)
        
    def on_item_clicked(self, item, column):
        # Print the text of the selected item
        print({item.checkState(0)})

        
# Iniciar aplicación PyQt
app = QApplication(sys.argv)

main = PRUEBA_CHECK()
main.show()

sys.exit(app.exec())
