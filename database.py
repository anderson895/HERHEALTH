import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from contextlib import contextmanager

# Load variables from .env
load_dotenv()


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establish a connection to the database using DATABASE_URL from env."""
        database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise ValueError("❌ DATABASE_URL is not set in environment variables")

        try:
            self.conn = psycopg2.connect(database_url)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print("✅ Successfully connected to the database.")
        except psycopg2.Error as e:
            print(f"❌ Database connection error: {e}")
            self.conn = None
            self.cursor = None
            raise  # Re-raise to prevent silent failures

    def execute_query(self, query, params=()):
        """Execute INSERT/UPDATE/DELETE queries."""
        if not self.conn or self.conn.closed:
            self.connect()

        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor
        except psycopg2.Error as e:
            print(f"❌ Database error: {e}")
            if self.conn:
                self.conn.rollback()
            raise  # Re-raise to handle errors properly

    def fetch_all(self, query, params=()):
        """Execute SELECT query and return all rows."""
        if not self.conn or self.conn.closed:
            self.connect()
        
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"❌ Database error: {e}")
            return []

    def fetch_one(self, query, params=()):
        """Execute SELECT query and return one row."""
        if not self.conn or self.conn.closed:
            self.connect()
        
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except psycopg2.Error as e:
            print(f"❌ Database error: {e}")
            return None

    def close(self):
        """Close cursor and database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("🔌 Database connection closed.")

    def test_connection(self):
        """Test DB connection."""
        result = self.fetch_one("SELECT 1 AS test")
        if result:
            print("✅ Connection test successful.")
            return True
        else:
            print("❌ Connection test failed.")
            return False

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - auto close connection."""
        self.close()


if __name__ == "__main__":
    # Test with context manager
    with Database() as db:
        db.test_connection()