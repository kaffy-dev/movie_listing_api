from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import Optional

class RatingBase(BaseModel):
    movie_rating: Optional[float] = Field(None, ge=1.0, le=10.0)

class Rating(RatingBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)

class RatingCreate(RatingBase):
    pass

class RatingResponse(BaseModel):
    movie_title: str
    average_rating: float

    model_config = ConfigDict(from_attributes=True)
