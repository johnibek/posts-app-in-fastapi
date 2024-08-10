import pytest
from app.models import Vote


@pytest.fixture
def create_vote(create_posts, create_user, session):
    new_vote = Vote(post_id=create_posts[2].id, user_id=create_user['id'])
    session.add(new_vote)
    session.commit()


def test_create_vote_on_post(authorized_client, create_posts):
    response = authorized_client.post("/vote/", json={'post_id': create_posts[2].id, 'dir': 1})
    assert response.status_code == 201


def test_vote_twice(authorized_client, create_posts, create_vote):
    response = authorized_client.post("/vote/", json={'post_id': create_posts[2].id, 'dir': 1})
    assert response.status_code == 409


def test_delete_vote_from_post(authorized_client, create_posts, create_vote):
    response = authorized_client.post("/vote/", json={'post_id': create_posts[2].id, 'dir': 0})
    assert response.status_code == 201


def test_delete_vote_non_exist(authorized_client, create_posts):
    response = authorized_client.post("/vote/", json={'post_id': create_posts[2].id, 'dir': 0})
    assert response.status_code == 404


def test_vote_on_post_non_exist(authorized_client, create_posts):
    response = authorized_client.post("/vote/", json={'post_id': 888, 'dir': 1})
    assert response.status_code == 404


def test_vote_unauthorized_user(client, create_posts):
    response = client.post("/vote/", json={"post_id": create_posts[2].id, "dir": 1})
    assert response.status_code == 401
