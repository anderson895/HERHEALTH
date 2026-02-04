# migrations/run_migration.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Database

def run_migration():
    db = Database()
    
    try:
        print("🔹 Starting migration...")

        # Begin transaction
        db.execute_query("BEGIN;")
        
        print("Creating 'user' table...")
        db.execute_query("""
            CREATE TABLE IF NOT EXISTS "user" (
                id SERIAL PRIMARY KEY,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                name VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                status VARCHAR(50) DEFAULT 'active'
            );
        """)
        
        print("Creating 'chat' table...")
        db.execute_query("""
            CREATE TABLE IF NOT EXISTS chat (
                chat_id SERIAL PRIMARY KEY,
                chat_sender_id INTEGER NOT NULL,
                chat_content TEXT NOT NULL,
                chat_bot_response JSONB NOT NULL DEFAULT '{}'::jsonb,
                chat_status SMALLINT NOT NULL DEFAULT 1,
                chat_sent_date TIMESTAMPTZ DEFAULT NOW()
            );
        """)
        
        print("Creating indexes...")
        db.execute_query('CREATE INDEX IF NOT EXISTS idx_user_email ON "user"(email);')
        db.execute_query('CREATE INDEX IF NOT EXISTS idx_chat_sender_date ON chat(chat_sender_id, chat_sent_date);')

        print("Adding foreign key constraint...")
        db.execute_query("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 
                    FROM pg_constraint 
                    WHERE conname = 'fk_chat_sender'
                ) THEN
                    ALTER TABLE chat
                    ADD CONSTRAINT fk_chat_sender
                    FOREIGN KEY (chat_sender_id)
                    REFERENCES "user"(id)
                    ON DELETE CASCADE;
                END IF;
            END $$;
        """)

        # Commit transaction
        db.execute_query("COMMIT;")
        print("✅ Migration completed successfully!")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        db.execute_query("ROLLBACK;")
    finally:
        db.close()


if __name__ == "__main__":
    run_migration()
