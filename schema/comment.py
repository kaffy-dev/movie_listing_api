from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class NestedCommentBase(BaseModel):
    reply: str

class NestedCommentCreate(NestedCommentBase):
    pass

class NestedComment(BaseModel):
    id: UUID
    username: str
    reply: str
    replies: Optional[List['NestedComment']] = []

    model_config = ConfigDict(from_attributes=True)


class Comment(BaseModel):
    id: UUID
    movie_id: UUID
    movie_title: Optional[str] = None
    username: str
    content: str
    replies: List[NestedComment] = []

    model_config = ConfigDict(from_attributes=True)

# To allow recursive models in Pydantic
NestedComment.model_rebuild()
