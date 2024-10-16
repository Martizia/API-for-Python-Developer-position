from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.schemas.users import UserSchema

from datetime import datetime


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    new_user = User(**body.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    user.refresh_token = token
    await db.commit()


async def get_user_by_id(user_id: int, db: AsyncSession) -> User | None:

    stmt = select(User).filter_by(id=user_id)
    user = await db.execute(stmt)
    result = user.scalar_one_or_none()
    return result


async def update_my_name(user: User, name: str, db: AsyncSession) -> User:

    user = await get_user_by_id(user.id, db)
    user.username = name
    user.updated_at = datetime.now()
    await db.commit()
    await db.refresh(user)
    return user
