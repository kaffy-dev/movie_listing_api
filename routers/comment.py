from fastapi import APIRouter, Depends
from typing import List
from crud.comment import crudService as crud
from sqlalchemy.orm import Session
from database import get_db
import schema.comment as schema
import schema.user as schemau
from auth import get_current_user
from uuid import UUID

from logger import get_logger

logger = get_logger(__name__)


comment_router = APIRouter()

@comment_router.get('/', response_model=List[schema.Comment])
def view_all_comments(offset: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    logger.info('Getting all comments')
    comments = crud.get_comments(db, offset, limit)
    return comments

@comment_router.get('/{movie_id}')
def get_comment_for_a_movie(movie_id: UUID, offset: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    logger.info('Getting comments for a movie by movie_id')
    comment = crud.get_comment_for_a_movie(db, movie_id, offset, limit)
    return {"message": "success", "data": comment}

@comment_router.post('/')
def add_comment(username: str,
                movie_id: UUID,
                payload: schema.CommentCreate, 
                user: schemau.User = Depends(get_current_user), 
                db: Session = Depends(get_db)
                ):
    logger.info('Adding a comment...')
    comment = crud.add_comment(db, payload, username, movie_id)
    return {'message': 'Comment added successfully', 'data': comment}

@comment_router.post('/nested_comment')
def add_reply_to_existing_comment(reply_username: str,
                                    parent_comment_id: UUID,
                                    payload: schema.NestedCommentCreate, 
                                    user: schemau.User = Depends(get_current_user), 
                                    db: Session = Depends(get_db)
                                    ):
    logger.info('Adding reply to existing comment')
    nested_comment = crud.nested_comment(db, payload, reply_username, parent_comment_id)
    return {'message': 'Reply added successfully', 'data': nested_comment}

@comment_router.post('/nested_reply')
def add_reply_to_existing_reply(reply_username: str,
                 parent_reply_id: UUID,
                 payload: schema.NestedCommentCreate,
                 user: schemau.User = Depends(get_current_user),
                 db: Session = Depends(get_db)
                ):
    logger.info('Adding reply to existing reply')
    nested_reply_data = crud.nested_reply(db, payload, reply_username, parent_reply_id)
    return {'message': 'Reply added successfully', 'data': nested_reply_data}


