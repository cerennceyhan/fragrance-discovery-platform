from flask import Flask

from perfume_finder.config import Config
from perfume_finder.llm import NoteExtractor
from perfume_finder.routes import bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.extensions["note_extractor"] = NoteExtractor(
        api_key=app.config["GROQ_API_KEY"], model=app.config["GROQ_MODEL"]
    )
    app.register_blueprint(bp)
    return app
