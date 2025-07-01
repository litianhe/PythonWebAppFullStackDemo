from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True if settings.ENVIRONMENT == "dev" else False,
)


def get_dbsession():
    with Session(engine) as session:
        yield session
