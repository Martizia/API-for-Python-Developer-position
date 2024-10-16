from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class PostResponse(BaseModel):
    id: int
    title: str
    description: str
    user_id: int
    created_at: datetime


class PostModel(BaseModel):
    title: str = Field(max_length=150)
    description: str = Field(max_length=250)


class PostUpdateSchema(BaseModel):
    title: str = Field(max_length=150)
    description: str = Field(max_length=250)
