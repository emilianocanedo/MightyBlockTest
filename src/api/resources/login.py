from datetime import datetime, timedelta
import flask
import jwt
from flask_restx import Resource, abort, Namespace
from flask import request
from api.resources.schema import create_account_schema, session_token_schema
from model import User


app = flask.current_app
ns_login = Namespace('login', description='Login endpoints')


@ns_login.route('/create_account')
class CreateAccount(Resource):
    @ns_login.expect(create_account_schema, validate=True)
    @ns_login.doc(
        responses={
            201: 'Created',
            409: 'User already created'
        }, description='''
            Create Account
        '''
    )
    def post(self):
        output = app.db.session.query(User).filter(User.username == request.json['username']).first()
        if output is not None:
            abort(409, 'User already created')
        print(request.json)
        user = User(**request.json)
        app.db.session.add(user)
        app.db.session.commit()
        return 201


@ns_login.route('/get_session_token')
class Session(Resource):
    @ns_login.expect(create_account_schema, validate=True)
    @ns_login.marshal_with(session_token_schema)
    @ns_login.doc(
        responses={
            200: 'Success',
            401: 'Not authorized'
        }, description='''
            Get Session Token. This will be valid for 1 hour.
            In order to use the 'post' endpoints, you need to provide an Authorization header like:
            Authorization: Bearer TOKEN
        '''
    )
    def post(self):
        output = app.db.session.query(User).filter(
            User.username == request.json['username'] and
            User.password == request.json['password']
        ).first()
        if output is None:
            abort(401, 'Bad Login')
        expiration_time = datetime.utcnow()+timedelta(hours=1)
        token = jwt.encode({'user_id': output.id, "exp": expiration_time}, 'JWTSECRET')
        return {'jwt_token': token}
