import sys
from PySide6.QtWidgets import QMainWindow,QHeaderView,QSizePolicy,QTimeEdit,QComboBox,QFormLayout,QDialog,QAbstractItemView,QApplication, QPushButton, QWidget, QVBoxLayout,QLineEdit,QTableWidgetItem,QTableWidget,QLabel,QHBoxLayout,QTabWidget,QMessageBox
from services.media_player import add_media,get_all_media,delete_media,get_media_count

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

        self.All_tab = QWidget()
        self.pending_tab = QWidget()
        self.completed_tab = QWidget()

        #LAYOUT 3 TABS
        self.All_tab_layout = QVBoxLayout()
        self.All_tab.setLayout(self.All_tab_layout)

        self.pending_tab.setLayout(QVBoxLayout())
        self.completed_tab.setLayout(QVBoxLayout())

        #ADD TABS
        self.tabs.addTab(self.All_tab, "All")
        self.tabs.addTab(self.pending_tab, "Pending")
        self.tabs.addTab(self.completed_tab, "Completed")

        #TABLE
        self.table = QTableWidget()
        self.crearTabla()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.All_tab_layout.addWidget(self.table,stretch=1)        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #LAYOUT BUTTONS
        self.button_layout = QHBoxLayout()
        self.All_tab_layout.addLayout(self.button_layout)

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
        #self.edit_button.clicked.connect(self.editar_item)
        self.edit_button.clicked.connect(self.cargar_tabla_desde_bd)

        self.cantidad_items = QLabel("Cantidad: ")
        self.All_tab_layout.addWidget(self.cantidad_items)
        self.actualizar_cantidad()


        self.cargar_tabla_desde_bd()

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
        self.cantidad_items.setText(f"Cantidad: {get_media_count()}")
    
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
        table_selected_item = self.table.selectedItems()
        if not table_selected_item:
                return
        row = table_selected_item[0].row() #Obtengo fila
        id_item = int(self.table.item(row,0).text()) #Obtengo el ID de la fila
        delete_media(id_item)
        self.table.removeRow(row)
        self.actualizar_cantidad()
        self.cargar_tabla_desde_bd
        self.actualizar_cantidad()
    

    def crearTabla(self):
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID","Titulo","URL","Hora:Minuto","Estado"])
        self.table.setColumnHidden(0, True)  # Oculta la primera columna (ID)
        self.table.resizeColumnsToContents()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        

    def cargar_tabla_desde_bd(self):
        #Limpio tabla
        self.table.setRowCount(0)

        all_media = get_all_media()

        for data in all_media:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col,value in enumerate(data):
                if col == 3:#Columna de current_seconds
                    horas = value//3600
                    minutos = (value %3600) //60
                    value = f"{horas:02d}:{minutos:02d}" 
                else:
                    value = str(value).capitalize()
                self.table.setItem(row,col,QTableWidgetItem(value))

def run_app():
    app = QApplication()
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())