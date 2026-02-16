import sqlite3
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "data" / "media.db"

def get_connection():

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row


    return conn


def init_db():
    
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS media (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        url TEXT NOT NULL,
                        current_seconds INTEGER DEFAULT 0,
                        status TEXT NOT NULL DEFAULT 'pending'
                        CHECK(status IN('pending','completed')),
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TRIGGER IF NOT EXISTS update_media_timestamp
            AFTER UPDATE ON media
            BEGIN
                UPDATE media
                SET updated_at = CURRENT_TIMESTAMP
                WHERE id = NEW.id;
            END;

        """)

init_db()