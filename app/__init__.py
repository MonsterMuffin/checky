from flask import Flask
from .models import init_db

def create_app():
    app = Flask('checky')

    with app.app_context():
        init_db(app)

    from .routes import init_routes
    init_routes(app)

    return app