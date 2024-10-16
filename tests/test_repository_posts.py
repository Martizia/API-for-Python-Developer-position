import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from src.database.models import User, Post
from src.schemas.posts import PostModel, PostUpdateSchema
from src.repository.posts import create_post, get_post, update_post


# Mocking the database session
class AsyncMockSession:
    def __init__(self):
        self.posts = [
            Post(id=1, title="Test Post", description="Test Description", user_id=1),
            Post(id=3, title="Old Title", description="Old Description", user_id=1),
        ]

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def commit(self):
        pass

    async def refresh(self, instance):
        pass

    async def execute(self, statement):
        print(f"Executing statement: {statement}")
        if isinstance(statement, select):
            whereclause = statement.whereclause
            if whereclause.compare(Post.id == 1):
                print("Returning post with id 1")
                return MockResult([self.posts[0]])
            elif whereclause.compare(Post.id == 2):
                print("Returning no posts")
                return MockResult([])
            elif whereclause.compare(Post.id == 3):
                print("Returning post with id 3")
                return MockResult([self.posts[1]])
        print("Returning no posts")
        return MockResult([])

    def add(self, instance):
        self.posts.append(instance)


@pytest.fixture
def db_session():
    return AsyncMockSession()


class MockResult:
    def __init__(self, rows):
        self.rows = rows

    def scalar(self):
        return self.rows[0] if self.rows else None

    def scalar_one_or_none(self):
        return self.rows[0] if self.rows else None


# Mocking the User and Post models
@pytest.fixture
def mock_user():
    return User(id=1, username="testuser")


@pytest.fixture
def mock_post():
    return Post(id=1, title="Test Post", description="Test Description", user_id=1)


# Test create_post
@pytest.mark.asyncio
async def test_create_post(db_session, mock_user):
    post_data = PostModel(title="New Post", description="New Description")
    new_post = await create_post(db_session, post_data, mock_user)
    assert new_post.title == "New Post"
    assert new_post.description == "New Description"
    assert new_post.user_id == mock_user.id


# Test get_post
@pytest.mark.asyncio
async def test_get_post_found(db_session):
    result = await get_post(db_session, 1)
    assert result is True


@pytest.mark.asyncio
async def test_get_post_not_found(db_session):
    with pytest.raises(HTTPException) as exc_info:
        await get_post(db_session, 2)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Post not found"


# Test update_post
@pytest.mark.asyncio
async def test_update_post(db_session, mock_user):
    update_data = PostUpdateSchema(
        title="Updated Title", description="Updated Description"
    )
    updated_post = await update_post(3, update_data, db_session, mock_user)
    assert updated_post.title == "Updated Title"
    assert updated_post.description == "Updated Description"


@pytest.mark.asyncio
async def test_update_post_not_found(db_session, mock_user):
    update_data = PostUpdateSchema(
        title="Updated Title", description="Updated Description"
    )
    updated_post = await update_post(2, update_data, db_session, mock_user)
    assert updated_post is None
