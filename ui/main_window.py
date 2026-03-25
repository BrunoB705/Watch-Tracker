import sys
from pathlib import Path
from PySide6.QtWidgets import QHeaderView,QSizePolicy,QTimeEdit,QComboBox,QFormLayout,QDialog,QAbstractItemView,QApplication, QPushButton, QWidget, QVBoxLayout,QLineEdit,QTableWidgetItem,QTableWidget,QLabel,QHBoxLayout,QTabWidget,QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication, QIcon
from services.media_player import (
    get_all_media,
    get_media_count,
    get_completed,
    get_pending,
    get_pending_media_count,
    get_completed_media_count,
)
from ui.dialogs import MediaDialog
from controllers.media_controllers import MediaController
from utils.paths import resource_path
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.current_theme = "light"
        self.theme_manager = ThemeManager(window=self)
        self.theme_manager.load_theme()
        self.controller = MediaController()


        #MAIN LAYOUT
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(5, 0, 5, 5)    
        self.setFixedSize(1200, 400)  # ancho,alto
        self.setWindowTitle("Watch Tracker")

        # HABILITAR DARK THEME
        self.theme_button = QPushButton("")
        self.theme_button.setObjectName("themeButton")
        self.theme_button.clicked.connect(self.theme_manager.toggle)
        self.theme_layout = QHBoxLayout()
        self.theme_layout.setContentsMargins(0, 10, 0, 0)
        self.theme_layout.setSpacing(0)

        self.theme_button.setIcon(QIcon(resource_path("ui/nightmode.png")))

        self.theme_layout.addStretch()
        self.theme_layout.addWidget(self.theme_button)
        self.main_layout.addLayout(self.theme_layout)

        #ORDER BY
        self.order_by = QComboBox()
        self.order_by.addItems(["Más Antiguo","Más Reciente"])
        self.order_by.currentIndexChanged.connect(self.refresh_ui)

        self.order_by_layout = QHBoxLayout()
        self.order_by_layout.setContentsMargins(0, 0, 0, 0)
        self.order_by_layout.addStretch()
        self.order_by_label = QLabel("Ordenar por:")
        self.order_by_label.setObjectName("orderByLabel")
        self.order_by_layout.addWidget(self.order_by_label)
        self.order_by_layout.addWidget(self.order_by)

        self.main_layout.addLayout(self.order_by_layout)
        

        

        #TABS
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        self.all_tab = QWidget()
        self.pending_tab = QWidget()
        self.completed_tab = QWidget()

        #LAYOUT 3 TABS
        self.all_tab_layout = QVBoxLayout()
        self.all_tab.setLayout(self.all_tab_layout)

        self.pending_tab_layout = QVBoxLayout()
        self.pending_tab.setLayout(self.pending_tab_layout)

        self.completed_tab_layout = QVBoxLayout()
        self.completed_tab.setLayout(self.completed_tab_layout)

        #ADD TABS
        self.tabs.addTab(self.all_tab, "All")
        self.tabs.addTab(self.pending_tab, "Pending")
        self.tabs.addTab(self.completed_tab, "Completed")

        #TABLAS
        self.all_table = QTableWidget()
        self.pending_table = QTableWidget()
        self.completed_table = QTableWidget()
        self.table_methods()

        #TAB TABLE MAP
        self.tab_table_map = {
            self.all_tab: self.all_table,
            self.pending_tab: self.pending_table,
            self.completed_tab: self.completed_table
        }
        self.crearTabla()

        #LAYOUT TABLAS
        self.all_tab_layout.addWidget(self.all_table,stretch=1)        
        self.pending_tab_layout.addWidget(self.pending_table,stretch=1)
        self.completed_tab_layout.addWidget(self.completed_table,stretch=1)

        #LAYOUT BUTTONS
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        #BUTTONS
        self.print_button = QPushButton("Agregar")
        self.button_layout.addWidget(self.print_button)

        self.remove_button = QPushButton("Borrar")
        self.button_layout.addWidget(self.remove_button)

        self.edit_button = QPushButton("Edit")
        self.button_layout.addWidget(self.edit_button)
        
        #CLICKED BUTTONS
        self.print_button.clicked.connect(self.agregar_item)
        self.remove_button.clicked.connect(self.delete_item)
        self.edit_button.clicked.connect(self.edit_item)


        #CANTIDAD ELEMENTOS
        self.total_elements = {}

        tabs_info = [
            (self.all_tab_layout,"All"),
            (self.pending_tab_layout,"Pending"),
            (self.completed_tab_layout,"Completed")
        ]
        for layouts,key in tabs_info:
            self.count_layout = QHBoxLayout()
            self.count_label = QLabel("Cantidad: 0")
            self.count_layout.addWidget(self.count_label)
            layouts.addLayout(self.count_layout)
            self.total_elements[key] = self.count_label

        self.refresh_ui()

    def edit_item(self):
        table = self.get_current_table()
        selected_item = table.selectedItems()
        if not selected_item:#Verificacion de si esta algo seleccionado
            return
        row = selected_item[0].row() #Obtengo fila
        media_id = int(table.item(row,0).text()) #Obtengo el ID de la fila
        try :
            media = self.controller.get_for_edit(media_id)
        except ValueError as e:
            self.show_error(e)
            return
        
        edit_dialog = MediaDialog(parent=self,media_data=media)
        if edit_dialog.exec():
            data = edit_dialog.obtener_data()
            try:
                self.controller.edit(media_id,data)
            except ValueError as e:
                self.show_error(e)
                return
        self.refresh_ui()
        
    def table_methods(self):
        tables = [self.all_table,self.pending_table,self.completed_table]
        for table in tables:
            table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.verticalHeader().setVisible(False)

            try:
                table.cellDoubleClicked.disconnect()
            except TypeError:
                pass
            table.cellDoubleClicked.connect(self.copy_column_on_double_click)

    def copy_column_on_double_click(self,row,column):
        url_column = 2
        if column != url_column:
            return
        table = self.sender() #Obtiene tabla que emite señal
        item = table.item(row,column)
        if item:
            QGuiApplication.clipboard().setText(item.text())

    def actualizar_cantidad_elementos(self):
        self.total_elements["All"].setText(f"Cantidad: {get_media_count()}")
        self.total_elements["Completed"].setText(f"Cantidad: {get_completed_media_count()}")
        self.total_elements["Pending"].setText(f"Cantidad: {get_pending_media_count()}")
    
    def agregar_item(self):
        dialog = MediaDialog(parent=self)
        if dialog.exec():
            data = dialog.obtener_data()
            try:
                self.controller.add(data)
            except ValueError as e:
                self.show_error(e)
                return
        self.refresh_ui()

    def delete_item(self):
        table = self.get_current_table()
        selected_item = table.selectedItems()
        row = selected_item[0].row() #Obtengo fila
        selected_item_title = table.item(row,1).text()#Obtengo titulo para mensaje de confirmacion
        if not selected_item:#Verificacion de si esta algo seleccionado
                return
        if not self.confirm_delete(selected_item_title):
            return
        media_id = int(table.item(row,0).text()) #Obtengo el ID de la fila
        self.controller.delete(media_id)
        self.refresh_ui()
    

    def crearTabla(self):
        tables = [self.all_table,self.pending_table,self.completed_table]
        for table in tables:
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["ID","Titulo","URL","Hora:Minuto","Estado"])
            table.setColumnHidden(0, True)  # Oculta la primera columna (ID)
            table.resizeColumnsToContents()
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        

    def cargar_tabla_desde_bd(self):
        if self.order_by.currentText() == "Más Antiguo":
            order = "ASC"
        else: 
            order = "DESC"
        tables_data = [(self.all_table,self.controller.controller_get_all(order=order)),
                       (self.pending_table,self.controller.controller_get_pending(order=order)),
                       (self.completed_table,self.controller.controller_get_completed(order=order))
                       ]
        for table,media_list in tables_data:
            table.setRowCount(0)#LIMPIA TABLA

            for data in media_list:
                row_index = table.rowCount()
                table.insertRow(row_index)

                for col,value in enumerate(data):
                    table.setItem(row_index,col,QTableWidgetItem(value))

    def get_current_table(self):
        return self.tab_table_map[self.tabs.currentWidget()]
    

    def refresh_ui(self):
        self.cargar_tabla_desde_bd()
        self.actualizar_cantidad_elementos()

    def show_error(self,message:str):
        QMessageBox.warning(self,"Error",message)

    def confirm_delete(self,title)->bool:
        return QMessageBox.question(self,"Borrar media",f"Estas seguro querer borrar {title}?",
                                    QMessageBox.Cancel |QMessageBox.Ok)==QMessageBox.Ok

from utils.paths import resource_path
class ThemeManager:
    def __init__(self,window):
        self.window = window
        self.current_theme = "light"

    def load_theme(self):
        path = resource_path(f"ui/styles/{self.current_theme}.qss")
        with open(path, "r", encoding="utf-8") as f:
            self.window.setStyleSheet(f.read())
    
    def toggle(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.load_theme()

def run_window():
    app = QApplication()
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())