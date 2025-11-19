# Db/Database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_CONNECTION_STRING

engine = create_engine(
    DB_CONNECTION_STRING, connect_args={"check_same_thread": False} if "sqlite" in DB_CONNECTION_STRING else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()   