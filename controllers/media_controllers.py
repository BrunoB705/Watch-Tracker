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
from PySide6.QtWidgets import QHeaderView,QSizePolicy,QTimeEdit,QComboBox,QFormLayout,QDialog,QAbstractItemView,QApplication, QPushButton, QWidget, QVBoxLayout,QLineEdit,QTableWidgetItem,QTableWidget,QLabel,QHBoxLayout,QTabWidget,QMessageBox

class MediaController:

    def seconds_to_hhmm(self,seconds:int) ->str:
        hours = seconds//3600
        minutes = (seconds%3600)//60
        result = f"{hours:02d}:{minutes:02d}"
        return result
    
    def hhmm_to_seconds(self,time:str) ->int:
        hours,minutes = map(int,time.split(":"))
        result = hours*3600+minutes*60
        return result
    def add(self,data):
        seconds = self.hhmm_to_seconds(data["time"])
        if data["status"].lower() == "completed":
            seconds = 0
        add_media(title=data["title"],url=data["url"],
                  seconds=seconds,status=data["status"].lower())
    
    def edit(self,id,data):
        seconds = self.hhmm_to_seconds(data["time"])
        if data["status"].lower() == "completed": #Todo media completo tiene hora 00:00
            seconds = 0
        edit_media(id=id,title=data["title"],
                   seconds=seconds,url=data["url"],status=data["status"].lower())
    
    def delete(self,id):
        delete_media(id)

    def get_for_edit(self,id):
        media_data = get_media_by_id(id)
        return{
            "title" :media_data["title"],
            "url": media_data["url"],
            "time": self.seconds_to_hhmm(media_data["current_seconds"]),
            "status": media_data["status"]
        }
    
    def format_list(self,media_list):
        formatted = []

        for media in media_list:
            formatted.append([str(media[0]),#id
                              str(media[1]),#title
                              media[2],#url
                              self.seconds_to_hhmm(media[3]), #current_seconds
                              str(media[4]).capitalize()]) #status
        return formatted
    def controller_get_all(self, order="ASC"):#ASC por default
        return self.format_list(get_all_media(order_by="id",order=order))
    
    def controller_get_pending(self, order="ASC"):#ASC por default
        return self.format_list(get_pending(order_by="id",order=order))
    
    def controller_get_completed(self, order="ASC"):#ASC por default
        return self.format_list(get_completed(order_by="id",order=order))
    