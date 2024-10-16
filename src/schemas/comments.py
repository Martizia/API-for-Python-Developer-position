from pydantic import BaseModel, Field
from sqlalchemy import null


class CommentModel(BaseModel):
    text: str = Field(max_length=250)
    post_id: int
    parent_comment_id: int | None = Field(default=None)


class CommentUpdateSchema(BaseModel):
    text: str = Field(max_length=250)
