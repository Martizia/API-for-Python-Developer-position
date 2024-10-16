from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, Comment
from src.schemas.comments import CommentModel, CommentUpdateSchema


async def create_comment(body: CommentModel, db: AsyncSession, current_user: User):

    comment = Comment(**body.model_dump(exclude_unset=True), user_id=current_user.id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def update_comment(
    comment_id: int, body: CommentUpdateSchema, db: AsyncSession, current_user: User
):

    stmt = select(Comment).filter_by(id=comment_id, user_id=current_user.id)
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()
    if comment:
        comment.text = body.text
        await db.commit()
        await db.refresh(comment)
    return comment
