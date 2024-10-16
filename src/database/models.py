from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    DateTime,
    Boolean,
    func,
    Table,
    Column,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from datetime import date


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), index=True)
    description: Mapped[str] = mapped_column(String(250), nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[date] = mapped_column(
        "created_at", DateTime, default=func.now(), nullable=True
    )
    comments = relationship("Comment", cascade="all, delete")


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(250), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.id"), nullable=False
    )
    created_at: Mapped[date] = mapped_column(
        "created_at", DateTime, default=func.now(), nullable=True
    )


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column(
        "updated_at", DateTime, default=func.now(), onupdate=func.now()
    )
