from fastapi.testclient import TestClient
from ..main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import Base, Post
from ..database import get_db
from ..config import settings
import pytest
from ..oauth2 import create_access_token


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def create_user(client):
    user_data = {
        "username": "thomas",
        "password": "thomas123",
        "email": "thomas@mail.com"
    }
    response = client.post("/users/", json=user_data)
    new_user = response.json()  # {"username": "thomas", "password": "hashed_password", "email": "thomas@mail.com"}
    new_user['password'] = user_data['password']  # {"username": "thomas", "password": "thomas123", "email": "thomas@mail.com"}
    return new_user


@pytest.fixture
def create_user2(client):
    user_data = {
        "username": "john",
        "password": "john123",
        "email": "john@mail.com"
    }
    response = client.post("/users/", json=user_data)
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(create_user):
    return create_access_token({"user_id": create_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def create_posts(create_user, session, create_user2):
    sample_posts = [
        {
            "title": "1st post",
            "content": "1st content",
            "user_id": create_user['id']
        },
        {
            "title": "2nd post",
            "content": "2nd content",
            'user_id': create_user['id']
        },
        {
            "title": "3rd post",
            "content": "3rd content",
            "user_id": create_user2['id']
        }
    ]

    def create_post_model(post_dict):
        return Post(**post_dict)

    posts = list(map(create_post_model, sample_posts))

    session.add_all(posts)
    session.commit()

    posts_created = session.query(Post).all()

    return posts_created
