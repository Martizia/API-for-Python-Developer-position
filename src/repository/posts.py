from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Post, User
from src.schemas.posts import PostModel, PostUpdateSchema


async def create_post(db: AsyncSession, post: PostModel, user: User):
    new_post = Post(**post.dict(), user_id=user.id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post


async def get_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return True


async def update_post(
    post_id: int, post_update: PostUpdateSchema, db: AsyncSession, user: User
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this post"
        )
    for key, value in post_update.dict(exclude_unset=True).items():
        setattr(post, key, value)
    await db.commit()
    await db.refresh(post)
    return post
