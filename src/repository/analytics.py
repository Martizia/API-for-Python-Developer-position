from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from src.database.models import Comment, Post
from datetime import datetime


async def get_posts_daily_breakdown(
    db: AsyncSession, date_from: datetime, date_to: datetime
):
    query = (
        select(
            func.date(Post.created_at).label("date"),
            func.count(Post.id).filter(Post.is_blocked == False).label("created_count"),
            func.count(Post.id).filter(Post.is_blocked == True).label("blocked_count"),
        )
        .where(and_(Post.created_at >= date_from, Post.created_at <= date_to))
        .group_by(func.date(Post.created_at))
    )

    result = await db.execute(query)
    return result.all()


async def get_comments_daily_breakdown(
    db: AsyncSession, date_from: datetime, date_to: datetime
):
    query = (
        select(
            func.date(Comment.created_at).label("date"),
            func.count(Comment.id)
            .filter(Comment.is_blocked == False)
            .label("created_count"),
            func.count(Comment.id)
            .filter(Comment.is_blocked == True)
            .label("blocked_count"),
        )
        .where(and_(Comment.created_at >= date_from, Comment.created_at <= date_to))
        .group_by(func.date(Comment.created_at))
    )

    result = await db.execute(query)
    return result.all()
