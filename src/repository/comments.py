from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, Comment
from src.schemas.comments import CommentModel, CommentUpdateSchema
from src.services.profanity_filter import contains_profanity


async def create_comment(body: CommentModel, db: AsyncSession, current_user: User):

    comment = Comment(**body.model_dump(exclude_unset=True), user_id=current_user.id)
    if contains_profanity(comment.text):
        comment = Comment(
            **body.model_dump(exclude_unset=True),
            user_id=current_user.id,
            is_blocked=True
        )
        print("Post contains forbidden words and has been blocked.")
    else:
        comment = Comment(
            **body.model_dump(exclude_unset=True),
            user_id=current_user.id,
            is_blocked=False  # Set is_blocked to False if no profanity is found
        )
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
