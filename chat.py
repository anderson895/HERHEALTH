import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor
from database import Database
import json

class Chat(Database):
    def __init__(self):
        """Initializes the User class and ensures the database connection is established."""
        super().__init__()

 
    

    def close(self):
        """Closes the database connection properly when done."""
        super().close()


if __name__ == "__main__":
    db = Database()
    db.test_connection()
    db.close()
