from pydantic import BaseModel, ConfigDict
from uuid import UUID

class UserBase(BaseModel):
    username: str

class User(UserBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    full_name: str
    password: str
