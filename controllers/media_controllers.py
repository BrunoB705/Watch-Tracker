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
from database.models import Media
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
    
    def add(self, data):
        """Agrega un nuevo media desde datos del dialog"""
        seconds = self.hhmm_to_seconds(data["time"])
        if data["status"].lower() == "completed":
            seconds = 0
        media = Media(
            title=data["title"],
            url=data["url"],
            current_seconds=seconds,
            status=data["status"].lower()
        )
        add_media(media)
    
    def edit(self, id, data):
        """Edita un media existente desde datos del dialog"""
        seconds = self.hhmm_to_seconds(data["time"])
        if data["status"].lower() == "completed":
            seconds = 0
        media = Media(
            id=id,
            title=data["title"],
            url=data["url"],
            current_seconds=seconds,
            status=data["status"].lower()
        )
        edit_media(media)
    
    def delete(self, id):
        delete_media(id)

    def get_for_edit(self, id):
        """Obtiene datos de un media para editarlo"""
        media = get_media_by_id(id)
        return {
            "title": media.title,
            "url": media.url,
            "time": self.seconds_to_hhmm(media.current_seconds),
            "status": media.status
        }
    
    def format_list(self, media_list):
        """Convierte lista de Media a formato para mostrar en tabla"""
        formatted = []
        for media in media_list:
            formatted.append([
                str(media.id),
                str(media.title),
                media.url,
                self.seconds_to_hhmm(media.current_seconds),
                str(media.status).capitalize()
            ])
        return formatted
    
    def controller_get_all(self, order="ASC"):
        return self.format_list(get_all_media(order_by="id", order=order))
    
    def controller_get_pending(self, order="ASC"):
        return self.format_list(get_pending(order_by="id", order=order))
    
    def controller_get_completed(self, order="ASC"):
        return self.format_list(get_completed(order_by="id", order=order))
    