import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor
from database import Database
import json
class User(Database):
    def __init__(self):
        """Initializes the User class and ensures the database connection is established."""
        super().__init__()

    def check_and_update_password(self, user_id, currentpassword, newpassword):
        result = self.fetch_one('SELECT password FROM "user" WHERE id = %s', (user_id,))
        
        if result is None:
            return False  
        
        stored_password_hash = result['password']
        current_password_hash = hashlib.sha256(currentpassword.encode()).hexdigest()

        # Check if current password is correct
        if stored_password_hash != current_password_hash:
            return False  # Current password is incorrect

        # Hash the new password
        new_password_hash = hashlib.sha256(newpassword.encode()).hexdigest()

        # Update the password in the database
        self.execute_query('UPDATE "user" SET password = %s WHERE id = %s', (new_password_hash, user_id))

        return True  # Password updated successfully


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
        status='active'

        try:
            self.execute_query('''INSERT INTO "user" (name, email, password,status) VALUES (%s, %s, %s,%s)''', 
                               (name, email, hashed_password,status))
            print("✅ Account created successfully")
            return True
        except psycopg2.IntegrityError as e:
            print(f"❌ Error creating account: Email might already exist. {e}")
            return False
        except psycopg2.Error as e:
            print(f"❌ Database error: {e}")
            return False
    

    def login_user_account(self, email, password):
        """Checks if the email and password combination exists in the database."""
        hashed_password = self.hash_password(password)

        result = self.fetch_one('''
            SELECT COUNT(*) FROM "user"
            WHERE email = %s AND password = %s
        ''', (email, hashed_password))

        return result['count'] > 0 if result else False

    def search_user_session(self, email, password):
        """Retrieves user details if login credentials are valid."""
        hashed_password = self.hash_password(password)

        result = self.fetch_one('''
            SELECT id, name, email, created_at FROM "user"
            WHERE email = %s AND password = %s
        ''', (email, hashed_password))

        # Prepare the response data
        if result:
            response_data = {
                'success': True,
                'account': result
            }
        else:
            response_data = {
                'success': False,
                'message': 'Incorrect Email or Password'
            }

        return json.dumps(response_data, default=str)

    def close(self):
        """Closes the database connection properly when done."""
        super().close()
