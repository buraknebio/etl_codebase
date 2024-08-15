# db_config.py
import os
import sqlite3
import subprocess
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_sqlite_connection():
    container_name = os.getenv("CONTAINER_NAME", "openwebui")
    db_path_in_container = "/app/backend/data/webui.db"
    local_db_path = "/tmp/webui.db"  # Choose a suitable temporary location

    try:
        subprocess.run(
            ["docker", "cp", f"{container_name}:{db_path_in_container}", local_db_path],
            check=True,
        )
        conn = sqlite3.connect(local_db_path)
        return conn
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error copying database from container: {e}")


def get_oracle_engine(oracle_url):
    return create_engine(oracle_url, arraysize=10000)


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
