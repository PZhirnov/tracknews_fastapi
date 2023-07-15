from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from apps.authapp.routes import user_router
from core.config import TemplateResponse

api_router = APIRouter()
api_router.include_router(user_router)


@api_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return TemplateResponse('index.html', {'request': request})
