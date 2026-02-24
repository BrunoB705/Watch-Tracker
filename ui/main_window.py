import sys
from PySide6.QtWidgets import QHeaderView,QSizePolicy,QTimeEdit,QComboBox,QFormLayout,QDialog,QAbstractItemView,QApplication, QPushButton, QWidget, QVBoxLayout,QLineEdit,QTableWidgetItem,QTableWidget,QLabel,QHBoxLayout,QTabWidget,QMessageBox
from services.media_player import add_media,get_all_media,delete_media,get_media_count,get_completed,get_pending,get_pending_media_count,get_completed_media_count

class AddMediaDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Video")
        self.add_media_main_layout = QVBoxLayout()
        self.setLayout(self.add_media_main_layout)

        self.form_layout = QFormLayout()
        self.add_media_main_layout.addLayout(self.form_layout)

        #INPUTS
        self.title_input = QLineEdit()
        self.url_input = QLineEdit()
        self.time_input = QTimeEdit()
        self.status_input = QComboBox()
        self.status_input.addItems(["Pending","Completed"])
        

        self.form_layout.addRow("Titulo: ",self.title_input)
        self.form_layout.addRow("URL: ",self.url_input)
        self.form_layout.addRow("Hora/Minuto: ",self.time_input)
        self.form_layout.addRow("Estado: ",self.status_input)


        #LAYOUT BUTTONS
        self.button_layout = QHBoxLayout()
        self.add_media_main_layout.addLayout(self.button_layout)
        #BUTTONS SAVE & CANCEL
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_data)
        self.button_layout.addWidget(self.save_button)
        
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)



    def save_data(self):
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Error","El titulo no es correcto")
            return
        if not self.url_input.text().strip():
            QMessageBox.warning(self,"Error","El URL no es correcto")
            return
        self.accept()
    def obtener_data(self):
        return{
            "title": self.title_input.text().strip(),
            "url": self.url_input.text().strip(),
            "time": self.time_input.time().toString("HH:mm"),
            "status": self.status_input.currentText()
        }

    


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        #MAIN LAYOUT
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.setFixedSize(1200, 400)  # ancho,alto

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
        self.remove_button.clicked.connect(self.borrar_item)
        self.edit_button.clicked.connect(self.cargar_tabla_desde_bd)



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

        self.actualizar_cantidad()


    def editar_item(self):
        text = self.line_edit.text()
        selected_item = self.lista.currentItem()
        if text and selected_item:
            selected_item.setText(f"{text}")
            print("ENTRO")
        else:
            error_msg = QMessageBox()
            error_msg.setText("Error al editar el item")
            error_msg.exec()

    def actualizar_cantidad(self):
        self.total_elements["All"].setText(f"Cantidad: {get_media_count()}")
        self.total_elements["Completed"].setText(f"Cantidad: {get_completed_media_count()}")
        self.total_elements["Pending"].setText(f"Cantidad: {get_pending_media_count()}")
    
    def agregar_item(self):
        self.add_media_dialog = AddMediaDialog(self)
        if self.add_media_dialog.exec():
            data = self.add_media_dialog.obtener_data()
            horas,minutos = map(int,data['time'].split(":"))
            segundos_totales = horas*3600 + minutos*60

            try:
                add_media(title=data['title'],url=data['url'],seconds=segundos_totales,status=data['status'].lower())
            except ValueError as e:
                QMessageBox.warning(self,"Error",str(e))
                return
        self.cargar_tabla_desde_bd()
        self.actualizar_cantidad()



    def borrar_item(self):
        current_tab = self.tabs.currentWidget()
        if current_tab == self.all_tab:
            table = self.all_table
        elif current_tab == self.pending_tab:
            table = self.pending_table
        else:
            table = self.completed_table
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
        self.cargar_tabla_desde_bd()
        self.actualizar_cantidad()
    

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
                        horas = value//3600
                        minutos = (value %3600) //60
                        value = f"{horas:02d}:{minutos:02d}" 
                    else:
                        value = str(value).capitalize()
                    table.setItem(row,col,QTableWidgetItem(value))


def run_app():
    app = QApplication()
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())