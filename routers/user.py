import schema.user as schema
import crud.user as crud
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy.orm import Session
from auth import pwd_context, authenticate_user, create_access_token

from logger import get_logger

logger = get_logger(__name__)

user_router = APIRouter()

@user_router.post('/signup')
def signup(user: schema.UserCreate, db: Session = Depends(get_db)):
    logger.info('Creating user...')
    db_user = crud.get_user_by_username(db, username=user.username)
    hashed_password = pwd_context.hash(user.password)
    if db_user:
        logger.warning(f'User with username, "{user.username}" already exists')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    logger.info('User created successfully')
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)

@user_router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info('Generating authentication token...')
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            detail="Incorrect username or password", 
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.username})
    logger.info(f"Token successfully generated for {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}
