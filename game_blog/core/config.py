import os
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings

SECRET_KEY = b"SECRET_KEY"
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

SQLALCHEMY_DATABASE_URL = 'sqlite:///./site.db'
ALEMBIC_SQLALCHEMY_DATABASE_URL = 'sqlite:///./site.db'

templates = Jinja2Templates(directory="templates")

TemplateResponse = templates.TemplateResponse
