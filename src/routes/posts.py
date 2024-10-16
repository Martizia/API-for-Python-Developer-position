from fastapi import APIRouter, Path, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.config.config import config
from src.services.auth import auth_service
from src.database.models import User, Post
from src.repository import posts as repository_posts
from src.schemas.posts import PostResponse, PostModel, PostUpdateSchema


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(
    body: PostModel = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_posts.create_post(db, body, current_user)


@router.put(
    "/{post_id}",
)
async def edit_post(
    body: PostUpdateSchema,
    post_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):

    post = await repository_posts.update_post(post_id, body, db, current_user)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return post
