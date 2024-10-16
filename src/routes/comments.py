from fastapi import APIRouter, Depends, Path, status, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.repository import comments as repository_comments
from src.schemas.comments import CommentModel, CommentUpdateSchema
from src.services.auth import auth_service
from src.repository.posts import get_post


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post(
    "/",
    response_model=CommentModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    body: CommentModel = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):

    await get_post(db, body.post_id)
    if body is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Comment is empty"
        )
    comment = await repository_comments.create_comment(body, db, current_user)
    return comment


@router.put(
    "/{comment_id}",
)
async def edit_comment(
    body: CommentUpdateSchema,
    comment_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):

    comment = await repository_comments.update_comment(
        comment_id, body, db, current_user
    )
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return comment
