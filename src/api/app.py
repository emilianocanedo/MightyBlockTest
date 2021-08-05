from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Resource, Api

from api.resources import blueprint as mb_blueprint

import settings

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    app.config['SECRET_KEY'] = 'JWTSECRET'
    app.db = SQLAlchemy(app)
    app.register_blueprint(mb_blueprint)

    @app.route('/')
    def swagger_doc_links():
        html = f'''
<!doctype html>
<html>
<head>
   <title>Mighty Blocks Documentation</title>
</head>
<body>
   <h1>Welcome to Mighty Blocks Swagger Documentation</h1>
   <p><a href="{mb_blueprint.url_prefix}">Mighty Blocks Swagger Documentation</a></p>
</body>
</html>
        '''
        return html


    return app
