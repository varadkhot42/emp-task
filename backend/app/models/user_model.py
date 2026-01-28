from app.utils.db import get_db_connection

def create_users_table():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role VARCHAR(20) CHECK (role IN ('ADMIN', 'EMPLOYEE')) NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
