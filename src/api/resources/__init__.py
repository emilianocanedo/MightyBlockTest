from flask import Blueprint
from flask_restx import Api

import settings
from .login import ns_login
from .post import ns_post
from .schema import all_schemas

blueprint = Blueprint('mighty_blocks_api', __name__, url_prefix=f'/mighty_blocks_api')
api = Api(blueprint, title='Mighty Blocks API')

api.add_namespace(ns_login)
api.add_namespace(ns_post)

for schema in all_schemas:
    api.add_model(schema.name, schema)
