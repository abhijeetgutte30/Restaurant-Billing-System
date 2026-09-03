import os

from flask_bcrypt import Bcrypt
from flask_login import LoginManager

bcrypt = Bcrypt()

login_manager = LoginManager()

login_manager.login_view = "auth.login"


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-change-this"
    )

    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql+psycopg://",
            1
        )

    SQLALCHEMY_DATABASE_URI = (
        DATABASE_URL
        or "sqlite:///database.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False