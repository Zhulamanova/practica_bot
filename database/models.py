from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.database_module import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=True)
    username = Column(String(100), nullable=True)
    telegram_user_id = Column(String(100), nullable=False)

    request_histories = relationship("RequestHistory")


class RequestHistory(Base):
    __tablename__ = 'request_histories'
    id = Column(Integer, primary_key=True)
    request_text = Column(String(150), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, nullable=True)
