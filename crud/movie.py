from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import schema.movie as schema
import models
from uuid import UUID

from logger import get_logger

logger = get_logger(__name__)

class MovieService:
    @staticmethod
    def create_movie(db: Session, movie: schema.MovieCreate, user_id: UUID = None):
        logger.info('Creating a movie...')
        db_movie = models.Movie(
            **movie.model_dump(),
            user_id = user_id,
        )
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie
  
    @staticmethod
    def update_movie_average_rating(db: Session, movie_title: str):
        logger.info('Querying the rating model for all')
        ratings = db.query(models.Rating).filter_by(movie_title=movie_title).all()
        if not ratings:
            return
        
        logger.info('Getting all ratings to calculate average rating')
        rating_values = []
        for rating in ratings:
            rating_values.append(rating.movie_rating)
        average_rating = round((sum(rating_values) / len(rating_values)), 1)

        db_movie = db.query(models.Movie).filter_by(title=movie_title).first()
        logger.info("Updating the movie's average rating")
        if db_movie:
            db_movie.average_rating = average_rating
            db.commit()
            db.refresh(db_movie)

    @staticmethod
    def get_all_movies(db: Session, offset: int = 0, limit: int =5):
        logger.info('Querying the movie model')
        movies = db.query(models.Movie).offset(offset).limit(limit).all()
        
        logger.info('Getting all ratings to calculate average rating')
        ratings = db.query(models.Rating).all()
        movie_ratings = {}
        for rating in ratings:
            if rating.movie_title not in movie_ratings:
                movie_ratings[rating.movie_title] = []
            movie_ratings[rating.movie_title].append(rating.movie_rating)
        
        logger.info('Calculating average rating...')
        average_rating = {}
        for movie_title, ratings in movie_ratings.items():
            if ratings:
               average_rating[movie_title] = round((sum(ratings) / len(ratings)), 1)
            else:
               average_rating[movie_title] = 0

        response_data = []
        for movie in movies:
            movie_data = {
               "id": movie.id,
               "user_id": movie.user_id,
               "title": movie.title,
               "description": movie.description,
               "duration": movie.duration,
               "release_date": movie.release_date,
               "average_rating": average_rating.get(movie.title, 0)
            }

            response_data.append(movie_data)
        return response_data
        
    @staticmethod
    def get_movie_by_id(db: Session, movie_id: UUID):
        logger.info('Querying movie model for movie_id')
        return db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    
    @staticmethod
    def get_movie_by_title(db: Session, movie_title: str):
        logger.info('Querying movie model for movie_title')
        return db.query(models.Movie).filter(models.Movie.title == movie_title).first()

    @staticmethod
    def update_movie(db: Session, movie_id: int, movie_payload: schema.MovieUpdate, user_id: UUID):
        logger.info('Getting movie by id')
        movie = crudService.get_movie_by_id(db, movie_id)
        if not movie:
           return None
        
        if movie.user_id != user_id:
            raise HTTPException(
                detail= "Book not created by user cannot be updated", 
                status_code=status.HTTP_403_FORBIDDEN
            )
        movie_payload_dict = movie_payload.model_dump(exclude_unset=True)

        for k, v in movie_payload_dict.items():
            setattr(movie, k, v)
        db.add(movie)
        db.commit()
        db.refresh(movie)
        return movie
    
    @staticmethod
    def delete_movie(db: Session, movie_id: int, user_id: UUID):
        logger.info('Getting movie by id')
        movie = crudService.get_movie_by_id(db, movie_id)
        if not movie:
            raise HTTPException(detail="Movie does not exist", status_code=status.HTTP_404_NOT_FOUND)
        if movie.user_id != user_id:
            raise HTTPException(
                detail= "Movie not created by user cannot be deleted", 
                status_code=status.HTTP_403_FORBIDDEN
            )
        logger.info('Deleting movie when it is found')
        if movie:
            db.delete(movie)
            db.commit()
            return True
        return False


crudService = MovieService()