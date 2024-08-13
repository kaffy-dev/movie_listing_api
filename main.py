from fastapi import FastAPI
from routers.movie import movie_router
from routers.user import user_router
from routers.comment import comment_router
from routers.rating import rating_router
from database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def home():
    return {"message": "Welcome to my movie listing app"}

app.include_router(user_router, prefix='/users', tags=['Registration'])
app.include_router(movie_router, prefix='/movies', tags=['Movies'])
app.include_router(comment_router, prefix='/comments', tags=['Comment on Movies'])
app.include_router(rating_router, prefix='/ratings', tags=['Rate Movies'])


