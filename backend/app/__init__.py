from flask import Flask
from app.routes import register_routes
from app.pages import register_pages

def create_app():
    app = Flask(__name__)

    register_routes(app)
    register_pages(app)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app
