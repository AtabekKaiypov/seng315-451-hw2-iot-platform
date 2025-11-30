from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sensor_db.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency için database session döndürür.
    Her request'te yeni session açar, bitince kapatır.
    
    Yields:
        db: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()