import logging
from datetime import datetime
from sqlalchemy import insert
from db_config import get_sqlite_connection, get_oracle_engine, get_session
from models import user_table, chat_table

logger = logging.getLogger(__name__)

def migrate_data():
    """
    Migrates data from the SQLite database to the Oracle database.
    """
    engine = get_oracle_engine()
    session = get_session(engine)

    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()

        logger.debug("Starting data migration process...")

        # --- Migrate users ---
        cursor.execute(
            'SELECT id, name, email, role, created_at, updated_at, last_active_at FROM user'
        )
        users = cursor.fetchall()
        logger.debug(f"Fetched {len(users)} users from SQLite.")

        user_records = [{
            'id': user[0],
            'name': user[1],
            'email': user[2],
            'role': user[3],
            'created_at': datetime.fromtimestamp(user[4]).date() if user[4] else None,
            'updated_at': datetime.fromtimestamp(user[5]).date() if user[5] else None,
            'last_active_at': datetime.fromtimestamp(user[6]).date() if user[6] else None,
            'reflected_at': datetime.now()
        } for user in users]
        session.execute(insert(user_table), user_records)
        logger.debug("Inserted users into Oracle.")

        # --- Migrate chats ---
        cursor.execute(
            'SELECT id, user_id, title, chat, created_at, updated_at FROM chat'
        )
        chats = cursor.fetchall()
        logger.debug(f"Fetched {len(chats)} chats from SQLite.")

        chat_records = [{
            'id': chat[0],
            'user_id': chat[1],
            'title': chat[2],
            'chat': chat[3],
            'created_at': datetime.fromtimestamp(chat[4]).date() if chat[4] else None,
            'updated_at': datetime.fromtimestamp(chat[5]).date() if chat[5] else None,
            'reflected_at': datetime.now()
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
        if conn:
            conn.close()
