from database.database_module import session
from database.models import RequestHistory
from repositories.user_repository import get_user_id_by_telegram_id
from datetime import datetime


def create_history_request(full_text: str, telegram_user_id: str):
    try:
        db_user_id = get_user_id_by_telegram_id(telegram_user_id)
        if db_user_id is not None:
            new_entity = RequestHistory(request_text=full_text, user_id=db_user_id[0], date=datetime.now())
            session.add(new_entity)
        session.commit()
    except:
        session.commit()


def get_last_ten_history_request_by_tg_id(telegram_user_id: str) -> list[str]:
    try:
        db_user_id = get_user_id_by_telegram_id(telegram_user_id)
        if db_user_id is not None:
            result_list = session.query(RequestHistory.request_text).filter(RequestHistory.user_id == db_user_id[0]) \
                .order_by(RequestHistory.date.desc())\
                .limit(10).all()
            return result_list
        else:
            return list()
    except:
        return list()
