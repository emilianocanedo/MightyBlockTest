from flask_restx import fields, Model

create_account_schema = Model('CreateAccountSchema',{
    'username': fields.String(description='Username'),
    'password': fields.String(description='Password')
})

session_token_schema = Model('SessionSchema',{
    'jwt_token': fields.String(description='JWT session token'),
})

post_schema = Model('PostSchema',{
    'id': fields.Integer(readonly=True, description='id'),
    'likes': fields.Integer(readonly=True, description='Number of likes'),
    'text': fields.String(description='Post text')
})

get_posts_schema = Model('CreatePost',{
    'posts': fields.List(cls_or_instance=fields.Nested(post_schema, skip_none=True), description='Results')
})

all_schemas = [create_account_schema, session_token_schema, post_schema, get_posts_schema]