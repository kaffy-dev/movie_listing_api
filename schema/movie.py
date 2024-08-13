from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date

class MovieBase(BaseModel):
    title: str
    description: str
    duration: str
    release_date: date = "YYYY-MM-DD"

class Movie(MovieBase):
    id: UUID
    user_id: UUID
    average_rating: Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True)

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    release_date: Optional[date] = None