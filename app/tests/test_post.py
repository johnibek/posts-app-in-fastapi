from ..schemas import PostOut, PostResponse
import pytest
from ..models import Post


def test_get_all_posts(authorized_client, create_posts):
    response = authorized_client.get("/posts/")

    def validate(post):
        return PostOut(**post)

    posts = list(map(validate, response.json()))
    print(posts)

    assert len(response.json()) == len(create_posts)
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client, create_posts):
    response = client.get("/posts/")

    assert response.status_code == 401


def test_unauthorized_user_get_one_post(client, create_posts):
    response = client.get(f"/posts/{create_posts[0].id}")

    assert response.status_code == 401


def test_one_post_not_exist(authorized_client, create_posts):
    response = authorized_client.get("/posts/8")

    assert response.status_code == 404


def test_one_post(authorized_client, create_posts):
    response = authorized_client.get(f"/posts/{create_posts[0].id}")

    post = PostOut(**response.json())

    assert response.status_code == 200
    assert post.Post.title == create_posts[0].title
    assert post.Post.content == create_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favourite pizza", "I love pepperoni", False),
    ("tallest skyscraper", "Wahoo", True)
])
def test_create_post(authorized_client, create_user, title, content, published):
    response = authorized_client.post("/posts/",
                                      json={"title": title, "content": content, "published": published})

    created_post = PostResponse(**response.json())

    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == create_user['id']


def test_create_post_default_published_true(authorized_client):
    response = authorized_client.post("/posts/", json={"title": "arbitrary title", "content": "arbitrary content"})

    created_post = PostResponse(**response.json())

    assert response.status_code == 201
    assert created_post.published == True
    assert created_post.title == "arbitrary title"
    assert created_post.content == "arbitrary content"


def test_unauthorized_user_create_post(client):
    response = client.post("/posts/", json={"title": "arbitrary title", "content": "arbitrary content"})

    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, create_posts):
    response = client.delete(f"/posts/{create_posts[0].id}")

    assert response.status_code == 401


def test_delete_post_success(authorized_client, create_posts, session):
    length_before_deletion = len(create_posts)
    response = authorized_client.delete(f"/posts/{create_posts[0].id}")
    length_after_deletion = len(session.query(Post).all())

    assert response.status_code == 204
    assert length_before_deletion - length_after_deletion == 1


def test_delete_post_non_exist(authorized_client, create_posts):
    response = authorized_client.delete("/posts/888")

    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, create_posts):
    response = authorized_client.delete(f"/posts/{create_posts[-1].id}")

    assert response.status_code == 403


def test_update_post(authorized_client, create_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": True
    }

    response = authorized_client.put(f"/posts/{create_posts[0].id}", json=data)
    updated_post = PostResponse(**response.json())

    assert response.status_code == 200
    assert updated_post.id == 1
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.published == data['published']


def test_update_other_user_post(authorized_client, create_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": True
    }

    response = authorized_client.put(f"/posts/{create_posts[2].id}", json=data)

    assert response.status_code == 403


def test_unauthorized_user_update_post(client, create_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": True
    }

    response = client.put(f"/posts/{create_posts[0].id}", json=data)

    assert response.status_code == 401


def test_update_post_non_exist(authorized_client, create_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": True
    }

    response = authorized_client.put(f"/posts/888", json=data)

    assert response.status_code == 404
