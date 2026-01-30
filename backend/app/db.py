import psycopg2
import os

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "taskdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "varad123"),
        port=os.getenv("DB_PORT", "5432"),
    )
