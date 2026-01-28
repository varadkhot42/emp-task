from flask import Flask
from app.config.config import Config
from app.models.user_model import create_users_table
from app.models.task_model import create_tasks_table
from app.routes.task_routes import task_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        create_users_table()
        create_tasks_table()

    # register routes
    app.register_blueprint(task_bp)

    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "UP"}, 200

    return app
