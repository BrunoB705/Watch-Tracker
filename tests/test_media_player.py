from services.media_player import add_media, get_pending, get_completed, delete_media, mark_completed, get_media_by_id, edit_media, update_current_seconds
from database.models import Media

def test_manual_1():  # CREO VIDEOS
    for i in range(1, 8):
        media = Media(
            title=f"Video test {i}",
            url=f"youtube.com/test{i}",
            current_seconds=i
        )
        video_id = add_media(media)
        print("ID AGREGADO: ", video_id)
        print("\n")
        retrieved_media = get_media_by_id(i)
        print(retrieved_media.title, ",", retrieved_media.status)


def test_manual_2():
    # MARCO COMO COMPLETO
    for i in range(1, 3):
        mark_completed(i)

    # MUESTRO VIDEOS PENDIENTES
    pending_videos = get_pending()
    for media in pending_videos:
        print(media.title, ",", media.status)
        print("\n")

    # MUESTRO VIDEOS COMPLETOS
    completed_videos = get_completed()
    for media in completed_videos:
        print(media.title, ",", media.status)
        print("\n")

def test_manual_3():  # ELIMINO UN VIDEO DE PENDING
    pending_videos = get_pending()
    print(len(pending_videos))
    delete_media(7)
    pending_videos = get_pending()
    print(len(pending_videos))
