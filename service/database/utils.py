from sqlalchemy import select

from service.database import Session
from service.database.models import Users


def init_user(session, user_id):
    user = session.scalar(
        select(Users).where(Users.telegram_id == user_id)
    )
    if user is None:
        user = Users(telegram_id=user_id)
        insert_record(session, user)
    return user


def insert_record(session, record):
    session.add(record)
    session.commit()
    session.refresh(record)


def get_all_usernames():
    with Session() as session:
        usernames = session.scalars(
            select(Users.username)
        ).all()
        return usernames


def get_user_by_username(username):
    with Session() as session:
        user = session.scalar(
            select(Users).where(Users.username == username)
        )
        return user
