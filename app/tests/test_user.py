from ..schemas import UserOut, Token
import jwt
from ..config import settings
import pytest


def test_user_create(client):
    response = client.post("/users/", json={"username": "thomas", "password": "thomas123", "email": "thomas@mail.com"})
    user = UserOut(**response.json())
    # assert response.json().get("email") == 'thomas@mail.com'
    assert user.email == 'thomas@mail.com'
    assert response.status_code == 201


def test_user_login(client, create_user):
    response = client.post("/users/auth/login", data={'username': create_user['username'], "password": create_user['password']})
    login_res = Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == create_user['id']
    assert login_res.token_type == "Bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("username, password, status_code", [
    ("wrongusername", "thomas123", 403),
    ("thomas", "wrongpassword", 403),
    ("wrongusername", "wrongpassword", 403),
    (None, "thomas123", 422),
    ("thomas", None, 422)
])
def test_incorrect_login(client, create_user, username, password, status_code):
    response = client.post("/users/auth/login", data={"username": username, "password": password})

    assert response.status_code == status_code
