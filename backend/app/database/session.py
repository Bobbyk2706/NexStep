
from sqlalchemy.orm import sessionmaker

from app.database.engine import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)