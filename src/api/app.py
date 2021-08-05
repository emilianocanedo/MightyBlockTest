from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Resource, Api

import settings

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    app.db = SQLAlchemy(app)
    api = Api(app)

    @api.route('/login')
    class Login(Resource):
        def post(self):
            return {'hello': 'world'}

    @api.route('/post')
    class Post(Resource):
        def post(self):
            return {'hello': 'world'}
        def get(self):
            return {'hello': 'world'}

    return app
