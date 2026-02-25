import sys
from PySide6.QtWidgets import QHeaderView,QSizePolicy,QTimeEdit,QComboBox,QFormLayout,QDialog,QAbstractItemView,QApplication, QPushButton, QWidget, QVBoxLayout,QLineEdit,QTableWidgetItem,QTableWidget,QLabel,QHBoxLayout,QTabWidget,QMessageBox
from services.media_player import (
    add_media,
    get_all_media,
    delete_media,
    get_media_count,
    get_completed,
    get_pending,
    get_pending_media_count,
    get_completed_media_count,
    get_media_by_id,
    edit_media
)
from ui.dialogs import MediaDialog

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        #MAIN LAYOUT
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.setFixedSize(1200, 400)  # ancho,alto
        self.setWindowTitle("Watch Tracker")
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
        self.all_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.all_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.pending_table = QTableWidget()
        self.pending_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pending_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.completed_table = QTableWidget()
        self.completed_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.completed_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #TAB TABLE MAP
        self.tab_table_map = {
            self.all_tab: self.all_table,
            self.pending_tab: self.pending_table,
            self.completed_tab: self.completed_table
        }
        #CREACION Y CARGA TABLA
        self.crearTabla()
        self.cargar_tabla_desde_bd()

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

        self.refhresh_ui()

    def edit_item(self):
        table = self.get_current_table()
        table_selected_item = table.selectedItems()
        if not table_selected_item:#Verificacion de si esta algo seleccionado
            return
        row = table_selected_item[0].row() #Obtengo fila
        id_item = int(table.item(row,0).text()) #Obtengo el ID de la fila
        try :
            media_data = get_media_by_id(id_item)
        except ValueError as e:
            self.show_error(self,e)
            return
        media = {
            "title": media_data["title"],
            "url": media_data["url"],
            "time": f"{media_data[3]//3600:02d}:{(media_data["current_seconds"]%3600)//60:02d}", #current_seconds a HH:MM
            "status": media_data["status"]
        }

        self.edit_media_dialog = MediaDialog(parent=self,media_data=media)
        if self.edit_media_dialog.exec():
            data = self.edit_media_dialog.obtener_data()
            segundos_totales = self.hhmm_to_seconds(data["time"])
            try:
                edit_media(title=data['title'],url=data['url'],seconds=segundos_totales,status=data['status'].lower(),id=id_item)
            except ValueError as e:
                self.show_error(self,e)
                return
        self.refhresh_ui()
        


    def actualizar_cantidad_elementos(self):
        self.total_elements["All"].setText(f"Cantidad: {get_media_count()}")
        self.total_elements["Completed"].setText(f"Cantidad: {get_completed_media_count()}")
        self.total_elements["Pending"].setText(f"Cantidad: {get_pending_media_count()}")
    
    def agregar_item(self):
        self.add_media_dialog = MediaDialog(parent=self)
        if self.add_media_dialog.exec():
            data = self.add_media_dialog.obtener_data()
            segundos_totales = self.hhmm_to_seconds(data["time"])
            try:
                add_media(title=data['title'],url=data['url'],seconds=segundos_totales,status=data['status'].lower())
            except ValueError as e:
                self.show_error(self,e)
                return
        self.refhresh_ui()



    def delete_item(self):
        table = self.get_current_table()
        table_selected_item = table.selectedItems()
        if not table_selected_item:#Verificacion de si esta algo seleccionado
                return
        delete_confirmation = QMessageBox.question(
                                    self,
                                    "Borrar media",
                                    "Estas seguro querer borrar?",
                                    QMessageBox.Cancel | QMessageBox.Ok)
        if delete_confirmation != QMessageBox.Ok:
            return
        row = table_selected_item[0].row() #Obtengo fila
        id_item = int(table.item(row,0).text()) #Obtengo el ID de la fila

        delete_media(id_item)
        self.refhresh_ui()
    

    def crearTabla(self):
        tables = [self.all_table,self.pending_table,self.completed_table]
        for table in tables:
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["ID","Titulo","URL","Hora:Minuto","Estado"])
            table.setColumnHidden(0, True)  # Oculta la primera columna (ID)
            table.resizeColumnsToContents()
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        

    def cargar_tabla_desde_bd(self):
        tables_data = [(self.all_table,get_all_media()),
                       (self.pending_table,get_pending()),
                       (self.completed_table,get_completed())]
        
        for table,media_list in tables_data:
            table.setRowCount(0)#LIMPIA TABLA
            for data in media_list:
                row = table.rowCount()
                table.insertRow(row)
                for col,value in enumerate(data):
                    if col == 3:#Columna de current_seconds
                        value = self.seconds_to_hhmm(value)
                    else:
                        value = str(value).capitalize()
                    table.setItem(row,col,QTableWidgetItem(value))
                    
    def get_current_table(self):
        return self.tab_table_map[self.tabs.currentWidget()]
    
    def seconds_to_hhmm(self,seconds:int) ->str:
        hours = seconds//3600
        minutes = (seconds%3600)//60
        result = f"{hours:02d}:{minutes:02d}"
        return result
    
    def hhmm_to_seconds(self,time:str) ->int:
        hours,minutes = map(int,time.split(":"))
        result = hours*3600+minutes*60
        return result

    def refhresh_ui(self):
        self.cargar_tabla_desde_bd()
        self.actualizar_cantidad_elementos()

    def show_error(self,message:str):
        QMessageBox.warning(self,"Error",message)

def run_app():
    app = QApplication()
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())