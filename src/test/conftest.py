import pytest

from api.app import create_app

@pytest.fixture
def app(mocker):
    mocker.patch('settings.SQLALCHEMY_DATABASE_URI', "sqlite:///:memory:")
    app = create_app()
    # CREATE DB
    app.db.engine.execute(f'''
    CREATE TABLE user (
        id integer,
        username varchar(200),
        password varchar(200)
    );
    ''')
    app.db.engine.execute(f'''
    CREATE TABLE userpost (
        id integer,
        text varchar(280),
        image varchar(200),
        likes integer,
        created_dt datetime,
        user_id integer
    );
    ''')
    return app
