from database.connection import get_connection
from database.models import Media
from typing import List

"""
1. get_pending
2. get_completed
3. delete_media
4. add_media
5. mark_completed
6. update_minute
7. edit_media
8. get_media_by_id
9. get_all_media
10. get_media_count
"""

MEDIA_COLUMNS = {"updated_at","created_at","title", "status", "url", "time_watched","id"}

def _row_to_media(row) -> Media:
    """Convierte una fila de sqlite3.Row a objeto Media"""
    return Media(
        id=row["id"],
        title=row["title"],
        url=row["url"],
        current_seconds=row["current_seconds"],
        status=row["status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"]
    )

def add_media(media: Media) -> int:
    """Agrega un nuevo media a la BD. Retorna el ID generado."""
    if not media.title.strip():
        raise ValueError("El título del video no puede ser vacío")
    if not media.url.strip():
        raise ValueError("La URL del video no puede ser vacía")
    if media.current_seconds < 0:
        raise ValueError("Los minutos no pueden ser negativos")

    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO media (title, url, current_seconds, status) VALUES (?, ?, ?, ?)""",
            (media.title.strip(), media.url.strip(), media.current_seconds, media.status.strip())
        )

    return cursor.lastrowid


def get_pending(order_by="updated_at", order="ASC") -> List[Media]:
    """Retorna lista de videos pendientes como objetos Media"""
    if order_by not in MEDIA_COLUMNS:
        order_by = "updated_at"

    order = order.upper()
    if order not in {"ASC", "DESC"}:
        order = "ASC"
    with get_connection() as conn:
        cursor = conn.execute(f"""
            SELECT * FROM media 
            WHERE status = 'pending'
            ORDER BY {order_by} {order}""")
        pending_videos = cursor.fetchall()
    return [_row_to_media(row) for row in pending_videos]

def get_completed(order_by="updated_at", order="ASC") -> List[Media]:
    """Retorna lista de videos completados como objetos Media"""
    if order_by not in MEDIA_COLUMNS:
        order_by = "updated_at"

    order = order.upper()
    if order not in {"ASC", "DESC"}:
        order = "ASC"

    with get_connection() as conn:
        cursor = conn.execute(f"""
            SELECT * FROM media
            WHERE status = 'completed'
            ORDER BY {order_by} {order}""")
        completed_videos = cursor.fetchall()
    return [_row_to_media(row) for row in completed_videos]

def delete_media(id:int):
    if id<=0:
        raise ValueError("ID de video erroneo")
    
    with get_connection() as conn:
        cursor = conn.execute("""
            DELETE FROM media 
            WHERE id = ?""",
            (id,))
        if cursor.rowcount == 0:#ROWCOUNT DEVUELVE CUANTAS FILAS FUERON CAMBIADAS DURANTE EL DELETE
            raise ValueError("No se pudo borrar el video")
    return

def mark_completed(id:int):
    if id<=0:
        raise ValueError("ID de video erroneo")
    
    with get_connection() as conn:
        cursor = conn.execute("""
            UPDATE media 
            SET status = 'completed',
            updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?""",
            (id,))
        if cursor.rowcount == 0:#ROWCOUNT DEVUELVE CUANTAS FILAS FUERON CAMBIADAS DURANTE EL UPDATE
            raise ValueError("No se pudo marcar como completo el video, ID no existe")
    return

def update_current_seconds(seconds:int, id:int):
    if id< 0:
        raise ValueError("ID de video erroneo")
    if seconds <0:
        raise ValueError("Los minutos no pueden ser negativos")
    with get_connection() as conn:
        cursor = conn.execute("""
            UPDATE media
            SET current_seconds  = ?,updated_at = CURRENT_TIMESTAMP
            WHERE id = ?""",
            (seconds,id))
        if cursor.rowcount == 0:#ROWCOUNT DEVUELVE CUANTAS FILAS FUERON CAMBIADAS DURANTE EL UPDATE
            raise ValueError("No se pudo actualizar el minuto del video, ID no existe")
    return

def get_media_by_id(id: int) -> Media:
    """Retorna un video como objeto Media"""
    if id <= 0:
        raise ValueError("ID invalido")
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT * FROM media
            WHERE id = ?""",
            (id,))
        media = cursor.fetchone()
    if media is None:
        raise ValueError("No se encontro el video con ese ID")
    return _row_to_media(media)

def edit_media(media: Media) -> None:
    """Edita un video existente. El media debe tener id asignado"""
    if media.id is None or media.id <= 0:
        raise ValueError("ID invalido")
    if not media.title.strip():
        raise ValueError("El titulo no puede ser vacio")
    if not media.url.strip():
        raise ValueError("El url no puede ser vacio")
    
    with get_connection() as conn:
        cursor = conn.execute("""
            UPDATE media
            SET title = ?, url = ?, current_seconds = ?, status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?""",
            (media.title.strip(), media.url.strip(), media.current_seconds, media.status, media.id))
        
        if cursor.rowcount == 0:
            raise ValueError("No se pudo editar el video, el ID no existe")        

def get_all_media(order_by="id", order="ASC") -> List[Media]:
    """Retorna lista de todos los videos como objetos Media"""
    if order_by not in MEDIA_COLUMNS:
        order_by = "id"
    if order not in {"ASC", "DESC"}:
        order = "ASC"
    with get_connection() as conn:
        cursor = conn.execute(f"""
            SELECT * FROM media
            ORDER BY {order_by} {order}""")
        all_media = cursor.fetchall()
        return [_row_to_media(row) for row in all_media]
    
def get_media_count():
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT COUNT(*) FROM media""")
        resultado = cursor.fetchone()[0]
    return resultado

def get_completed_media_count():
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT COUNT(*) FROM media
            WHERE status = 'completed'""")
        resultado = cursor.fetchone()[0]
    return resultado

def get_pending_media_count():
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT COUNT(*) FROM media
            WHERE status = 'pending'""")
        resultado = cursor.fetchone()[0]
    return resultado