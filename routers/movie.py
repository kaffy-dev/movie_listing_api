from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import schema.movie as schema
import schema.user as schemau
from auth import get_current_user
from crud.movie import crudService as crud
from uuid import UUID

from logger import get_logger

logger = get_logger(__name__)

movie_router = APIRouter()

@movie_router.get('/')
def get_all_movies(db: Session = Depends(get_db), offset: int = 0, limit: int = 5):
    logger.info('Getting all movies')
    movies = crud.get_all_movies(db, offset, limit)
    return {'message': 'success', 'data': movies}

@movie_router.get('/{movie_id}')
def get_movie_by_id(movie_id: UUID, db: Session = Depends(get_db)):
    logger.info('Getting movie by id')
    movie = crud.get_movie_by_id(db, movie_id)
    if not movie:
        logger.error(f'Movie with the id,{movie_id} does not exist')
        raise HTTPException(detail="Movie not found", status_code=status.HTTP_404_NOT_FOUND)
    return {'message': 'success', 'data': movie}

@movie_router.get('/title/{movie_title}')
def get_movie_by_title(movie_title: str, db: Session = Depends(get_db)):
    logger.info('Getting movie by title')
    title = crud.get_movie_by_title(db, movie_title)
    if not title:
        logger.error(f'Movie with the title, {movie_title} does not exist')
        raise HTTPException(detail="Movie not found", status_code=status.HTTP_404_NOT_FOUND)
    return {'message': 'success', 'data': title}

@movie_router.post('/')
def create_movie(payload: schema.MovieCreate, 
                 user: schemau.User= Depends(get_current_user), 
                 db: Session = Depends(get_db)
                ):
    logger.info('Getting movie by title...')
    title_exists = crud.get_movie_by_title(db, movie_title=payload.title)
    if title_exists:
        logger.warning(f"{payload.title} already exists")
        raise HTTPException(detail="Title already exists",status_code=status.HTTP_400_BAD_REQUEST)
    movie = crud.create_movie(
        db, 
        payload,
        user_id = user.id
    )
    logger.info('Movie created successfully')
    return {'message': 'success', 'data': movie}

@movie_router.put('/{movie_id}')
def update_movie(movie_id: UUID, 
                 payload: schema.MovieUpdate, 
                 user: schemau.User = Depends(get_current_user), 
                 db: Session = Depends(get_db)
                ):
    logger.info('Making updates to a movie')
    movie = crud.update_movie(db, movie_id, payload, user_id = user.id)
    if not movie:
        logger.error('Movie not found')
        raise HTTPException(detail="Movie not found", status_code=status.HTTP_404_NOT_FOUND)
    
    logger.info('Update made to movie successfully')
    return {'message': 'Movie updated successfully', 'data': movie}

@movie_router.delete('/{movie_id}')
def delete_movie(movie_id: UUID, 
                 user: schemau.User = Depends(get_current_user), 
                 db: Session = Depends(get_db)
                ):
    logger.info('Deleting a movie using its title')
    movie = crud.delete_movie(db, movie_id, user_id = user.id)
    if not movie:
        logger.error('Movie not found')
        raise HTTPException(detail="Movie not found", status_code=status.HTTP_404_NOT_FOUND)
    logger.info('Movie deleted successfully')
    return {'message': 'Movie deleted successfully'}
    