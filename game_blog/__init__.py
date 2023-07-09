from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .apps import authapp
from game_blog.apps.mainapp import router

from .database import engine

game_blog.apps.users.models.Base.metadata.create_all(bind=engine)
game_blog.apps.posts.models.Base.metadata.create_all(bind=engine)


def create_app(debug=True):
    app = FastAPI(debug=debug)
    app.mount('/static', StaticFiles(directory='game_blog/static'),
              name='static')
    app.include_router(router)
    return app
