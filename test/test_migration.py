# etl_process/test/test_migration.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from testcontainers.oracle import OracleDbContainer
from ..migration import migrate_data
from ..models import metadata
from ..db_config import get_sqlite_connection

load_dotenv()

class TestMigration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with OracleDbContainer() as oracle:
            cls.oracle_url = oracle.get_connection_url()
            # Create tables in Oracle
            engine = create_engine(cls.oracle_url, arraysize=10000)
            metadata.create_all(engine)

    def setUp(self):
        self.sqlite_conn = get_sqlite_connection()
        self.engine = create_engine(self.oracle_url, arraysize=10000)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()

    def test_new_user(self):
        # Add a new user to SQLite
        self.sqlite_conn(
            "INSERT INTO user (id, name, email, role) VALUES ('test_user_id', 'Test User', 'test@example.com', 'user')"
        )

        # Migrate data
        migrate_data(self.oracle_url)

        # Check if the new user exists in Oracle
        result = self.session.execute(
            "SELECT * FROM user WHERE id = 'test_user_id'"
        ).fetchone()
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
