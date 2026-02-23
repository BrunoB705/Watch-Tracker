from database.connection import init_db
from services.media_player import add_media,get_pending,get_completed,delete_media,mark_completed,get_media_by_id,get_all_media
from tests.test_media_player import test_manual_1,test_manual_2,test_manual_3
from ui.main_window import run_app
def main():
    init_db()
    #test_manual_1()
    #test_manual_2()
    #test_manual_3()
    run_app()

    
if __name__ == "__main__":
    main()