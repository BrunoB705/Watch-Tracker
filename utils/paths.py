import sys
import os


APP_NAME = "WatchTracker"

# -------------------------
# BASE DIRS
# -------------------------

def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.abspath(".")

def get_data_dir():
    path = os.path.join(os.environ["LOCALAPPDATA"], APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path

# -------------------------
# RECURSOS (solo lectura)
# -------------------------

def resource_path(relative_path):
    return os.path.join(get_base_path(), relative_path)

def get_icon(name):
    return resource_path(f"ui/icons/{name}")

def get_style(name):
    return resource_path(f"ui/styles/{name}.qss")

# -------------------------
# DATOS (persistentes)
# -------------------------

def get_db_path():
    return os.path.join(get_data_dir(), "media.db")