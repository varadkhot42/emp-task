from flask import Flask
from app.config.config import Config
from app.models.user_model import create_users_table
from app.models.task_model import create_tasks_table

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        create_users_table()
        create_tasks_table()

    @app.route("/health")
    def health():
        return {"status": "UP"}, 200

    return app
