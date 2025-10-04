from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Users


engine = create_engine("sqlite:///service/database/db.sqlite3")
Session = scoped_session(sessionmaker(bind=engine))


def init_db():
    SQLModel.metadata.create_all(engine)
