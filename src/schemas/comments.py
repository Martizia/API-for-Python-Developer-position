from pydantic import BaseModel, Field


class CommentModel(BaseModel):
    text: str = Field(max_length=250)
    post_id: int


class CommentUpdateSchema(BaseModel):
    text: str = Field(max_length=250)
