from services.media_player import add_media,get_pending,get_completed,delete_media,mark_completed,get_media_by_id,edit_media,update_current_seconds

def test_manual_1():#CREO VIDEOS
    for i in range(1,8):
        video_id = add_media(f"Video test {i}",f"youtube.com/test{i}",i)
        print("ID AGREGADO: ",video_id)
        print("\n")
        media = get_media_by_id(i)
        print(media['title'],",",media['status'])


def test_manual_2():
    #MARCO COMO COMPLETO
    for i in range(1,3):
        mark_completed(i)

    #MUESTRO VIDEOS PENDIENTES
    pending_videos = get_pending()
    for row in pending_videos:
        print(row['title'],",",row['status'])
        print("\n")

    #MUESTRO VIDEOS COMPLETOS
    completed_videos = get_completed()
    for row in completed_videos:
        print(row['title'],",",row['status'])
        print("\n")

def test_manual_3():#ELIMINO UN VIDEO DE PENDING
    pending_videos = get_pending()
    print(len(pending_videos))
    delete_media(7)
    pending_videos = get_pending()
    print(len(pending_videos))
