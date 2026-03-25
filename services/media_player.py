from database.connection import get_connection
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

def add_media(title: str, url: str, seconds: int = 0, status: str = "pending")->int:
    if not title.strip():
        raise ValueError("El título del video no puede ser vacío")
    if not url.strip():
        raise ValueError("La URL del video no puede ser vacía")
    if seconds<0:
        raise ValueError("Los minutos no pueden ser negativos")

    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO media (title, url, current_seconds,status) VALUES (?,?,?,?)""",
            (title.strip(),url.strip(),seconds,status.strip())
        )

    return cursor.lastrowid


def get_pending(order_by="updated_at",order="ASC"):
    if order_by not in MEDIA_COLUMNS:
        order_by = "updated_at"

    order = order.upper()
    if order not in {"ASC","DESC"}:
        order = "ASC"
    with get_connection() as conn:
        cursor = conn.execute(f"""
            SELECT * FROM media 
            WHERE status  = 'pending'
            ORDER BY {order_by} {order}""")
        pending_videos = cursor.fetchall()
    return pending_videos

def get_completed(order_by="updated_at",order="ASC"):
    if order_by not in MEDIA_COLUMNS:
        order_by = "updated_at"

    order = order.upper()
    if order not in {"ASC","DESC"}:
        order = "ASC"

    with get_connection() as conn:
        cursor = conn.execute(f"""
            SELECT * FROM media
            WHERE status = 'completed'
            ORDER BY {order_by} {order}""")
        completed_videos = cursor.fetchall()
    return completed_videos

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

def get_media_by_id(id:int):
    if id<=0:
        raise ValueError("ID invalido")
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT * FROM media
            WHERE id = ?""",
            (id,))
        media = cursor.fetchone()
    if media is None:
        raise ValueError("No se encontro el video con ese ID")
    return media

def edit_media(title:str, url:str,seconds:int,status:str, id:int):
    if id<=0:
        raise ValueError("ID invalido")
    if not title.strip():
        raise ValueError("El titulo no puede ser vacio")
    if not url.strip():
        raise ValueError("El url no puede ser vacio")
    
    with get_connection() as conn:
        cursor = conn.execute("""
            UPDATE media
            SET title = ?,url = ?,current_seconds = ?,status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?""",
            (title.strip(),url.strip(),seconds,status,id))
        
        if cursor.rowcount == 0:#ROWCOUNT DEVUELVE CUANTAS FILAS FUERON CAMBIADAS DURANTE EL UPDATE
            raise ValueError("No se pudo editar el video, el ID no existe")
    return        

def get_all_media(order_by="id",order="ASC"): #Por default ordena por id de forma ascendente
    if order_by not in MEDIA_COLUMNS:
        order_by = "id"
    if order not in {"ASC","DESC"}:
        order = "ASC"
    with get_connection() as conn:
        cursor = conn.execute(f"""
            SELECT * FROM media
            ORDER BY {order_by} {order}""")
        all_media = cursor.fetchall()
        return all_media
    
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