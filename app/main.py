from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, alchemy_post, auth, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

my_posts = [
    {
        "title": "post 1 title",
        "content": "post 1 content",
        "id": 123,
    },
    {
        "title": "favorite foods",
        "content": "I like pizza",
        "id": 128,
    }
]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_post_index(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index


app.include_router(user.router)
app.include_router(post.router)
app.include_router(alchemy_post.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    return {"message": "Hello berry"}



