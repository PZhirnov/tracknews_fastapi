from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from game_blog import users, posts
from game_blog.main.routes import router

from .database import engine
from .users import models
from .posts import models

users.models.Base.metadata.create_all(bind=engine)
posts.models.Base.metadata.create_all(bind=engine)


def create_app(debug=True):
    app = FastAPI(debug=debug)
    app.mount('/static', StaticFiles(directory='game_blog/static'),
              name='static')
    app.include_router(router)
    return app
