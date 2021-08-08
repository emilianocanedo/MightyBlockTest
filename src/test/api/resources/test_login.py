import pytest

from model import User

def test_create_account(app):
    with app.test_client() as c:
        response = c.post(
            f'mighty_blocks_api/login/create_account',
            json={'username': 'user', 'password': 'passwd'}
        )
        assert response.status_code == 200


def test_account_already_created(app):
    with app.test_client() as c:
        app.db.engine.execute(f'''
        INSERT INTO user (id, username, password) VALUES
        (1, "user", "passwd");
        ''')
        response = c.post(
            f'mighty_blocks_api/login/create_account',
            json={'username': 'user', 'password': 'passwd'}
        )
        assert response.status_code == 409


def test_get_session_token(app):
    with app.test_client() as c:
        app.db.engine.execute(f'''
        INSERT INTO user (id, username, password) VALUES
        (1, "user", "passwd");
        ''')
        response = c.post(
            f'mighty_blocks_api/login/get_session_token',
            json={'username': 'user', 'password': 'passwd'}
        )
        assert 'jwt_token' in response.json
        assert response.status_code == 200


def test_get_session_token_not_authorized(app):
    with app.test_client() as c:
        app.db.engine.execute(f'''
        INSERT INTO user (id, username, password) VALUES
        (1, "other_user", "other_passwd");
        ''')
        response = c.post(
            f'mighty_blocks_api/login/get_session_token',
            json={'username': 'user', 'password': 'passwd'}
        )
        assert response.status_code == 401
