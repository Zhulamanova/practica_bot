from database.database_module import session
from database.models import User


def create_user(full_name: str, username: str, telegram_user_id: str):
    try:
        db_user_id = session.query(User.id).filter(User.telegram_user_id == telegram_user_id).one_or_none()
        if db_user_id is None:
            new_user = User(full_name=full_name, telegram_user_id=telegram_user_id, username=username)
            session.add(new_user)
        session.commit()
    except:
        session.commit()


def get_user_id_by_telegram_id(telegram_id: str) -> int:
    try:
        db_user_id = session.query(User.id).filter(User.telegram_user_id == telegram_id).one_or_none()
        return db_user_id
    except:
        return None
