from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.config import config
from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.schemas.users import UserResponse
from src.services.auth import auth_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_my_user(
    my_user: User = Depends(auth_service.get_current_user),
):
    my_user = UserResponse(
        id=my_user.id,
        username=my_user.username,
        email=my_user.email,
    )

    return my_user


@router.put(
    "/",
)
async def edit_my_name(
    name: str,
    user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):

    user = await repository_users.update_my_name(user, name, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return user
