import os
import logging
from dotenv import load_dotenv
from testcontainers.oracle import OracleDbContainer
from .models import metadata
from .migration import migrate_data
from sqlalchemy import create_engine

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    with OracleDbContainer() as oracle:
        oracle_url = oracle.get_connection_url()

        # Create tables in Oracle
        engine = create_engine(oracle_url, arraysize=10000)
        metadata.create_all(engine)

        # Migrate data
        migrate_data(oracle_url)

        print(f"Oracle Connection URL: {oracle.get_connection_url()}")
        input("Press Enter to stop the container...")
