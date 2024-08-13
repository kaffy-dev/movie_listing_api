import uuid
from sqlalchemy import Column, String, ForeignKey, Date, Float, CheckConstraint, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID,JSON

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)

    # Relationships
    movies = relationship("Movie", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey('users.id'))
    title = Column(String, unique=True, index=True)
    description = Column(String)
    duration = Column(String)
    release_date = Column(Date)
    average_rating = Column(Float)
    
    #  Relationships
    user = relationship("User", back_populates="movies")
    comments = relationship("Comment", back_populates="movie", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")


def default_replies():
    return []

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    movie_id = Column(UUID, ForeignKey('movies.id'))
    username = Column(String, nullable=False)
    content = Column(String, nullable=False)
    replies = Column(JSON, default=default_replies)

    # Relationships
    movie = relationship("Movie", back_populates="comments")
    

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    movie_title = Column(String, ForeignKey('movies.title'))
    movie_rating = Column(Float, nullable=True)
    username = Column(String, ForeignKey('users.username'))

    # Relationships
    movie = relationship('Movie', back_populates='ratings')
    
    # Constraint to make sure rating is 1-10
    __table_args__ = (
        CheckConstraint('movie_rating >= 1 AND movie_rating <= 10', name='check_movie_rating_range'),
    )



