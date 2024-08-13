from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.rating import crudService as crud
import schema.rating as schema
import schema.user as schemau
from database import get_db
from auth import get_current_user

from logger import get_logger

logger = get_logger(__name__)

rating_router = APIRouter()

@rating_router.get("/", response_model=List[schema.RatingResponse])
def get_all_movies_rating(offset: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    ratings = crud.get_ratings(db, offset, limit)
    logger.info('Getting movie rating...')
    return ratings

@rating_router.get('/{movie_title}')
def get_rating_for_a_movie(movie_title: str, db: Session = Depends(get_db)):
    logger.info(f'Getting movie rating for {movie_title}')
    rating = crud.get_rating_for_movie(db, movie_title)
    return {"message": "success", "data": rating}

@rating_router.post('/')
def rate_movie(username: str,
               movie_title: str,
               payload: schema.RatingCreate, 
               user: schemau.User = Depends(get_current_user), 
               db: Session = Depends(get_db)
               ):
    logger.info('Adding rating for a movie...')
    rating = crud.add_ratings(db, payload, username, movie_title)
    logger.info(f"Movie rated successfully by {user.username}")
    return {'message': 'Rating added successfully', 'data': rating}
