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
"""

def add_media(title: str, url: str, seconds: int = 0)->int:
    if not title.strip():
        raise ValueError("El título del video no puede ser vacío")
    if not url.strip():
        raise ValueError("La URL del video no puede ser vacía")
    if seconds<0:
        raise ValueError("Los minutos no pueden ser negativos")

    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO media (title, url, current_seconds) VALUES (?,?,?)""",
            (title.strip(),url.strip(),seconds)
        )

    return cursor.lastrowid


def get_pending():
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT * FROM media 
            WHERE status  = 'pending'
            ORDER BY created_at ASC""")#VA A MOSTRAR EL PRIMER CREADO
        pending_videos = cursor.fetchall()
    return pending_videos

def get_completed():
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT * FROM media
            WHERE status = 'completed'
            ORDER BY updated_at DESC""")#VA A MOSTRAR EL ULTIMO UPDATEADO
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

def edit_media(title:str, url:str, id:int):
    if id<=0:
        raise ValueError("ID invalido")
    if not title.strip():
        raise ValueError("El titulo no puede ser vacio")
    if not url.strip():
        raise ValueError("El url no puede ser vacio")
    
    with get_connection() as conn:
        cursor = conn.execute("""
            UPDATE media
            SET title = ?,url = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?""",
            (title.strip(),url.strip(),id))
        
        if cursor.rowcount == 0:#ROWCOUNT DEVUELVE CUANTAS FILAS FUERON CAMBIADAS DURANTE EL UPDATE
            raise ValueError("No se pudo editar el video, el ID no existe")
    return        