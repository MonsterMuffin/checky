from flask import Flask
from .models import init_db
from flask_cors import CORS

def create_app():
    app = Flask('checky')

    with app.app_context():
        init_db(app)

    from .routes import init_routes
    init_routes(app)

    CORS(app)

    return app