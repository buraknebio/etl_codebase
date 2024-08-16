import os
import logging
import sqlite3
import cx_Oracle
from migration import migrate_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def openwebui_sync(sqlite_path, oracle_name, oracle_password, oracle_port, oracle_url, chat_table_name, user_table_name):
    """
    Synchronizes data from SQLite to Oracle.
    """

    # Log environment variables
    logging.info(f"SQLite Path: {sqlite_path}")
    logging.info(f"Oracle Name: {oracle_name}")
    logging.info(f"Oracle Password: {oracle_password}")  # Consider masking or omitting this in logs
    logging.info(f"Oracle Port: {oracle_port}")
    logging.info(f"Oracle URL: {oracle_url}")
    logging.info(f"Chat Table Name: {chat_table_name}")
    logging.info(f"User Table Name: {user_table_name}")

    try:
        # Call the migrate_data function for data transfer
        result = migrate_data()

        if result == "ok":
            logging.info("Data synchronization completed successfully.")
            return "ok"
        else:
            logging.error("Data synchronization failed.")
            return "not ok"

    except Exception as e:
        logging.error(f"An error occurred during synchronization: {e}")
        return "not ok"


if __name__ == "__main__":
    # Get environment variables
    sqlite_path = os.getenv("SQLITE_PATH")
    oracle_name = os.getenv("ORACLE_NAME")
    oracle_password = os.getenv("ORACLE_PASSWORD")
    oracle_port = os.getenv("ORACLE_PORT")
    oracle_url = os.getenv("ORACLE_URL")
    chat_table_name = os.getenv("CHAT_TABLE_NAME")
    user_table_name = os.getenv("USER_TABLE_NAME")

    # Run the synchronization function
    result = openwebui_sync(sqlite_path, oracle_name, oracle_password, oracle_port, oracle_url, chat_table_name,
                           user_table_name)

    if result == "ok":
        print("Synchronization completed successfully.")
    else:
        print("Synchronization failed.")
