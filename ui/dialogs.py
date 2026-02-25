from PySide6.QtWidgets import QTimeEdit,QComboBox,QFormLayout,QDialog, QPushButton, QVBoxLayout,QLineEdit,QHBoxLayout,QMessageBox
class MediaDialog(QDialog):
    def __init__(self, media_data=None, parent=None):
        super().__init__(parent)
        self.media_data = media_data
        self.edit_data = media_data is not None
        self.resize(500,100)

        self.setWindowTitle("Agregar/Editar Media")
        self.dialog_main_layout = QVBoxLayout()
        self.setLayout(self.dialog_main_layout)

        #INPUTS
        self.title_input = QLineEdit()
        self.url_input = QLineEdit()
        self.time_input = QTimeEdit()
        self.status_input = QComboBox()
        self.status_input.addItems(["Pending","Completed"])
        
        #FORM LAYOUT
        self.form_layout = QFormLayout()
        self.dialog_main_layout.addLayout(self.form_layout)

        self.form_layout.addRow("Titulo: ",self.title_input)
        self.form_layout.addRow("URL: ",self.url_input)
        self.form_layout.addRow("Hora/Minuto: ",self.time_input)
        self.form_layout.addRow("Estado: ",self.status_input)

        #LAYOUT BUTTONS
        self.button_layout = QHBoxLayout()
        self.dialog_main_layout.addLayout(self.button_layout)

        #BUTTONS SAVE & CANCEL
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_data)
        self.button_layout.addWidget(self.save_button)
    
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)

        #EDIT MODE CHECK
        if self.edit_data:
            self.load_data()


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
    
    def load_data(self):
        self.title_input.setText(self.media_data["title"])
        self.url_input.setText(self.media_data["url"])
        horas, minutos = map(int, self.media_data["time"].split(":"))
        self.time_input.setTime(self.time_input.time().fromString(
            f"{horas:02d}:{minutos:02d}", "HH:mm"
        ))
        self.status_input.setCurrentText(self.media_data["status"].capitalize())
