import os
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_sqlite_connection():
    sqlite_path = os.getenv("SQLITE_PATH")  # Get path from environment variable
    if not sqlite_path:
        raise ValueError("SQLITE_PATH environment variable not set")
    conn = sqlite3.connect(sqlite_path)
    return conn


def get_oracle_engine():
    oracle_url = os.getenv("ORACLE_URL")  # Get URL from environment variable
    if not oracle_url:
        raise ValueError("ORACLE_URL environment variable not set")
    return create_engine(oracle_url, arraysize=1000)


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
