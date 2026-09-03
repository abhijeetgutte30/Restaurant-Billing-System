from database.database import db
from flask_login import UserMixin
from config import bcrypt, login_manager


from database.database import db
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class Admin(UserMixin, db.Model):

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Menu(db.Model):

    __tablename__ = "menu"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    category = db.Column(db.String(100), nullable=False)

    price = db.Column(db.Float, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))