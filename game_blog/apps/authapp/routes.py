import json

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import status
from apps.authapp.form import UserCreateForm, UserLoginForm, UserUpdateForm
from apps.authapp.schemas import UserCreate
from core.config import TemplateResponse
from secrets import token_urlsafe
from db.repository.users import create_new_user
from db.session import get_db
from fastapi import responses
from sqlalchemy.exc import IntegrityError
from .models import User

user_router = APIRouter()


@user_router.post('/register/')
@user_router.get('/register/')
async def register(request: Request, db: Session = Depends(get_db)):
    """Контроллер используется для регистрации пользователя
    """
    print(db.query(User).all())
    if request.method == 'GET':
        return TemplateResponse("auth/register.html", {"request": request})
    else:
        form = UserCreateForm(request)
        await form.load_data()
        if await form.is_valid(db):
            user = UserCreate(username=form.username, email=form.email,
                              password=form.password)
            try:
                user = create_new_user(user=user, db=db)

                return responses.RedirectResponse(
                    "/login?msg=Successfully-Registered",
                    status_code=status.HTTP_302_FOUND
                )
            except IntegrityError:
                form.__dict__.get("errors").append(
                    "Duplicate username or email")
                return TemplateResponse("auth/register.html", form.__dict__)

        return TemplateResponse("auth/register.html", form.__dict__)


@user_router.post('/update/')
@user_router.get('/update/')
async def update(request: Request, db: Session = Depends(get_db)):
    if request.method == 'GET':
        return TemplateResponse("auth/update.html", {"request": request})
    else:
        form = UserUpdateForm(request)
        await form.load_data()
        if await form.is_valid(db):
            try:
                user = db.query(User).filter(
                    User.username == form.old_name).first()
                if form.username:
                    user.username = form.username
                if form.email:
                    user.email = form.email
                db.commit()
                return responses.JSONResponse(
                    {'status': 'success', 'user': user.username})
            except IntegrityError:
                form.__dict__.get("errors").append(
                    "Duplicate username or email")
                return TemplateResponse("auth/update.html", form.__dict__)

        return TemplateResponse("auth/update.html", form.__dict__)


@user_router.post('/login/')
@user_router.get('/login/')
async def login_page(request: Request, db: Session = Depends(get_db)):
    if request.method == 'POST':
        form = UserLoginForm(request)
        await form.load_data()
        if await form.is_valid(db):
            user = form.user
            token = token_urlsafe(32)
            user.token = token
            db.commit()
            response = responses.JSONResponse(
                {'status': 'success', 'token': token, 'user': form.username})
            return response
        else:
            return responses.JSONResponse(
                {'status': 'failed', 'errors': json.dumps(form.errors)})

    return TemplateResponse('auth/login.html', {'request': request})


@user_router.get('/logout/{username}')
async def logout(username, db: Session = Depends(get_db)):

    user = db.query(User).filter_by(username=username).first()
    user.token = ''
    db.commit()
    response = responses.RedirectResponse('/')
    return response
