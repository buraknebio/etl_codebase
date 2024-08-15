import logging
from datetime import datetime
from sqlalchemy import insert
import os
import subprocess
import shutil
import sqlite3
from .db_config import get_sqlite_connection, get_oracle_engine, get_session
from .models import user_table, chat_table

logger = logging.getLogger(__name__)

def migrate_data(oracle_url):
    engine = get_oracle_engine(oracle_url)
    session = get_session(engine)

    tmp_db_path = "/tmp/webui.db"

    try:
        container_name = os.getenv("CONTAINER_NAME", "openwebui")
        db_path_in_container = "/app/backend/data/webui.db"
        subprocess.run(["docker", "cp", f"{container_name}:{db_path_in_container}", tmp_db_path], check=True)

        tmp_conn = sqlite3.connect(tmp_db_path)


        logger.debug("Starting data migration process...")

        tmp_cursor = tmp_conn.cursor()
        tmp_cursor.execute(
            'SELECT id, name, email, role, created_at, updated_at, last_active_at FROM user'
        )
        users = tmp_cursor.fetchall()
        logger.debug(f"Fetched {len(users)} users from SQLite.")

        tmp_cursor.execute(
            'SELECT id, user_id, title, chat, created_at, updated_at FROM chat'
        )
        chats = tmp_cursor.fetchall()
        logger.debug(f"Fetched {len(chats)} chats from SQLite.")

        dtime = datetime.now()

        # Insert users
        user_records = [{
            'id': user[0],
            'name': user[1],
            'email': user[2],
            'role': user[3],
            'created_at': datetime.fromtimestamp(user[4]) if user[4] else None,
            'updated_at': datetime.fromtimestamp(user[5]) if user[5] else None,
            'last_active_at': datetime.fromtimestamp(user[6]) if user[6] else None,
            'reflected_at': dtime
        } for user in users]
        session.execute(insert(user_table), user_records)
        logger.debug("Inserted users into Oracle.")

        # Insert chats
        chat_records = [{
            'id': chat[0],
            'user_id': chat[1],
            'title': chat[2],
            'chat': chat[3],
            'created_at': datetime.fromtimestamp(chat[4]) if chat[4] else None,
            'updated_at': datetime.fromtimestamp(chat[5]) if chat[5] else None,
            'reflected_at': dtime
        } for chat in chats]
        session.execute(insert(chat_table), chat_records)
        logger.debug("Inserted chats into Oracle.")

        session.commit()
        logger.debug("Data migration completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred during data migration: {e}")
        session.rollback()
        raise
    finally:
        session.close()
