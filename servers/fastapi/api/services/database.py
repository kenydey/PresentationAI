from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlmodel import Session


sql_url = "sqlite:///sqlite.db"
sql_engine = create_engine(sql_url, connect_args={"check_same_thread": False})


@contextmanager
def get_sql_session():
    session = Session(sql_engine)
    try:
        yield session
    finally:
        session.close()
