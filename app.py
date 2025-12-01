from flask import Flask, render_template

# Kendi dosyalarımızı içeri aktaralım
from config import Config
from api_routes import api

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Blueprint'i (API rotalarını) kaydet
    app.register_blueprint(api)

    # Ana Sayfa Rotası (URL: /)
    @app.route("/")
    def index():
        # HTML_PAGE içeriği artık templates/index.html dosyasından yüklenecek.
        return render_template('index.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config['DEBUG'])