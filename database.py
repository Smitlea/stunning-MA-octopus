# app/database.py
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()  # 讀 .env（在 Docker 裡我們用環境變數也可）

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


# FastAPI 依賴用：拿一個 db session, request 結束就關
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
