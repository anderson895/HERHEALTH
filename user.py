import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor
from database import Database

class User(Database):
    def __init__(self):
        """Initializes the User class and ensures the database connection is established."""
        super().__init__()

    def email_exists(self, email):
        """Checks if the email already exists in the database."""
        result = self.fetch_one('SELECT email FROM "user" WHERE email = %s', (email,))
        return result is not None  # Returns True if email exists
    
    def hash_password(self, password):
        """Hashes the password securely using SHA256 (consider bcrypt or Argon2 for better security)."""
        return hashlib.sha256(password.encode()).hexdigest()  # Use bcrypt/argon2 in production

    def create_user_account(self, name, email, password):
        """Creates a new user account only if the email is unique."""
        if self.email_exists(email):
            print(f"❌ Error: The email '{email}' is already in use.")
            return False

        hashed_password = self.hash_password(password)

        try:
            self.execute_query('''INSERT INTO "user" (name, email, password) VALUES (%s, %s, %s)''', 
                               (name, email, hashed_password))
            print("✅ Account created successfully")
            return True
        except psycopg2.IntegrityError as e:
            print(f"❌ Error creating account: Email might already exist. {e}")
            return False
        except psycopg2.Error as e:
            print(f"❌ Database error: {e}")
            return False

    def close(self):
        """Closes the database connection properly when done."""
        super().close()
