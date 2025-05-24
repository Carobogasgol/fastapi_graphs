from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import time
import os

SQLALCHEMY_DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@postgres:5432/postgres'
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True
)

from sqlalchemy import text
from app.database import engine
from app.models import Base

def recreate_tables():
    with engine.connect() as conn:
        conn.execute(text('DROP SCHEMA public CASCADE;'))
        conn.execute(text('CREATE SCHEMA public;'))
        conn.commit()
    
    Base.metadata.create_all(bind=engine)

from app.models import Base
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 