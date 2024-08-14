from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
import schema.comment as schema
import models
from uuid import UUID
import uuid

from logger import get_logger

logger = get_logger(__name__)

class CommentService():
    @staticmethod
    def add_comment(db: Session, comment: schema.CommentCreate, username: str, movie_id: UUID):
        logger.info('Querying the user model')
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
        logger.info('Querying the movie model')
        movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(detail="Movie not found", status_code=status.HTTP_404_NOT_FOUND)
        db_comment = models.Comment(
            movie_id = movie.id,
            username = user.username,
            content = comment.content
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return {
            "id": db_comment.id,
            "movie_id": db_comment.movie_id,
            "username": db_comment.username,
            "content": db_comment.content,
            "movie_title": movie.title
        }
    

    @staticmethod
    def nested_comment(db: Session, comment: schema.NestedCommentCreate, reply_username: str, parent_comment_id: UUID):
        logger.info(f'Querying the user model for {reply_username}')
        user = db.query(models.User).filter(models.User.username == reply_username).first()
        if not user:
            raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
        
        logger.info(f'Querying the comment model for {parent_comment_id}')
        parent_comment = db.query(models.Comment).filter(models.Comment.id == parent_comment_id).first()
        if not parent_comment:
            raise HTTPException(detail="Comment does not exist", status_code=status.HTTP_404_NOT_FOUND)
        
        reply_id = str(uuid.uuid4())
        reply = {
            "id": reply_id,
            "comment_id": str(parent_comment_id),
            "username": user.username,
            "reply": comment.reply,
            "replies": []
        }

        if parent_comment.replies is None:
           parent_comment.replies = []

        logger.info('Appending reply to parent_comment.replies')
        parent_comment.replies.append(reply)
        
        logger.info('Marking the "replies" field as modified')
        flag_modified(parent_comment, "replies")

        logger.info('Committing changes to database')
        db.commit()
        db.refresh(parent_comment)

        response_data = {
            "content": parent_comment.content,
            "reply_id": reply["id"],
            "movie_id": parent_comment.movie_id,
            "username": parent_comment.username,
            "parent_comment_id": reply["comment_id"],
            "reply_username": reply["username"],
            "reply": reply["reply"],
            "replies": reply["replies"]
        }
        return response_data
    
    @staticmethod
    def nested_reply(db: Session, comment: schema.NestedCommentCreate, reply_username: str, parent_reply_id: UUID):
        logger.info(f'Querying the user model for {reply_username}')
        user = db.query(models.User).filter(models.User.username == reply_username).first()
        if not user:
            raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
        
        logger.info('Querying all comments in comment model')
        parent_comments = db.query(models.Comment).all()
    
        parent_comment = None
        parent_reply = None

        def find_parent_reply(reply_list, target_reply_id):
            for reply in reply_list:
                if reply['id'] == str(target_reply_id):
                   return reply
                if 'replies' in reply:
                    found_reply = find_parent_reply(reply['replies'], target_reply_id)
                if found_reply:
                    return found_reply
                return None

        logger.info('Searching for parent_reply in comments')
        for p_comment in parent_comments:
            parent_reply = find_parent_reply(p_comment.replies, parent_reply_id)
            if parent_reply:
               parent_comment = p_comment
               break
            
        if not parent_comment or not parent_reply:
            logger.error('Parent reply with ID: %s does not exist', parent_reply_id)
            raise HTTPException(detail="Reply does not exist", status_code=status.HTTP_404_NOT_FOUND)

        nested_reply_id = str(uuid.uuid4())
        nested_reply = {
           "id": nested_reply_id,
           "comment_id": str(parent_comment.id),
           "username": user.username,
           "reply": comment.reply,
           "replies": []
    }

        if 'replies' not in parent_reply:
            parent_reply['replies'] = []
        parent_reply['replies'].append(nested_reply)
        
        logger.info('Marking the "replies" field as modified')
        flag_modified(parent_comment, "replies")
        db.commit()
        db.refresh(parent_comment)

        response_data = {
           "nested_reply_id": nested_reply["id"],
           "parent_comment_id": nested_reply["comment_id"],
           "parent_reply_id": parent_reply_id,
           "nested_reply_username": nested_reply["username"],
           "nested_reply": nested_reply["reply"]
        }
        return response_data


    @staticmethod
    def get_comments(db: Session, offset: int = 0, limit: int = 5):
        logger.info('Querying the comment model')
        comments = db.query(models.Comment).offset(offset).limit(limit).all()

        # Extracting movie_ids from the comments
        movie_ids = []
        for comment in comments:
            movie_ids.append(comment.movie_id)
        
        # Fetching all movies corresponding to the movie_ids
        movies = db.query(models.Movie).filter(models.Movie.id.in_(movie_ids)).all()

        # Dictionary mapping movie_id to movie_title
        map_movie = {}
        for movie in movies:
           map_movie[movie.id] = movie.title

        formatted_comments = []
        for comment in comments:
            logger.info('Querying the movie model')
            movie_title = map_movie.get(comment.movie_id, None)
            
            if comment.replies:
                replies = comment.replies
            else:
                replies = []

            formatted_replies = [{
                "reply_id": reply.get("id"),
                "parent_comment_id": reply.get("comment_id"),
                "reply_username": reply.get("username"),
                "reply": reply.get("reply"),
                "replies": reply.get("replies")
            } for reply in replies]
            
            formatted_replies = replies

            comment_data = {
               "id": comment.id,
               "movie_title": movie_title,
               "movie_id": comment.movie_id,
               "username": comment.username,
               "content": comment.content,
               "replies": formatted_replies
            }
            formatted_comments.append(comment_data)
        
        return formatted_comments
    
    @staticmethod
    def get_comment_for_a_movie(db: Session, movie_id: UUID, offset: int = 0, limit: int = 5):
        movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(detail="Movie not found", status_code=status.HTTP_404_NOT_FOUND)
        comments = db.query(models.Comment).filter(models.Comment.movie_id == movie_id).offset(offset).limit(limit).all()
        formatted_comments = []
        for comment in comments:
            formatted_replies = [{
            "reply_id": reply.get("id"),
            "parent_comment_id": reply.get("comment_id"),
            "reply_username": reply.get("username"),
            "reply": reply.get("reply"),
            "replies": reply.get("replies")
            } for reply in comment.replies] if comment.replies else []

            comment_data = {
            "id": comment.id,
            "movie_title": movie.title,
            "movie_id": comment.movie_id,
            "username": comment.username,
            "content": comment.content,
            "replies": formatted_replies
             }
            formatted_comments.append(comment_data)

            return formatted_comments

crudService = CommentService()