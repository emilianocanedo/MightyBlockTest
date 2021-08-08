from datetime import datetime
import pytest
import jwt

from model import User, UserPost


@pytest.fixture
def test_user_header(app):
    app.db.engine.execute(f'''
    INSERT INTO user (id, username, password) VALUES
    (1, "user", "passwd");
    ''')
    token = jwt.encode({'user_id': 1}, 'JWTSECRET').decode('utf-8')
    return {'Authorization': f'Bearer {token}'}


def test_create_post(app, test_user_header):
    with app.test_client() as c:
        response = c.post(
            f'mighty_blocks_api/post/create',
            json={'text': 'This is The Post'},
            headers=test_user_header
        )
        assert response.status_code == 200


def test_create_post_not_authorized(app):
    fake_token = jwt.encode({'user_id': 1}, 'FAKESECRET').decode('utf-8')
    fake_headers = {'Authorization': f'Bearer {fake_token}'}

    with app.test_client() as c:
        response = c.post(
            f'mighty_blocks_api/post/create',
            json={'text': 'This is The Post'},
            headers=fake_headers
        )
        assert response.status_code == 401


def test_add_like(app, test_user_header):
    with app.test_client() as c:
        app.db.engine.execute(f'''
        INSERT INTO userpost (id, text, likes) VALUES
        (1, "This text", 0);
        ''')
        response = c.get(
            f'mighty_blocks_api/post/add_like/1',
            headers=test_user_header
        )
        assert response.status_code == 200

        # check increment
        post = app.db.session.query(UserPost).get(1)
        assert post.likes == 1


def test_add_like_post_not_found(app, test_user_header):
    with app.test_client() as c:
        app.db.engine.execute(f'''
        INSERT INTO userpost (id, text, likes) VALUES
        (1, "This text", 0);
        ''')
        response = c.get(
            f'mighty_blocks_api/post/add_like/2',
            headers=test_user_header
        )
        assert response.status_code == 404


def test_get_posts(app, test_user_header):
    with app.test_client() as c:
        app.db.engine.execute(f'''
        INSERT INTO userpost (id, text, likes, created_dt) VALUES
        (1, "This text", 5, datetime('2021-05-05 18:00')),
        (2, "This text 2", 10, datetime('2019-01-27 12:47')),
        (3, "This text 3", 56, datetime('2018-08-30 13:22')),
        (4, "This text 4", 3, datetime('2018-08-29 11:37'));
        ''')
        response = c.get(
            f'mighty_blocks_api/post/latest_posts',
            headers=test_user_header
        )
        assert response.status_code == 200
        expected = {'posts': [
            {'id': 1, 'likes': 5, 'text': 'This text'},
            {'id': 2, 'likes': 10, 'text': 'This text 2'},
            {'id': 3, 'likes': 56, 'text': 'This text 3'},
            {'id': 4, 'likes': 3, 'text': 'This text 4'}
        ]}
        assert response.json == expected


def test_get_posts_pagination(app, test_user_header):
    with app.test_client() as c:
        app.db.engine.execute(f'''
        INSERT INTO userpost (id, text, likes, created_dt) VALUES
        (1, "This text", 5, datetime('2021-05-05 18:00')),
        (2, "This text 2", 10, datetime('2019-01-27 12:47')),
        (3, "This text 3", 56, datetime('2018-08-30 13:22')),
        (4, "This text 4", 3, datetime('2018-08-29 11:37'));
        ''')
        response = c.get(
            f'mighty_blocks_api/post/latest_posts?page=2&rows_per_page=2',
            headers=test_user_header
        )
        assert response.status_code == 200
        print(response.json)
        expected = {'posts': [
            {'id': 3, 'likes': 56, 'text': 'This text 3'},
            {'id': 4, 'likes': 3, 'text': 'This text 4'}
        ]}
        assert response.json == expected