from typing import List, Optional
from sqlalchemy.orm import Session

from core.hashing import Hasher
from core.requests_framework import PostRequest
from .models import User
from fastapi import Request


class UserForm:
    def __init__(self, request: Request) :
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None

    async def load_data(self):
        pass

    async def is_valid(self, db: Session):
        return True

    async def validate_username(self, db: Session):
        user = db.query(User).filter(User.username ==
                                     self.username).first()
        if user:
            self.errors.append(
                f'User with username {self.username} has already')


class UserCreateForm(UserForm):
    def __init__(self, request: Request):
        super().__init__(request)
        self.password: Optional[str] = None
        self.email: Optional[str] = None
        self.confirm_password: Optional[str] = None

    async def load_data(self):
        data = await self.request.body()
        data = PostRequest.parse_body_json(data)
        self.username = data.get('username')
        self.password = data.get('password')

    async def is_valid(self, db: Session):
        if not all([self.username, self.password]):
            self.errors.append('Пожалуйста, введите данные!')
        else:
            user = db.query(User).filter(User.username == self.username).first()
            self.user = user
            if not user:
                self.errors.append(f'Пользователя с именем {self.username} не существует!')
            else:
                verified = Hasher.verify_password(self.password, user.hashed_password)
                if not verified:
                    self.errors.append('Пароль не корректный')
        if not self.errors:
            return True


class UserUpdateForm(UserForm):
    def __init__(self, request: Request):
        super().__init__(request)
        self.email: Optional[str] = None
        self.user: Optional[str] = None

    async def load_data(self):
        data = await self.request.body()
        data = PostRequest.parse_body_json(data)
        self.username = data.get('username')
        self.email = data.get('email')
        self.old_name = data.get('old')

    async def is_valid(self, db:Session):
        await self.validate_username(db)
        await self.validate_email(db)

        if not self.errors:
            return True
        return False

    async def validate_email(self, db: Session):
        user = db.query(User).filter(User.email == self.email).first()

        if user:
            self.errors.append(f'Пользователь с электронной почтой {self.email} уже существует.')
