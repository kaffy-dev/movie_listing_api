from sqlalchemy.orm import Session
import schema.user as schema
import models

from logger import get_logger

logger = get_logger(__name__)

def create_user(db: Session, user: schema.UserCreate, hashed_password: str):
    logger.info('Creating a user...')
    db_user = models.User(
        username=user.username, 
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    logger.info('Querying the user model to get user by username')
    return db.query(models.User).filter(models.User.username == username).first()
