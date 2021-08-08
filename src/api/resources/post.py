import flask
import jwt
from flask_restx import Resource, abort, Namespace
from flask import request
from api.resources.schema import post_schema, get_posts_schema
from model import UserPost

app = flask.current_app
ns_post = Namespace('post', description='Posts endpoints')


@ns_post.route('/create')
class CreatePost(Resource):
    @ns_post.expect(post_schema, validate=True)
    @ns_post.doc(
        responses={
            201: 'Created',
            401: 'Not authorized'
        }, description='''
            Create Post
        '''
    )
    def post(self):
        try:
            token = request.headers['Authorization'].split(" ")[1]
            payload = jwt.decode(token, 'JWTSECRET')
        except jwt.DecodeError:
            abort(401, 'Signature verification failed')
        user_post = UserPost(
            user_id=payload['user_id'],
            text=request.json['text']
        )
        app.db.session.add(user_post)
        app.db.session.commit()
        return 201

    
@ns_post.route('/latest_posts')
class GetPosts(Resource):  
    @ns_post.marshal_with(get_posts_schema, as_list=True)
    @ns_post.doc(
        responses={
            200: 'Success',
            401: 'Not authorized',
            422: 'Missing query string'
        }, description='''
            Get all posts
        '''
    )
    def get(self):
        try:
            token = request.headers['Authorization'].split(" ")[1]
            payload = jwt.decode(token, 'JWTSECRET')
        except jwt.DecodeError:
            abort(401, 'Signature verification failed')

        if request.args:
            # pagination on
            try:
                page = int(request.args['page'])
                rows_per_page = int(request.args['rows_per_page'])
            except KeyError:
                abort(422, 'Missing query string') 
            output = app.db.session.query(UserPost).order_by(
                UserPost.created_dt.desc()).paginate(page=page, per_page=rows_per_page).items
        else:
            #pagination off
            output = app.db.session.query(UserPost).order_by(
                UserPost.created_dt.desc())

        return {'posts': output}


@ns_post.route('/add_like/<int:post_id>')
class AddLike(Resource):  
    @ns_post.doc(
        responses={
            200: 'Success',
            401: 'Not authorized',
            404: 'Not found'
        }, description='''
            Add like to a post
        '''
    )
    def get(self, post_id):
        try:
            token = request.headers['Authorization'].split(" ")[1]
            payload = jwt.decode(token, 'JWTSECRET')
        except jwt.DecodeError:
            abort(401, 'Signature verification failed')

        output = app.db.session.query(UserPost).get(post_id)
        if output is None:
            abort(404, 'Post id not found')
        # to avoid null problems
        prev_likes = 0 if output.likes is None else output.likes
        output.likes = prev_likes + 1
        app.db.session.commit()

        return 200
