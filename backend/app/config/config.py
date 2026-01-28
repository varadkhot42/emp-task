import os

class Config:
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ["DB_NAME"]
    DB_USER = os.environ["DB_USER"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]

