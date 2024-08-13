from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import schema.rating as schema
import models
from crud.movie import crudService as movieCrud

from logger import get_logger

logger = get_logger(__name__)

class RatingService():
    @staticmethod
    def add_ratings(db: Session, rating: schema.RatingCreate, username: str, movie_title: str):
        logger.info('Querying the user model')
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
        
        logger.info('Getting movie by title')
        movie = movieCrud.get_movie_by_title(db, movie_title)
        if not movie:
            raise HTTPException(detail="Movie not found", status_code=status.HTTP_404_NOT_FOUND)
        db_rating = models.Rating(
            movie_rating = rating.movie_rating,
            movie_title = movie.title,
            username = user.username
        )
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        
        logger.info('Adding average_rating function from movieCrud')
        movieCrud.update_movie_average_rating(db, movie_title)

        rating_data =  {
                "movie_title": db_rating.movie_title,
                "username": db_rating.username,
                "movie_rating": db_rating.movie_rating
            }
        return rating_data

    
    @staticmethod
    def get_ratings(db: Session, offset: int = 0, limit: int = 5):
        logger.info('Querying the movie model')
        movies = db.query(models.Movie).offset(offset).limit(limit).all()
        movie_titles = {movie.title for movie in movies}
        logger.info('Querying the rating model...')
        ratings = db.query(models.Rating).offset(offset).limit(limit).all()
        movie_ratings = {}

        logger.info('Getting all ratings to calculate average')
        for rating in ratings:
            if rating.movie_title not in movie_ratings:
                movie_ratings[rating.movie_title] = []
            movie_ratings[rating.movie_title].append(rating.movie_rating)
        
        # Average rating
        logger.info('Calculating average rating')
        aggregated_ratings = []
        for movie_title in movie_titles:
            ratings_list = movie_ratings.get(movie_title, [])
            if ratings_list:
                average_rating = round(sum(ratings_list) / len(ratings_list), 1)
            else:
                average_rating = 0
            aggregated_ratings.append({
                "movie_title": movie_title,
                "average_rating": average_rating
            })
        
        return aggregated_ratings
    
    @staticmethod
    def get_rating_for_movie(db: Session, movie_title: str):
        logger.info('Getting movie by title')
        movie = movieCrud.get_movie_by_title(db, movie_title)
        if not movie:
            raise HTTPException(detail="Movie not found", status_code=status.HTTP_404_NOT_FOUND)
        logger.info('Querying the rating model...')
        ratings = db.query(models.Rating).filter(models.Rating.movie_title == movie_title).all()
        if not ratings:
            return {"movie_title": movie_title, "rating": 0}
        average_rating = round((sum(rating.movie_rating for rating in ratings) / len(ratings)), 1)

        aggregate_rating = {
            "movie_title": movie_title,
            "rating": average_rating
        }

        return aggregate_rating
    
        

crudService = RatingService()