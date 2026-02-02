from flask import Flask, render_template
from backend.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
